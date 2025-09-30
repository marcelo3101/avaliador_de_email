"""
    Functions for using the AI models
"""

from google import genai

import os

# Get absolute path for model instantiation
path = os.path.abspath(__file__)
dirpath = os.path.dirname(path)


# Using Gemini API
# The client gets the API key from the environment variable `GEMINI_API_KEY`
client = genai.Client()

def classify_and_generate_response(email_text: str):
    #prompt = f"Escreva uma resposta para o seguinte email: '{email_text}'" 
    prompt = f"""
        Classifique o seguinte email em uma das duas categorias explicadas:
        Produtivo: Emails que requerem uma ação ou resposta específica (ex.: solicitações de suporte técnico, atualização sobre casos em aberto, dúvidas sobre o sistema).
        Improdutivo: Emails que não necessitam de uma ação imediata (ex.: mensagens de felicitações, agradecimentos).

        Após classificar, escreva uma resposta profissional e educada para o email. O Texto do email é: '{email_text}'

        Na sua resposta retorne o nome da classificação e o texto da resposta gerada, separados por &&. Exemplo:
        <classificação>&&<Resposta>
    """

    # Using Gemini 2.5 Flash-Lite because of its higher request per day rate
    generated_response = client.models.generate_content(
        model="gemini-2.5-flash-lite", contents=prompt
    )
    
    return generated_response.text

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
def generate_response_from_template(email_category, email_text: str):
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