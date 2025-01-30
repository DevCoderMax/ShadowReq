"""
Módulo para atualização automática de cookies usando Selenium.
"""

import json
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

class CookieUpdater:
    def __init__(self, server_config_file: str = 'servers.json'):
        """
        Inicializa o atualizador de cookies.
        
        Args:
            server_config_file (str): Caminho para o arquivo de configuração dos servidores
        """
        self.config_file = server_config_file
        self.driver = None

    def setup_driver(self):
        """Configura o driver do Chrome em modo headless."""
        if self.driver is not None:
            return

        print("Configurando Chrome em modo headless...")
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

    def get_cookie_and_useragent(self, url: str) -> tuple:
        """
        Obtém o cookie e User-Agent de um servidor.
        
        Args:
            url (str): URL do servidor
            
        Returns:
            tuple: (cookie, user_agent)
        """
        try:
            # Construir URL da API
            if not url.endswith('api.php'):
                if not url.endswith('/'):
                    url += '/'
                url += 'api.php'

            print(f"Acessando {url}...")
            self.driver.get(url)
            cookies = self.driver.get_cookies()
            user_agent = self.driver.execute_script("return navigator.userAgent")
            
            # Procurar pelo cookie __test
            test_cookie = next((cookie['value'] for cookie in cookies if cookie['name'] == '__test'), None)
            
            if not test_cookie:
                print(f"Aviso: Cookie __test não encontrado em {url}")
            
            return test_cookie, user_agent
        except Exception as e:
            print(f"Erro ao obter cookie de {url}: {str(e)}")
            return None, None

    def update_servers_cookies(self):
        """Atualiza os cookies e User-Agent no arquivo de configuração."""
        try:
            self.setup_driver()
            
            # Carregar configuração atual
            with open(self.config_file, 'r') as f:
                config = json.load(f)
            
            # Atualizar cada servidor
            for server_name, server_data in config.items():
                if isinstance(server_data, dict) and 'urls' in server_data:
                    url = server_data['urls'][0]  # Usar primeira URL
                    cookie, user_agent = self.get_cookie_and_useragent(url)
                    
                    if cookie and user_agent:
                        # Atualizar headers
                        if 'headers' not in server_data:
                            server_data['headers'] = {}
                        
                        server_data['headers']['cookie'] = f"__test={cookie}"
                        server_data['headers']['user-agent'] = user_agent
                        print(f"Atualizado {server_name} - Cookie: {cookie}")
            
            # Salvar configuração atualizada
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=4)
            
            print("Configuração atualizada com sucesso!")
        
        except Exception as e:
            print(f"Erro ao atualizar configuração: {str(e)}")
            raise
        
        finally:
            if self.driver:
                print("Fechando navegador...")
                self.driver.quit()

def main():
    """Função principal para executar a atualização de cookies."""
    updater = CookieUpdater()
    updater.update_servers_cookies()

if __name__ == '__main__':
    main()