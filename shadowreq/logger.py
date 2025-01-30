"""
Módulo de logging para o ShadowReq.
"""

import logging
import os
from datetime import datetime
from typing import Optional

class ShadowLogger:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ShadowLogger, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
            
        self.logger = None
        self._initialized = True
    
    def setup(self, enabled: bool = False, log_file: Optional[str] = None, level: int = logging.INFO):
        """
        Configura o logger.
        
        Args:
            enabled (bool): Se True, ativa o logging
            log_file (str, optional): Caminho para o arquivo de log. 
                                    Se None, usa 'shadowreq_{data}.log' no diretório atual
            level (int): Nível de logging (default: logging.INFO)
        """
        if not enabled:
            self.logger = None
            return
            
        # Criar logger
        self.logger = logging.getLogger('shadowreq')
        self.logger.setLevel(level)
        
        # Se já tiver handlers, limpa para não duplicar
        if self.logger.handlers:
            self.logger.handlers.clear()
        
        # Definir arquivo de log padrão se não fornecido
        if not log_file:
            date_str = datetime.now().strftime('%Y%m%d')
            log_file = f'shadowreq_{date_str}.log'
        
        # Criar diretório se não existir
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # Configurar handler de arquivo
        file_handler = logging.FileHandler(log_file)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
    
    def info(self, message: str):
        """Registra uma mensagem de nível INFO."""
        if self.logger:
            self.logger.info(message)
    
    def error(self, message: str):
        """Registra uma mensagem de nível ERROR."""
        if self.logger:
            self.logger.error(message)
    
    def debug(self, message: str):
        """Registra uma mensagem de nível DEBUG."""
        if self.logger:
            self.logger.debug(message)
    
    def warning(self, message: str):
        """Registra uma mensagem de nível WARNING."""
        if self.logger:
            self.logger.warning(message)
