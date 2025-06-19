from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
import asyncio

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "chat_endpoint": "/echo"
    })

async def llm_call(message):
    for word in message.split():
        yield word + " "
        await asyncio.sleep(0.3)  # simulate delay

@app.post("/echo")
async def echo_stream(request: Request):
    data = await request.json()
    message = data.get("message", "")
    dummy_llm_response = llm_call(message)
    return StreamingResponse(dummy_llm_response, media_type="text/plain")


if __name__ == "__main__":
    import uvicorn
    app_path = Path(__file__).resolve().with_suffix('').name  # gets filename without .py
    uvicorn.run(f"{app_path}:app", host="localhost", port=8000, reload=True)