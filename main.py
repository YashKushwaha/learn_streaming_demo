from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from pathlib import Path


app = FastAPI()

# Allow all CORS origins (for dev/demo use)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/echo")
async def echo_stream(message: str):
    async def word_stream():
        for word in message.split():
            yield word + " "
            await asyncio.sleep(0.3)  # simulate delay
    return StreamingResponse(word_stream(), media_type="text/plain")

if __name__ == "__main__":
    import uvicorn
    app_path = Path(__file__).resolve().with_suffix('').name  # gets filename without .py
    uvicorn.run(f"{app_path}:app", host="localhost", port=8000, reload=True)