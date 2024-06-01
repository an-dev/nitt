from fastapi import FastAPI

from middlewares import NitterRedirectMiddleware

app = FastAPI(openapi_url=None)

app.add_middleware(NitterRedirectMiddleware)
