#!/usr/bin/env python3
"""
Testes básicos do ShadowReq usando API de IP
"""

from shadowreq import ShadowReq
import time

def test_multiple_requests():
    """Testa múltiplas requisições para mostrar o rodízio de servidores."""
    shadow = ShadowReq(enable_logging=True)
    
    # Fazer várias requisições para ver o rodízio
    for i in range(5):
        print(f"\nRequisição {i+1}:")
        response = shadow.get('http://ip-api.com/json/')
        print(f"Status: {response.status_code}")
        print(f"IP Info: {response.text}")
        time.sleep(1)  # Esperar 1 segundo entre requisições

def main():
    """Função principal para executar os testes."""
    print("Testando rodízio de servidores...")
    test_multiple_requests()

if __name__ == '__main__':
    main()
