from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

# Allow React frontend (Vite runs on various ports)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:8081", "http://localhost:8082", "http://localhost:8083", "http://127.0.0.1:8081", "http://127.0.0.1:8082", "http://127.0.0.1:8083", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

HUGGING_FACE_TOKEN = os.getenv("HUGGING_FACE_TOKEN")

if not HUGGING_FACE_TOKEN:
    print("WARNING: HUGGING_FACE_TOKEN not found in environment variables!")

# Use a model that supports text generation via free inference API
MODEL_NAME = "Qwen/Qwen2-0.5B-Instruct"
API_URL = f"https://api-inference.huggingface.co/models/{MODEL_NAME}"

class QuestionRequest(BaseModel):
    question: str
    transcript: str

def query_huggingface(payload):
    headers = {"Authorization": f"Bearer {HUGGING_FACE_TOKEN}"}
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

@app.post("/ask-ai")
async def ask_ai(request: QuestionRequest):
    if not HUGGING_FACE_TOKEN:
        raise HTTPException(status_code=500, detail="Hugging Face token not configured. Please set HUGGING_FACE_TOKEN in backend/.env file.")
    
    # Format prompt for Qwen model
    prompt = f"""<|im_start|>system
You are a helpful assistant that answers questions about video content.<|im_end|>
<|im_start|>user
Based on this video transcript:
{request.transcript}

Answer this question:
{request.question}<|im_end|>
<|im_start|>assistant
"""
    
    try:
        output = query_huggingface({
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 500,
                "temperature": 0.7,
                "do_sample": True
            }
        })
        
        # Handle the response format
        if isinstance(output, dict) and 'error' in output:
            raise HTTPException(status_code=500, detail=f"Hugging Face API error: {output['error']}")
        
        # Extract the generated text
        if isinstance(output, list) and len(output) > 0:
            generated_text = output[0].get('generated_text', '')
            # Remove the prompt from the response
            answer = generated_text[len(prompt):].strip() if generated_text else str(output)
        else:
            answer = str(output)
            
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Hugging Face API error: {str(e)}")

