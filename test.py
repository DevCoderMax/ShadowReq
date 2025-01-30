from ShadowReq import ShadowReq

# Criar uma instância do ShadowReq
shadow = ShadowReq()

# Fazer uma requisição GET para um endpoint de teste
response = shadow.get('https://httpbin.org/get')

# Verificar a resposta
if response.status_code == 200:
    print("Resposta GET recebida com sucesso!")
    print(response.text)
else:
    print(f"Erro na requisição GET: {response.status_code}")

# Exemplo de POST com dados
data = {
    "name": "John Doe",
    "email": "john@example.com"
}
response = shadow.post('https://httpbin.org/post', data=data)

print("\nResposta do POST:")
print(f"Status: {response.status_code}")
print(f"Conteúdo: {response.text}")
