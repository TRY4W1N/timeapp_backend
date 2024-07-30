from collections.abc import Awaitable, Callable
from uuid import uuid4

from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette_exporter import PrometheusMiddleware, handle_metrics

from src.infrastructure.config import ConfigBase, EnvType, AppEnvType


def set_prometheus_labels(config: ConfigBase) -> dict:
    labels = {
        "APP_PORT": config.APP_PORT,
        "APP_HOST": config.APP_HOST,
        "DEBUG": config.DEBUG,
        "APP_ENV": config.APP_ENV,
    }
    return labels


async def set_request_id_middleware(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    request.state.request_id = uuid4()
    response = await call_next(request)
    return response


def setup_middlewares(app: FastAPI, config: ConfigBase) -> None:
    app.add_middleware(BaseHTTPMiddleware, dispatch=set_request_id_middleware)
    if EnvType.DOCKER.value == config.ENV and AppEnvType.PROD.value == config.APP_ENV:
        app.router.add_route(path="/metrics", endpoint=handle_metrics)
        app.add_middleware(
            PrometheusMiddleware,
            app_name=config.APP_NAME,
            labels=set_prometheus_labels(config=config),
            prefix="starlette_exporter",
            always_use_int_status=False,
        )
