from fastapi import APIRouter, Request, HTTPException, Header
import hmac
import hashlib
import base64
import os

router = APIRouter()

# Retrieve the Shopify shared secret from environment variables
SHOPIFY_SHARED_SECRET = 'c6cceed16f61f22e4d62ba9379da55e8'

def verify_shopify_hmac(data: bytes, hmac_header: str, secret: str) -> bool:
    # Generate HMAC using the secret and the request body
    hash = hmac.new(secret.encode('utf-8'), data, hashlib.sha256).digest()
    computed_hmac = base64.b64encode(hash).decode('utf-8')
    return hmac_header == computed_hmac

@router.post("/api/submit")
async def shopify_webhook(request: Request, x_shopify_hmac_sha256: str = Header(None)):
    body = await request.body()
    if not verify_shopify_hmac(body, x_shopify_hmac_sha256, SHOPIFY_SHARED_SECRET):
        raise HTTPException(status_code=401, detail="Unauthorized request")

    data = await request.json()
    return {"message": "Webhook received and verified successfully"}
