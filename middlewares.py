from starlette.datastructures import URL
from starlette.responses import RedirectResponse
from starlette.types import ASGIApp, Receive, Scope, Send

from services import get_least_requested_host, update_host_requests


class NitterRedirectMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        host = get_least_requested_host()
        scheme, netloc = host.split("://")
        url = URL(scope=scope).replace(netloc=netloc, scheme=scheme)
        response = RedirectResponse(url, status_code=307)
        await response(scope, receive, send)
        update_host_requests(host)
