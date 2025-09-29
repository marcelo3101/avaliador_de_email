"""
    Functions for using the AI models
"""

from transformers import AutoTokenizer, AutoModelForSequenceClassification, AutoModelForSeq2SeqLM, pipeline
import os

# Get absolute path for model instantiation
path = os.path.abspath(__file__)
dirpath = os.path.dirname(path)

# Classifier model declaration and function
classifier_model_path = dirpath + "/email_classifier_hf"
tokenizer = AutoTokenizer.from_pretrained(classifier_model_path)
classifier_model = AutoModelForSequenceClassification.from_pretrained(classifier_model_path)
classifier = pipeline("text-classification", model=classifier_model, tokenizer=tokenizer)

def classify_email_text(email_text: str):
    result = classifier(email_text)[0]
    
    # Check label and return classification
    return "Produtivo" if result["label"] == "LABEL_1" else "Improdutivo"

# Response generation model declaration and function
generator_model_path = dirpath + "/flan-t5-small"
generator_tokenizer = AutoTokenizer.from_pretrained(generator_model_path)
generator_model = AutoModelForSeq2SeqLM.from_pretrained(generator_model_path)
generator = pipeline("text2text-generation", model=generator_model, tokenizer=generator_tokenizer)

def generate_response(email_text: str):
    prompt = f"Write a professional answer for the following email in Portuguese:\n\n{email_text}\n\n"
    generated_response = generator(
        prompt,
        max_new_tokens=1024,
        num_beams=5
    )

    return generated_response[0]["generated_text"]
