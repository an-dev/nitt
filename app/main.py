import os

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from .middlewares import NitterRedirectMiddleware
from .services import get_valid_instances

app = FastAPI(openapi_url=None)
app.add_middleware(NitterRedirectMiddleware)

templates = Jinja2Templates(directory="app/templates")


@app.get("/", response_class=HTMLResponse)
async def main(request: Request) -> HTMLResponse:
    instances = get_valid_instances()
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "instance_count": len(instances),
            "BASE_URL": os.environ["BASE_URL"],
        },
    )
