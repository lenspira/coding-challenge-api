from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables from a .env file
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],
    allow_origin_regex=r"http://.+\.ecs\..+\.amazonaws\.com",  # Matches any ECS-based URL
    allow_credentials=True,
    allow_methods=["POST"],  # Restrict to POST only
    allow_headers=["*"],
)

# Set OpenAI API key
chatbot_api_key = os.getenv("OPENAI_API_KEY")
if not chatbot_api_key:
    raise Exception("OPENAI_API_KEY is not set in the environment variables.")

client = OpenAI(api_key=chatbot_api_key)

# Define the request model
class ChatRequest(BaseModel):
    question: str

# Define the response model
class ChatResponse(BaseModel):
    answer: str

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Endpoint to take a user's question and return a response from OpenAI GPT-4.
    """
    try:
        # Call the OpenAI API with the new interface
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant in the field of business insurance."},
                {"role": "user", "content": request.question},
            ],
            max_tokens=200,  # Limit response length
            temperature=0.7,  # Adjust creativity
        )

        # Extract GPT-4's response
        answer = response.choices[0].message.content.strip()
        return {"answer": answer}

    except OpenAI.OpenAIError as e:
        # Handle OpenAI-specific errors
        raise HTTPException(status_code=500, detail=f"OpenAI API Error: {str(e)}")
    except Exception as e:
        # Handle other unexpected errors
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
