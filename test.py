#!/usr/bin/env python3
"""
Testes básicos do ShadowReq
"""

from shadowreq import ShadowReq

def test_get_request():
    """Testa uma requisição GET básica."""
    shadow = ShadowReq()
    
    # Teste com httpbin
    response = shadow.get('https://httpbin.org/get')
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")

def test_post_request():
    """Testa uma requisição POST com dados."""
    shadow = ShadowReq()
    
    # Dados de exemplo
    data = {
        'name': 'John Doe',
        'email': 'john@example.com',
        'message': 'Hello World!'
    }
    
    # Teste com httpbin
    response = shadow.post('https://httpbin.org/post', data=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")

def main():
    """Função principal para executar os testes."""
    print("Testando GET request...")
    test_get_request()
    
    print("\nTestando POST request...")
    test_post_request()

if __name__ == '__main__':
    main()
