import uuid
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from starlette.requests import Request
from starlette.responses import Response
from app.core.middleware import RequestIDMiddleware


class TestRequestIDMiddleware:
    def get_middleware(self):
        mock_app = MagicMock()
        return RequestIDMiddleware(mock_app)

    @pytest.mark.asyncio
    async def test_dispatch_sets_request_id_from_header(self):
        middleware = self.get_middleware()
        request_id = str(uuid.uuid4())
        
        mock_request = MagicMock(spec=Request)
        mock_request.headers = {"X-Request-ID": request_id}
        mock_request.state = MagicMock()
        
        mock_response = MagicMock(spec=Response)
        mock_response.headers = {}
        
        call_next = AsyncMock(return_value=mock_response)
        
        await middleware.dispatch(mock_request, call_next)
        
        assert mock_request.state.request_id == request_id
        assert mock_response.headers["X-Request-ID"] == request_id

    @pytest.mark.asyncio
    async def test_dispatch_generates_request_id_when_missing(self):
        middleware = self.get_middleware()
        
        mock_request = MagicMock(spec=Request)
        mock_request.headers = {}
        mock_request.state = MagicMock()
        
        mock_response = MagicMock(spec=Response)
        mock_response.headers = {}
        
        call_next = AsyncMock(return_value=mock_response)
        
        await middleware.dispatch(mock_request, call_next)
        
        assert mock_request.state.request_id is not None
        assert mock_response.headers["X-Request-ID"] == mock_request.state.request_id

    @pytest.mark.asyncio
    async def test_dispatch_calls_call_next(self):
        middleware = self.get_middleware()
        
        mock_request = MagicMock(spec=Request)
        mock_request.headers = {}
        mock_request.state = MagicMock()
        
        mock_response = MagicMock(spec=Response)
        mock_response.headers = {}
        
        call_next = AsyncMock(return_value=mock_response)
        
        await middleware.dispatch(mock_request, call_next)
        
        call_next.assert_called_once_with(mock_request)