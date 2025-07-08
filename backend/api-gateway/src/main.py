from fastapi import FastAPI, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRoute
import httpx
from backend.api_gateway.config.settings import gateway_settings # You'd create this
from backend.shared.constants.api_constants import API_PREFIX # From shared

app = FastAPI(title="API Gateway", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], # Allow your frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.api_route(f"{API_PREFIX}/auth/{{path:path}}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_auth(path: str, request: Request):
    async with httpx.AsyncClient() as client:
        url = f"{gateway_settings.auth_service_base_url}/{path}"
        headers = {k: v for k, v in request.headers.items() if k.lower() not in ["host", "content-length"]}
        # Handle forms/JSON
        if request.method in ["POST", "PUT"]:
            try:
                json_data = await request.json()
                response = await client.request(
                    request.method, url, headers=headers, json=json_data
                )
            except Exception: # Not JSON, might be form data
                form_data = await request.form()
                response = await client.request(
                    request.method, url, headers=headers, data=dict(form_data)
                )
        else:
            response = await client.request(
                request.method, url, headers=headers
            )
        return Response(content=response.content, status_code=response.status_code, media_type=response.headers.get("content-type"))

@app.api_route(f"{API_PREFIX}/deepface/{{path:path}}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_deepface(path: str, request: Request):
    async with httpx.AsyncClient() as client:
        url = f"{gateway_settings.deepface_service_base_url}/{path}"
        headers = {k: v for k, v in request.headers.items() if k.lower() not in ["host", "content-length"]}
        try:
            json_data = await request.json()
            response = await client.request(
                request.method, url, headers=headers, json=json_data
            )
        except Exception: # Not JSON
            form_data = await request.form()
            response = await client.request(
                request.method, url, headers=headers, data=dict(form_data)
            )
        return Response(content=response.content, status_code=response.status_code, media_type=response.headers.get("content-type"))

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "API Gateway is running!"}