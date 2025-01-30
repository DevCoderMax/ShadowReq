import requests
import json
from typing import Optional, Dict, Any, Union
import urllib3

# Desabilitar avisos de SSL não verificado
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class ShadowReq:
    def __init__(self, server_config_file: str = 'servers.json', timeout: Optional[Union[float, tuple]] = None):
        """
        Inicializa o ShadowReq com as configurações do servidor.
        
        Args:
            server_config_file (str): Caminho para o arquivo de configuração dos servidores
            timeout (float, tuple, optional): Timeout para as requisições em segundos.
                                           Pode ser um número (timeout total) ou uma tupla (connect timeout, read timeout)
        """
        with open(server_config_file, 'r') as file:
            self.servers = json.load(file)
        self.current_server = self.servers['server1']
        self.base_url = self.current_server['urls'][0]
        self.headers = self.current_server['headers']
        self.timeout = timeout or (5, 30)  # Default: 5s para conexão, 30s para leitura

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
                return new_response
            except:
                return response
        return response

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
            data (dict, optional): Dados para enviar no corpo da requisição
            timeout (float, tuple, optional): Timeout específico para esta requisição
            **kwargs: Argumentos adicionais para a requisição
        
        Returns:
            requests.Response: Objeto de resposta
        """
        kwargs['data'] = data or {}
        if timeout:
            kwargs['timeout'] = timeout
        return self._make_request('POST', url, **kwargs)

    def put(self, url: str, data: Optional[Dict[str, Any]] = None, timeout: Optional[Union[float, tuple]] = None, **kwargs) -> requests.Response:
        """
        Faz uma requisição PUT através do servidor.
        
        Args:
            url (str): URL do destino
            data (dict, optional): Dados para enviar no corpo da requisição
            timeout (float, tuple, optional): Timeout específico para esta requisição
            **kwargs: Argumentos adicionais para a requisição
        
        Returns:
            requests.Response: Objeto de resposta
        """
        kwargs['data'] = data or {}
        if timeout:
            kwargs['timeout'] = timeout
        return self._make_request('PUT', url, **kwargs)

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