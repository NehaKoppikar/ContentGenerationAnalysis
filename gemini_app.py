import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
import nltk
import textstat

# Download necessary NLTK data
nltk.download('vader_lexicon')
nltk.download('punkt')
nltk.download('stopwords')

app = Flask(__name__)

# Configure Gemini API
genai.configure(api_key="")
model = genai.GenerativeModel('gemini-pro')

def generate_content(prompt):
    response = model.generate_content(prompt)
    return response.text

def analyze_content(text):
    # Sentiment analysis
    sia = SentimentIntensityAnalyzer()
    sentiment = sia.polarity_scores(text)

    # Key topics
    words = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in words if word.isalnum() and word not in stop_words]
    word_freq = Counter(filtered_words)
    top_topics = word_freq.most_common(5)

    # Readability
    readability = textstat.flesch_reading_ease(text)

    return {
        'sentiment': sentiment,
        'top_topics': top_topics,
        'readability': readability
    }

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        prompt = request.form['prompt']
        generated_content = generate_content(prompt)
        analysis = analyze_content(generated_content)
        return render_template('result.html', content=generated_content, analysis=analysis)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
