from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from chat import *

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"], # Explicitly allow your website
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

origins = [
    "http://localhost:5500",
    "http://127.0.0.1:5500",
    "https://edubuddy-chatbot.onrender.com",
    # "https://your-domain.com",  # Production domain
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def main():
    return {"message": "CORS is configured!"}

class PredictRequest(BaseModel):
    message: str = ""
    
@app.get("/cron-job")
async def cron_job():
    return {"message": "Cron job executed successfully!"}

@app.post("/predict")
async def predict(data: PredictRequest):
    text = data.message
    response = chat(text)
    return {"answer": response}

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=5000)

