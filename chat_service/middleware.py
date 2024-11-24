from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, Response
import time
import logging
import json


logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        method = request.method
        path = request.url.path

        headers = dict(request.headers)
        headers_info = json.dumps(headers, indent=2)  # 格式化为JSON格式

        try:
            body = await request.json()
        except Exception:
            body = None
        body_info = json.dumps(body, indent=2) if body else "No body"

        start_time = time.perf_counter()

        logger.info(f"INFO: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info(f"Request Method: {method}")
        logger.info(f"Request Path: {path}")
        logger.info(f"Request Headers: {headers_info}")
        logger.info(f"Request Body: {body_info}")

        try:
            response = await call_next(request)
        except Exception as e:
            logger.error(f"Error in {method} {path}: {str(e)}")
            raise e

        process_time = (time.perf_counter() - start_time) * 1000
        response.headers["X-Process-Time"] = f"{process_time:.2f}ms"

        status_code = response.status_code
        logger.info(f"Response Status: {status_code}")
        logger.info(f"Response Time: {process_time:.2f}ms")

        return response