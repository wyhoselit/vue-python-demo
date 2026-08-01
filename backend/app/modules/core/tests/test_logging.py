import pytest
import logging
from unittest.mock import patch, MagicMock
from app.modules.core.logging import setup_logging


class TestSetupLogging:
    def test_setup_logging_configures_logger(self):
        with patch.object(logging, 'getLogger') as mock_get_logger:
            mock_logger = MagicMock()
            mock_get_logger.return_value = mock_logger
            
            setup_logging()
            
            mock_get_logger.assert_called_once()
            mock_logger.addHandler.assert_called_once()
            mock_logger.setLevel.assert_called_once_with(logging.INFO)
    
    def test_setup_logging_adds_stream_handler(self):
        with patch('app.modules.core.logging.logging.StreamHandler') as mock_handler_class:
            mock_handler = MagicMock()
            mock_handler_class.return_value = mock_handler
            
            with patch('app.modules.core.logging.logging.getLogger') as mock_get_logger:
                mock_logger = MagicMock()
                mock_get_logger.return_value = mock_logger
                
                setup_logging()
                
                mock_handler_class.assert_called_once()
                mock_handler.setFormatter.assert_called_once()
    
    def test_setup_logging_sets_json_formatter(self):
        with patch('app.modules.core.logging.jsonlogger.JsonFormatter') as mock_formatter_class:
            mock_formatter = MagicMock()
            mock_formatter_class.return_value = mock_formatter
            
            with patch('app.modules.core.logging.logging.StreamHandler') as mock_handler_class:
                mock_handler = MagicMock()
                mock_handler_class.return_value = mock_handler
                
                with patch('app.modules.core.logging.logging.getLogger') as mock_get_logger:
                    mock_logger = MagicMock()
                    mock_get_logger.return_value = mock_logger
                    
                    setup_logging()
                    
                    mock_formatter_class.assert_called_once()
                    mock_handler.setFormatter.assert_called_once_with(mock_formatter)