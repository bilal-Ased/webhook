from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse, JSONResponse
import logging

app = FastAPI()

# Setup logging
logging.basicConfig(level=logging.INFO)

@app.get("/")
def read_root():
    return {"message": "Welcome"}

@app.get("/incoming-call")
def incoming_call(call_id: str, caller_name: str):
    logging.info(f"Incoming call: {call_id}, {caller_name}")
    return {"call_id": call_id, "caller_name": caller_name}

# Robust POST webhook handler
@app.post("/nylas/webhook")
async def nylas_webhook(request: Request):
    try:
        data = await request.json()
    except Exception:
        # If payload is not JSON, fallback to raw body
        body_bytes = await request.body()
        logging.warning(f"Received non-JSON payload: {body_bytes}")
        return JSONResponse({"status": "error", "message": "Invalid JSON"}, status_code=400)

    logging.info(f"Nylas webhook data received: {data}")
    # Always return 200 OK to prevent 502 retries
    return JSONResponse({"status": "ok"}, status_code=200)

# Nylas webhook verification
@app.get("/nylas/webhook")
async def verify_webhook(challenge: str = ""):
    """
    Nylas sends GET ?challenge=xxxx to verify webhook.
    """
    if not challenge:
        return JSONResponse({"error": "Missing challenge"}, status_code=400)

    logging.info(f"✅ Nylas webhook verified: {challenge}")
    # Must return plain text exactly as challenge
    return PlainTextResponse(challenge, status_code=200)
