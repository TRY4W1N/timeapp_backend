import asyncio

import uvicorn
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from src.infrastructure.config import ConfigBase
from src.infrastructure.di.container import build_container
from src.presentation.http.additional.exception import setup_exception_handlers
from src.presentation.http.additional.middlewares import setup_middlewares
from src.presentation.http.controllers.router import router


def create_app(config: ConfigBase):
    app = FastAPI(
        name=config.APP_NAME,
        debug=config.DEBUG,
        version="1.0.0",
        default_response_class=ORJSONResponse,
    )
    app.include_router(router)
    setup_middlewares(app)
    setup_exception_handlers(app)
    return app


async def run_app():
    container = build_container()
    config = await container.get(ConfigBase, component="CONFIG")
    app = create_app(config=config)
    setup_dishka(container, app)
    uvconfig = uvicorn.Config(
        app,
        host=config.APP_HOST,
        port=config.APP_PORT,
        reload=config.DEBUG,
    )
    server = uvicorn.Server(uvconfig)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(run_app())
