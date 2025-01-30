"""
Interface de linha de comando para o ShadowReq.
"""

import argparse
import os
from .cookie_updater import CookieUpdater

def update_cookies(args):
    """Atualiza os cookies dos servidores."""
    config_path = os.path.abspath(args.config)
    print(f"Usando arquivo de configuração: {config_path}")
    
    if not os.path.exists(config_path):
        print(f"Erro: Arquivo {config_path} não encontrado")
        return
    
    try:
        updater = CookieUpdater(config_path)
        print("Iniciando atualização de cookies...")
        updater.update_servers_cookies()
        print("Cookies atualizados com sucesso!")
    except Exception as e:
        print(f"Erro ao atualizar cookies: {str(e)}")

def main():
    """Função principal da interface de linha de comando."""
    parser = argparse.ArgumentParser(description='ShadowReq - Gerenciador de requisições através de servidores intermediários')
    subparsers = parser.add_subparsers(dest='command', help='Comandos disponíveis')

    # Comando update-cookies
    update_parser = subparsers.add_parser('update-cookies', help='Atualiza os cookies dos servidores')
    update_parser.add_argument('--config', default='servers.json', help='Arquivo de configuração dos servidores')

    args = parser.parse_args()

    if args.command == 'update-cookies':
        update_cookies(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
