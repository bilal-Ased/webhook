from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome"}


@app.get("/incoming-call")
def incoming_call(call_id: str, caller_name: str):
    print(call_id, caller_name)
    return {"status": "ok"}
