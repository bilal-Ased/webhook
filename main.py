from fastapi import FastAPI,Request

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
