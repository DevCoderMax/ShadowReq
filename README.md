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

1. **Melhorias no Servidor PHP**
   - [ ] Adicionar suporte a headers customizados na requisição
   - [ ] Implementar cache de respostas no servidor
   - [ ] Adicionar compressão gzip/deflate nas respostas
   - [ ] Melhorar tratamento de erros e logging
   - [ ] Implementar rate limiting por IP
   - [ ] Adicionar suporte a streaming de dados
   - [ ] Implementar validação de origem das requisições

2. **Melhorias no ShadowReq**
   - [ ] Adicionar suporte a proxy
   - [ ] Implementar sistema de retry em caso de falha
   - [ ] Adicionar suporte a sessões (similar ao requests.Session)
   - [ ] Suporte a upload de arquivos
   - [ ] Implementar cache local de respostas
   - [ ] Adicionar suporte a websockets
   - [ ] Criar sistema de eventos e callbacks
   - [ ] Implementar download de arquivos com progresso

3. **Melhorias no Gerenciamento de Servidores**
   - [ ] Adicionar suporte a múltiplos servidores com fallback
   - [ ] Implementar health check dos servidores
   - [ ] Sistema de balanceamento de carga simples
   - [ ] Rotação automática de servidores em caso de erro
   - [ ] Interface de administração web simples
   - [ ] Monitoramento de uso e estatísticas
   - [ ] Sistema de blacklist/whitelist de URLs

4. **Melhorias de Segurança**
   - [ ] Implementar verificação SSL configurável
   - [ ] Adicionar suporte a autenticação HTTP
   - [ ] Proteção contra CSRF
   - [ ] Sanitização de URLs e parâmetros
   - [ ] Sistema de tokens para autenticação entre cliente e servidor
   - [ ] Limitar tipos de conteúdo permitidos
   - [ ] Implementar timeouts no servidor PHP

5. **Melhorias na Automação**
   - [ ] Criar script de instalação automática do servidor
   - [ ] Implementar atualização automática de configurações
   - [ ] Sistema de backup de cookies e configurações
   - [ ] Agendamento de atualizações de cookies
   - [ ] Notificações de erros via email/webhook
   - [ ] Interface CLI para gerenciamento
   - [ ] Integração com Docker para fácil deployment

6. **Melhorias de Usabilidade**
   - [ ] Adicionar logs detalhados
   - [ ] Criar decoradores para retry e cache
   - [ ] Melhorar tratamento de erros
   - [ ] Adicionar suporte a async/await
   - [ ] Criar sistema de plugins
   - [ ] Implementar modo debug com informações detalhadas
   - [ ] Adicionar suporte a diferentes formatos de configuração (YAML, ENV)

7. **Documentação**
   - [ ] Adicionar exemplos mais complexos
   - [ ] Documentar todas as opções de configuração
   - [ ] Criar guia de contribuição
   - [ ] Adicionar testes unitários
   - [ ] Documentar processo de instalação do servidor
   - [ ] Criar troubleshooting guide
   - [ ] Adicionar diagramas de arquitetura

## Contribuição

Contribuições são bem-vindas! Por favor, sinta-se à vontade para submeter um Pull Request.
