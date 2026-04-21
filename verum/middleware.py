import json
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from .core import seal, bind, export


class VerumMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next) -> Response:
        body = await request.body()

        if body:
            source_id = f"{request.method}:{request.url.path}"
            data = body.decode("utf-8", errors="replace")
            s = seal(data=data, source_id=source_id)
            request.state.verum_seal = s
        else:
            request.state.verum_seal = None

        response = await call_next(request)

        if request.state.verum_seal is not None:
            s = request.state.verum_seal
            decision = f"{response.status_code}"
            receipt = bind(seal=s, decision=decision)
            request.state.verum_receipt = receipt
            response.headers["X-Verum-Fingerprint"] = s["fingerprint"]
            response.headers["X-Verum-Chain"] = receipt["chain"]
            response.headers["X-Verum-Source"] = s["source_id"]

        return response
