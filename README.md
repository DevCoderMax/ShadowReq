# ShadowReq

Uma biblioteca Python para fazer requisições HTTP através de servidores intermediários, mantendo cookies e headers atualizados automaticamente.

## Características Implementadas

- ✅ Suporte a métodos HTTP básicos (GET, POST, PUT, DELETE)
- ✅ Configuração via arquivo JSON para múltiplos servidores
- ✅ Atualização automática de cookies usando Selenium
- ✅ Captura automática de User-Agent do navegador
- ✅ Suporte a timeout nas requisições

## Instalação

```bash
pip install -r requirements.txt
```

## Uso Básico

```python
from ShadowReq import ShadowReq

# Criar instância com timeout personalizado
shadow = ShadowReq(timeout=(5, 30))  # 5s conexão, 30s leitura

# Fazer requisição GET
response = shadow.get('https://api.example.com/data')

# Fazer requisição POST com dados
data = {'name': 'John Doe', 'email': 'john@example.com'}
response = shadow.post('https://api.example.com/users', data=data)

# Verificar resposta
if response.status_code == 200:
    print(response.text)
```

## Atualização de Cookies

Para atualizar os cookies dos servidores:

```python
python autogetcookie.py
```

O script irá:
1. Acessar cada servidor configurado em `servers.json`
2. Capturar o cookie `__test` e User-Agent
3. Atualizar automaticamente o arquivo de configuração

## Próximas Tarefas

1. **Melhorias de Funcionalidade**
   - [ ] Adicionar suporte a proxy
   - [ ] Implementar sistema de retry em caso de falha
   - [ ] Adicionar suporte a sessões (similar ao requests.Session)
   - [ ] Suporte a upload de arquivos
   - [ ] Adicionar opção de compressão gzip/deflate

2. **Melhorias de Segurança**
   - [ ] Implementar verificação SSL configurável
   - [ ] Adicionar suporte a autenticação HTTP
   - [ ] Proteção contra CSRF

3. **Melhorias de Usabilidade**
   - [ ] Adicionar logs detalhados
   - [ ] Criar decoradores para retry e cache
   - [ ] Melhorar tratamento de erros
   - [ ] Adicionar suporte a async/await

4. **Documentação**
   - [ ] Adicionar exemplos mais complexos
   - [ ] Documentar todas as opções de configuração
   - [ ] Criar guia de contribuição
   - [ ] Adicionar testes unitários

## Contribuição

Contribuições são bem-vindas! Por favor, sinta-se à vontade para submeter um Pull Request.
