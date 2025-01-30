import requests
import json
import random
from typing import Optional, Dict, Any, Union
import urllib3
from .logger import ShadowLogger

# Desabilitar avisos de SSL não verificado
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class ShadowReq:
    def __init__(self, server_config_file: str = 'servers.json', 
                 timeout: Optional[Union[float, tuple]] = None,
                 enable_logging: bool = False,
                 log_file: Optional[str] = None):
        """
        Inicializa o ShadowReq com as configurações do servidor.
        
        Args:
            server_config_file (str): Caminho para o arquivo de configuração dos servidores
            timeout (float, tuple, optional): Timeout para as requisições em segundos.
                                           Pode ser um número (timeout total) ou uma tupla (connect timeout, read timeout)
            enable_logging (bool): Se True, ativa o logging para um arquivo
            log_file (str, optional): Caminho para o arquivo de log
        """
        # Configurar logging
        self.logger = ShadowLogger()
        self.logger.setup(enabled=enable_logging, log_file=log_file)
        
        # Carregar configuração
        try:
            with open(server_config_file, 'r') as file:
                self.servers = json.load(file)
        except Exception as e:
            self.logger.error(f"Erro ao carregar arquivo de configuração: {str(e)}")
            raise
            
        self.timeout = timeout or (5, 30)  # Default: 5s para conexão, 30s para leitura
        self.server_names = list(self.servers.keys())
        self._rotate_server()  # Seleciona um servidor aleatório inicial

    def _rotate_server(self):
        """
        Seleciona um servidor aleatório da lista de servidores disponíveis.
        Atualiza o servidor atual e seus headers.
        """
        server_name = random.choice(self.server_names)
        self.current_server = self.servers[server_name]
        self.base_url = self.current_server['urls'][0]
        self.headers = self.current_server['headers']
        self.logger.info(f"Usando servidor: {server_name}")

    def _make_request(self, method: str, url: str, **kwargs) -> requests.Response:
        """
        Faz a requisição através do servidor intermediário.
        
        Args:
            method (str): Método HTTP (GET, POST, PUT, DELETE)
            url (str): URL do destino
            **kwargs: Argumentos adicionais para a requisição
        
        Returns:
            requests.Response: Objeto de resposta
        
        Raises:
            requests.exceptions.Timeout: Se a requisição exceder o timeout
            requests.exceptions.RequestException: Para outros erros de requisição
        """
        # Rotacionar servidor antes de cada requisição
        self._rotate_server()
        
        # Preparar dados para enviar ao servidor PHP
        params = {}
        
        # Se tiver dados no body da requisição
        if 'data' in kwargs and kwargs['data']:
            params.update(kwargs['data'])
        
        # Se tiver query params
        if 'params' in kwargs and kwargs['params']:
            params.update(kwargs['params'])

        # Pegar o timeout específico desta requisição ou usar o default da classe
        timeout = kwargs.pop('timeout', self.timeout)

        # Preparar payload conforme esperado pelo servidor PHP
        payload = {
            'url': url,
            'method': method.upper(),
            'params': params
        }

        self.logger.debug(f"Fazendo requisição {method} para {url}")
        
        try:
            # Fazer requisição para o servidor PHP
            response = requests.post(
                f"{self.base_url}/api.php",
                headers=self.headers,
                json=payload,
                verify=False,
                timeout=timeout
            )

            # Extrair a resposta real do wrapper do servidor
            if response.status_code == 200:
                try:
                    result = response.json()
                    # Criar um novo objeto Response com os dados do servidor
                    new_response = requests.Response()
                    new_response.status_code = result.get('status', 500)
                    if 'response' in result:
                        new_response._content = json.dumps(result['response']).encode('utf-8')
                    self.logger.info(f"Requisição completada: Status {new_response.status_code}")
                    return new_response
                except Exception as e:
                    self.logger.error(f"Erro ao processar resposta: {str(e)}")
                    return response
            
            self.logger.warning(f"Servidor retornou status {response.status_code}")
            return response
            
        except Exception as e:
            self.logger.error(f"Erro na requisição: {str(e)}")
            raise

    def get(self, url: str, timeout: Optional[Union[float, tuple]] = None, **kwargs) -> requests.Response:
        """
        Faz uma requisição GET através do servidor.
        
        Args:
            url (str): URL do destino
            timeout (float, tuple, optional): Timeout específico para esta requisição
            **kwargs: Argumentos adicionais para a requisição
        
        Returns:
            requests.Response: Objeto de resposta
        """
        if timeout:
            kwargs['timeout'] = timeout
        return self._make_request('GET', url, **kwargs)

    def post(self, url: str, data: Optional[Dict[str, Any]] = None, timeout: Optional[Union[float, tuple]] = None, **kwargs) -> requests.Response:
        """
        Faz uma requisição POST através do servidor.
        
        Args:
            url (str): URL do destino
            data (dict, optional): Dados a serem enviados no corpo da requisição
            timeout (float, tuple, optional): Timeout específico para esta requisição
            **kwargs: Argumentos adicionais para a requisição
        
        Returns:
            requests.Response: Objeto de resposta
        """
        if timeout:
            kwargs['timeout'] = timeout
        return self._make_request('POST', url, data=data, **kwargs)

    def put(self, url: str, data: Optional[Dict[str, Any]] = None, timeout: Optional[Union[float, tuple]] = None, **kwargs) -> requests.Response:
        """
        Faz uma requisição PUT através do servidor.
        
        Args:
            url (str): URL do destino
            data (dict, optional): Dados a serem enviados no corpo da requisição
            timeout (float, tuple, optional): Timeout específico para esta requisição
            **kwargs: Argumentos adicionais para a requisição
        
        Returns:
            requests.Response: Objeto de resposta
        """
        if timeout:
            kwargs['timeout'] = timeout
        return self._make_request('PUT', url, data=data, **kwargs)

    def delete(self, url: str, timeout: Optional[Union[float, tuple]] = None, **kwargs) -> requests.Response:
        """
        Faz uma requisição DELETE através do servidor.
        
        Args:
            url (str): URL do destino
            timeout (float, tuple, optional): Timeout específico para esta requisição
            **kwargs: Argumentos adicionais para a requisição
        
        Returns:
            requests.Response: Objeto de resposta
        """
        if timeout:
            kwargs['timeout'] = timeout
        return self._make_request('DELETE', url, **kwargs)