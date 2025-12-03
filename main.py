from fastapi import FastAPI,Request
from fastapi.responses import PlainTextResponse, JSONResponse


app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome"}


@app.get("/incoming-call")
def incoming_call(call_id: str, caller_name: str):
    print(call_id, caller_name)
    return {
        "call_id": call_id,
        "caller_name": caller_name
    }


@app.post("/webhook")
async def webhook(request:Request):
    data = await request.json()
    print(data)
    return {"data": data}



# nlyas webhook verification endpoint
@app.get("/nylas/webhook")
async def verify_webhook(challenge: str = ""):
    """
    Nylas sends GET ?challenge=xxxx to verify webhook.
    """
    if not challenge:
        return JSONResponse({"error": "Missing challenge"}, status_code=400)
    print(f"✅ Nylas webhook verified: {challenge}")
    return PlainTextResponse(challenge, status_code=200)