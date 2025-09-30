# Classificador de Emails

## Instruções para rodar o projeto

### Configurações Iniciais

**Recomendado: Crie um virtualenv para realizar a instalação das bibliotecas necessárias com pip**
```
virtualenv env
```
Ou
```
python3 -m venv env
```

Ative o virtual env

```
source env/bin/activate
```

**Instalando as Dependências**

O projeto já possui um arquivo `requirements.txt` com todas as dependências do projeto.

```
pip install -r requirements.txt
```

**Chave da API do Gemini**

Caso nessesário, crie uma chave para usar a API do Gemini (Free tier). Ela será necessária para a geração de sugestão de respostas (exceto por template).

[Gemini API Documentation - API Keys](https://ai.google.dev/gemini-api/docs/api-key)

O cliente da api busca a chave de uma variável de ambiente `GEMINI_API_KEY`

```
export GEMINI_API_KEY="<YOUR_API_KEY>"
```

**Modelo Classificador**

Os arquivos do modelo classificador de emails devem ser colocados dentro da pasta `backend/utils/email_classifier_hf`.

Ele pode ser obtido através desse [link de download](https://drive.google.com/file/d/1B9hfwCrQpYUdP_c_aQVXDS6HV6jTWCE1/view?usp=sharing) ou rodando o arquivo .ipynb no Google Colab ou similar.

Para extrair os arquivos
```
unzip email_classifier_hf.zip
```

Mova a pasta para `avaiador_de_email/backend/utils`
```
mv email_classifier_hf avaiador_de_email/backend/utils
```

### Rodando a Aplicação

Com as configurações feitas, vá para o diretŕio `backend` e rode
```
 flask --app app run
```
