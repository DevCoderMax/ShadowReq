# ShadowReq

Uma biblioteca Python para fazer requisições HTTP através de servidores intermediários, mantendo cookies e headers atualizados automaticamente.

## Características Implementadas

- ✅ Suporte a métodos HTTP básicos (GET, POST, PUT, DELETE)
- ✅ Configuração via arquivo JSON para múltiplos servidores
- ✅ Atualização automática de cookies usando Selenium
- ✅ Captura automática de User-Agent do navegador
- ✅ Suporte a timeout nas requisições
- ✅ Interface de linha de comando (CLI)

## Instalação

```bash
# Criar e ativar ambiente virtual (opcional)
python -m venv .venv
source .venv/bin/activate

# Instalar dependências e o pacote
pip install -r requirements.txt
pip install -e .

# Instalar Biblioteca
pip install git+https://github.com/DevCoderMax/ShadowReq.git
```

## Uso da Biblioteca

```python
from shadowreq import ShadowReq

# Criar instância com timeout personalizado
shadow = ShadowReq(timeout=(5, 30))  # 5s conexão, 30s leitura

# Fazer requisição GET
response = shadow.get('https://httpbin.org/get')
print(f"Status: {response.status_code}")
print(response.text)

# Fazer requisição POST com dados
data = {'name': 'John Doe', 'email': 'john@example.com'}
response = shadow.post('https://httpbin.org/post', data=data)
print(f"Status: {response.status_code}")
print(response.text)
```

## Uso do CLI

O ShadowReq inclui uma interface de linha de comando para tarefas comuns:

```bash
# Ver comandos disponíveis
shadowreq --help

# Atualizar cookies dos servidores
shadowreq update-cookies

# Usar arquivo de configuração específico
shadowreq update-cookies --config outro_arquivo.json
```

## Estrutura do Projeto

```
ShadowReq/
├── README.md
├── VERSION               # Versão atual do pacote
├── requirements.txt      # Dependências do projeto
├── server/
│   └── api.php          # Servidor intermediário
├── servers.json         # Configuração dos servidores
├── setup.py             # Configuração do pacote
├── shadowreq/
│   ├── __init__.py      # Exporta a classe principal
│   ├── version.py       # Versão da biblioteca
│   ├── client.py        # Implementação principal
│   ├── cookie_updater.py # Atualização de cookies
│   └── cli.py           # Interface de linha de comando
└── test.py              # Testes básicos
```

## Próximas Tarefas

1. **Melhorias no Servidor PHP**
   - [ ] Implementar cache de respostas
   - [ ] Adicionar compressão gzip/deflate
   - [ ] Melhorar tratamento de erros e logging
   - [ ] Implementar rate limiting
   - [ ] Adicionar suporte a streaming

2. **Melhorias no Cliente**
   - [ ] Adicionar suporte a proxy
   - [ ] Implementar sistema de retry
   - [ ] Adicionar suporte a sessões
   - [ ] Suporte a upload/download de arquivos
   - [ ] Implementar cache local

3. **Segurança**
   - [ ] Implementar verificação SSL configurável
   - [ ] Adicionar suporte a autenticação HTTP
   - [ ] Proteção contra CSRF
   - [ ] Sistema de tokens entre cliente e servidor

4. **Usabilidade**
   - [ ] Adicionar logs detalhados
   - [ ] Criar decoradores para retry e cache
   - [ ] Adicionar suporte a async/await
   - [ ] Implementar modo debug

5. **Documentação**
   - [ ] Adicionar exemplos mais complexos
   - [ ] Documentar todas as opções
   - [ ] Criar guia de troubleshooting
   - [ ] Adicionar testes unitários

## Contribuição

Contribuições são bem-vindas! Por favor, sinta-se à vontade para submeter um Pull Request.
