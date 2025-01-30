import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib.parse

class CookieUpdater:
    def __init__(self, servers_file='servers.json'):
        """
        Inicializa o atualizador de cookies.
        
        Args:
            servers_file (str): Caminho para o arquivo de configuração dos servidores
        """
        self.servers_file = servers_file
        self.setup_driver()
        
    def setup_driver(self):
        """Configura o driver do Chrome com as opções necessárias"""
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Executa em modo headless (sem interface gráfica)
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        # Inicializa o driver
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
        
    def get_api_url(self, base_url):
        """
        Constrói a URL da API a partir da URL base.
        
        Args:
            base_url (str): URL base do servidor
            
        Returns:
            str: URL completa da API
        """
        # Remove qualquer barra final se existir
        base_url = base_url.rstrip('/')
        
        # Adiciona o endpoint api.php
        api_url = f"{base_url}/api.php"
        
        return api_url
        
    def get_user_agent(self):
        """
        Obtém o User-Agent atual do navegador.
        
        Returns:
            str: User-Agent string
        """
        return self.driver.execute_script("return navigator.userAgent")
        
    def get_browser_info(self, url):
        """
        Acessa a URL e captura os cookies e User-Agent.
        
        Args:
            url (str): URL base do servidor
            
        Returns:
            tuple: (cookie, user_agent) ou (None, None) em caso de erro
        """
        try:
            # Constrói a URL da API
            api_url = self.get_api_url(url)
            print(f"Acessando {api_url}...")
            
            # Acessa a URL da API
            self.driver.get(api_url)
            
            # Espera um pouco para garantir que os cookies foram definidos
            time.sleep(2)
            
            # Captura o User-Agent
            user_agent = self.get_user_agent()
            print(f"User-Agent capturado: {user_agent}")
            
            # Captura todos os cookies
            cookies = self.driver.get_cookies()
            
            # Procura especificamente pelo cookie __test
            test_cookie = next(
                (cookie for cookie in cookies if cookie['name'] == '__test'),
                None
            )
            
            if test_cookie:
                cookie_value = f"__test={test_cookie['value']}"
                return cookie_value, user_agent
            else:
                print(f"Cookie __test não encontrado para {api_url}")
                return None, user_agent
                
        except Exception as e:
            print(f"Erro ao acessar {url}: {str(e)}")
            return None, None
            
    def update_servers_cookies(self):
        """Atualiza os cookies e User-Agent de todos os servidores no arquivo de configuração"""
        try:
            # Carrega a configuração atual
            with open(self.servers_file, 'r') as f:
                servers_data = json.load(f)
            
            # Para cada servidor
            for server_name, server_info in servers_data.items():
                if 'urls' in server_info and server_info['urls']:
                    url = server_info['urls'][0]
                    
                    # Captura o novo cookie e User-Agent
                    new_cookie, user_agent = self.get_browser_info(url)
                    
                    if new_cookie and user_agent:
                        print(f"Informações atualizadas para {server_name}:")
                        print(f"Cookie: {new_cookie}")
                        print(f"User-Agent: {user_agent}")
                        
                        # Atualiza o cookie
                        servers_data[server_name]['headers']['cookie'] = new_cookie
                        # Atualiza o User-Agent
                        servers_data[server_name]['headers']['user-agent'] = user_agent
                        # Atualiza também o referer para apontar para api.php
                        servers_data[server_name]['headers']['referer'] = self.get_api_url(url)
                    else:
                        print(f"Não foi possível atualizar as informações para {server_name}")
            
            # Salva as alterações
            with open(self.servers_file, 'w') as f:
                json.dump(servers_data, f, indent=4)
                
            print("Informações atualizadas com sucesso!")
            
        except Exception as e:
            print(f"Erro ao atualizar informações: {str(e)}")
        
        finally:
            self.driver.quit()
            
def main():
    updater = CookieUpdater()
    updater.update_servers_cookies()

if __name__ == "__main__":
    main()