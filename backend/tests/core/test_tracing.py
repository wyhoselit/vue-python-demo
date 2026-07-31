import pytest
from unittest.mock import MagicMock, patch
from app.core.tracing import trace_execution


class TestTraceExecution:
    @pytest.mark.asyncio
    async def test_trace_execution_disabled(self):
        mock_db = MagicMock()
        mock_config = MagicMock()
        mock_config.enabled = False
        mock_db.query.return_value.filter_by.return_value.first.return_value = mock_config
    
        def get_db_generator():
            yield mock_db
    
        with patch('app.core.tracing.get_db', return_value=get_db_generator()):
            async def dummy_func():
                return "success"
    
            wrapper = trace_execution(dummy_func)
            result = await wrapper()
            assert result == "success"
            
            # Since get_db() is called as a generator in trace_execution
            # wrapper() calls it, and 'db' is assigned. 
            # The test should verify if logic correctly calls db.query
            assert mock_db.query.called
            assert mock_db.commit.call_count == 0
    
    @pytest.mark.asyncio
    async def test_trace_execution_enabled(self):
        mock_db = MagicMock()
        mock_config = MagicMock()
        mock_config.enabled = True
        mock_db.query.return_value.filter_by.return_value.first.return_value = mock_config
    
        async def dummy_func():
            return "success"
    
        def get_db_generator():
            yield mock_db
    
        with patch('app.core.tracing.get_db', return_value=get_db_generator()):
            wrapper = trace_execution(dummy_func)
            result = await wrapper()
            assert result == "success"
            
            assert mock_db.query.called
            assert mock_db.add.called
            assert mock_db.commit.called
    
    @pytest.mark.asyncio
    async def test_trace_execution_no_config(self):
        mock_db = MagicMock()
        mock_db.query.return_value.filter_by.return_value.first.return_value = None
    
        async def dummy_func():
            return "success"
    
        def get_db_generator():
            yield mock_db
    
        with patch('app.core.tracing.get_db', return_value=get_db_generator()):
            wrapper = trace_execution(dummy_func)
            result = await wrapper()
            assert result == "success"
            
            assert mock_db.query.called
            assert mock_db.commit.call_count == 0
    
    @pytest.mark.asyncio
    async def test_trace_execution_with_duration(self):
        mock_db = MagicMock()
        mock_config = MagicMock()
        mock_config.enabled = True
        mock_db.query.return_value.filter_by.return_value.first.return_value = mock_config
    
        def get_db_generator():
            yield mock_db
    
        with patch('app.core.tracing.get_db', return_value=get_db_generator()):
            with patch('app.core.tracing.time.perf_counter') as mock_time:
                mock_time.side_effect = [0.0, 1.5]
    
                async def dummy_func():
                    return "success"
    
                wrapper = trace_execution(dummy_func)
                result = await wrapper()
                assert result == "success"
                
                assert mock_time.call_count >= 2
                assert mock_db.add.called
                assert mock_db.commit.called

