"""
    Functions for using the AI models
"""

from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import os

path = os.path.abspath(__file__)
dirpath = os.path.dirname(path)
print(f"PATH AQUI: {dirpath}")
# Classifier model declaration and function
classifier_model_path = dirpath + "/email_classifier_hf"
tokenizer = AutoTokenizer.from_pretrained(classifier_model_path)
classifier_model = AutoModelForSequenceClassification.from_pretrained(classifier_model_path)
classifier = pipeline("email-classification", model=classifier_model, tokenizer=tokenizer)

def classify_email_text(email_text: str):
    result = classifier(email_text)[0]
    
    # Check label and return classification
    return "Produtivo" if result["label"] == "LABEL_1" else "Improdutivo"

# Response generation model declaration and function
generator_model_path = dirpath + "flan-t5-small"
generator_tokenizer = AutoTokenizer.from_pretrained(generator_model_path)
generator_model = AutoModelForSequenceClassification.from_pretrained(generator_model_path)
generator = pipeline("response-generator", model=generator_model, tokenizer=generator_tokenizer)

def generate_response(email_text: str):
    prompt = f"Gere uma resposta educada e profissional para este email: {email_text}"
    generated_response = generator(prompt, max_length = 50)

    return generated_response
