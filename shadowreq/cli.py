"""
Interface de linha de comando para o ShadowReq.
"""

import argparse
import os
from .cookie_updater import CookieUpdater
from .logger import ShadowLogger

def update_cookies(args):
    """Atualiza os cookies dos servidores."""
    config_path = os.path.abspath(args.config)
    
    # Configurar logging
    logger = ShadowLogger()
    logger.setup(enabled=args.enable_logging, log_file=args.log_file)
    logger.info(f"Usando arquivo de configuração: {config_path}")
    
    if not os.path.exists(config_path):
        logger.error(f"Erro: Arquivo {config_path} não encontrado")
        print(f"Erro: Arquivo {config_path} não encontrado")
        return
    
    try:
        updater = CookieUpdater(config_path, enable_logging=args.enable_logging, log_file=args.log_file)
        logger.info("Iniciando atualização de cookies...")
        print("Iniciando atualização de cookies...")
        
        updater.update_servers_cookies()
        
        logger.info("Cookies atualizados com sucesso!")
        print("Cookies atualizados com sucesso!")
        
    except Exception as e:
        error_msg = f"Erro ao atualizar cookies: {str(e)}"
        logger.error(error_msg)
        print(error_msg)

def main():
    """Função principal da interface de linha de comando."""
    parser = argparse.ArgumentParser(description='ShadowReq - Gerenciador de requisições através de servidores intermediários')
    subparsers = parser.add_subparsers(dest='command', help='Comandos disponíveis')

    # Comando update-cookies
    update_parser = subparsers.add_parser('update-cookies', help='Atualiza os cookies dos servidores')
    update_parser.add_argument('--config', default='servers.json', help='Arquivo de configuração dos servidores')
    update_parser.add_argument('--enable-logging', action='store_true', help='Ativa o logging para arquivo')
    update_parser.add_argument('--log-file', help='Caminho para o arquivo de log')

    args = parser.parse_args()

    if args.command == 'update-cookies':
        update_cookies(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
