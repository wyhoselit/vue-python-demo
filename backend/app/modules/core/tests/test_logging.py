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
            mock_logger.addHandler.assert_called()
            assert mock_logger.addHandler.call_count == 2
            mock_logger.setLevel.assert_called_once_with(logging.INFO)
    
    def test_setup_logging_adds_handlers(self):
        with patch('app.modules.core.logging.logging.StreamHandler') as mock_stream_handler_class, \
             patch('app.modules.core.logging.logging.FileHandler') as mock_file_handler_class:
            
            mock_stream_handler = MagicMock()
            mock_file_handler = MagicMock()
            mock_stream_handler_class.return_value = mock_stream_handler
            mock_file_handler_class.return_value = mock_file_handler
            
            with patch('app.modules.core.logging.logging.getLogger') as mock_get_logger:
                mock_logger = MagicMock()
                mock_get_logger.return_value = mock_logger
                
                setup_logging()
                
                mock_stream_handler_class.assert_called_once()
                mock_file_handler_class.assert_called_once()
                mock_stream_handler.setFormatter.assert_called_once()
                mock_file_handler.setFormatter.assert_called_once()
    
    def test_setup_logging_sets_json_formatter(self):
        with patch('app.modules.core.logging.jsonlogger.JsonFormatter') as mock_formatter_class:
            mock_formatter = MagicMock()
            mock_formatter_class.return_value = mock_formatter
            
            with patch('app.modules.core.logging.logging.StreamHandler') as mock_handler_class:
                mock_handler = MagicMock()
                mock_handler_class.return_value = mock_handler
                
                with patch('app.modules.core.logging.logging.FileHandler') as mock_file_handler_class:
                    mock_file_handler = MagicMock()
                    mock_file_handler_class.return_value = mock_file_handler
                
                    with patch('app.modules.core.logging.logging.getLogger') as mock_get_logger:
                        mock_logger = MagicMock()
                        mock_get_logger.return_value = mock_logger
                        
                        setup_logging()
                        
                        # formatter is instantiated once, set on both handlers
                        assert mock_formatter_class.call_count == 1
                        assert mock_handler.setFormatter.called
                        assert mock_file_handler.setFormatter.called