"""
    Functions for using the AI models
"""

from transformers import AutoTokenizer, AutoModelForSequenceClassification, AutoModelForSeq2SeqLM, pipeline
import os
from typing import List, Dict

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
    return ("Produtivo", 1) if result["label"] == "LABEL_1" else ("Improdutivo", 0)

# Response generation model declaration and function
generator_model_path = dirpath + "/flan-t5-small"
generator_tokenizer = AutoTokenizer.from_pretrained(generator_model_path)
generator_model = AutoModelForSeq2SeqLM.from_pretrained(generator_model_path)
generator = pipeline("text2text-generation", model=generator_model, tokenizer=generator_tokenizer)

def generate_response(email_text: str):
    #prompt = f"Escreva uma resposta para o seguinte email: '{email_text}'" 
    prompt = f"Write a polite answer for the following email: '{email_text}'"

    generated_response = generator(prompt, num_beams=5)

    return generated_response[0]["generated_text"]


templates_productive = {
    "relatório": "Olá! Recebemos sua solicitação do relatório. Segue em anexo ou iremos providenciar o quanto antes.",
    "solicitação": "Sua solicitação foi recebida e será processada em breve. Entraremos em contato se precisarmos de mais informações.",
    "acesso": "O acesso solicitado foi liberado. Por favor, verifique e nos avise caso haja algum problema.",
    "documento": "Obrigado pelo envio do documento. Nossa equipe analisará e retornará em breve.",
    "agendar": "Podemos agendar conforme sua disponibilidade. Qual horário seria melhor para você?",
    "status": "O status da sua solicitação está em andamento. Retornaremos com atualizações em breve.",
    "projeto": "Sua demanda sobre o projeto foi recebida e estamos tomando as providências necessárias.",
    "comprovante": "Segue o comprovante solicitado em anexo. Qualquer dúvida, estou à disposição.",
    "atualizar": "A atualização solicitada foi realizada. Por favor, verifique se está tudo correto."
}

# Exemplos de respostas para emails improdutivos
templates_unproductive = {
    "natal": "Muito obrigado! Desejamos também a você ótimas festas e um excelente ano novo!",
    "aniversário": "Muito obrigado pela lembrança!",
    "obrigado": "Agradecemos pela mensagem! Estamos sempre à disposição.",
    "parabéns": "Muito obrigado pelo reconhecimento! Isso nos motiva a continuar melhorando.",
    "sucesso": "Agradecemos os votos de sucesso! Continuamos à disposição.",
    "ótimo": "Obrigado! Desejamos também um ótimo dia/semana para você."
}

# Generates answer using keywords and email category
def generate_response_from_template(email_category: bool, email_text: str):
    text = email_text.lower()
    
    # 0 for unproductive and 1 for productive
    if email_category:  # Productive
        for key, template in templates_productive.items():
            if key in text:
                return template
            
    else:
        for key, template in templates_unproductive.items():
            if key in text:
                return template

    # Generic template in case no keywords are found
    return "Agradecemos pela mensagem! Seu email foi recebido e nossa equipe entrará em contato em breve."