from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from typing import Optional
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config

router = APIRouter(prefix="/oidc", tags=["OpenID Connect"])

# Configure OAuth clients (e.g., Google, GitHub)
config = Config(".env")
oauth = OAuth(config)
oauth.register(
    name="google",
    client_id=settings.OAUTH2_CLIENT_ID,
    client_secret=settings.OAUTH2_CLIENT_SECRET,
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    authorize_params=None,
    access_token_url="https://oauth2.googleapis.com/token",
    refresh_token_url=None,
    client_kwargs={"scope": "openid email profile"},
)

@router.get("/login")
async def login(request: Request):
    redirect_uri = request.url_for("auth")
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/auth")
async def auth(request: Request):
    token = await oauth.google.authorize_access_token(request)
    user = await oauth.google.parse_id_token(request, token)
    # Store user in DB or session
    return {"user": user}