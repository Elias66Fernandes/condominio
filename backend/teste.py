import requests
import json

# URL da rota que você deseja testar
url = 'http://127.0.0.1:5000/taxas'

# Dados do formulário (usuarios_id, valor, data_venc, data_cadastro)
data = {
    'usuarios_id': '1',
    'valor': '100.0',
    'data_venc': '2024-05-30',
    'data_cadastro': '2024-05-01',
}

# Arquivo PDF que você deseja enviar
files = {'boleto': open(r'C:/Users/ipslf/OneDrive/Área de Trabalho/Backend Condomínio/PORTIFÓLIO XII SENGE (com plano de patrocínio 2).pdf', 'rb')}

# Envia a solicitação POST com os dados do formulário e o arquivo PDF
response = requests.post(url, json=data, files=files)

# Verifica a resposta
if response.status_code == 201:
    print('Taxa criada com sucesso!')
else:
    print('Erro ao criar taxa:', response.text)
