import os
from flask import Flask, render_template, request, jsonify
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
import nltk
import textstat
import markovify

# Download necessary NLTK data
nltk.download('vader_lexicon')
nltk.download('punkt')
nltk.download('stopwords')

app = Flask(__name__)

# Sample text for Markov chain model (replace with a larger corpus for better results)
sample_text = """
Artificial intelligence (AI) is intelligence demonstrated by machines, as opposed to natural intelligence displayed by animals including humans. AI research has been defined as the field of study of intelligent agents, which refers to any system that perceives its environment and takes actions that maximize its chance of achieving its goals.
The term "artificial intelligence" had previously been used to describe machines that mimic and display "human" cognitive skills that are associated with the human mind, such as "learning" and "problem-solving". This definition has since been rejected by major AI researchers who now describe AI in terms of rationality and acting rationally, which does not limit how intelligence can be articulated.
"""

# Create a Markov chain model
text_model = markovify.Text(sample_text)

def generate_content(prompt):
    # Generate a sentence based on the prompt (not truly using the prompt, just for demonstration)
    return text_model.make_sentence() or "Failed to generate content. Please try again."

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