import os
from flask import Flask, render_template, request, jsonify
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
import nltk
import textstat
from vertexai.generative_models import (
    GenerationConfig,
    GenerativeModel,
    HarmBlockThreshold,
    HarmCategory,
    Part,
)



# Download necessary NLTK data
nltk.download('vader_lexicon')
nltk.download('punkt')
nltk.download('stopwords')

app = Flask(__name__)

# Initialize Vertex AI
#aiplatform.init(project=os.environ['GOOGLE_CLOUD_PROJECT'], location='us-central1')

def generate_content(prompt):
    # Get the Gemini model
    #model = aiplatform.GenerativeModel("gemini-1.0-pro")

    # Load Gemini 1.5 Pro Model
    MODEL_ID = "gemini-1.5-pro-001"
    model = GenerativeModel(MODEL_ID)

    # Load a example model with system istructions
    example_model = GenerativeModel(
        MODEL_ID,
        system_instruction=[
            "You are a helpful text generator.",
            "Your mission is help complete paragraphs.",
        ],
    )

    # Set model parameters
    generation_config = GenerationConfig(
        temperature=0.9,
        top_p=1.0,
        top_k=32,
        candidate_count=1,
        max_output_tokens=8192,
    )

    # Set safety settings
    safety_settings = {
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    }

    # Set contents to send to the model
    contents = [prompt]

    # Prompt the model to generate content
    response = example_model.generate_content(
        contents,
        generation_config=generation_config,
        safety_settings=safety_settings,
    )


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

port = int(os.environ.get('PORT', 8080))
#app.run(host='0.0.0.0', port=port)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=port)
