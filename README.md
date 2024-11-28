# Chatbot Backend API with Python FastAPI

This repository contains a FastAPI-based backend for a chatbot application that integrates with OpenAI's GPT-4 API. It receives user queries from the frontend, processes them using GPT-4, and returns intelligent responses. The backend is containerized using Docker and is deployable to AWS ECS.

---

## Features

- Built with **FastAPI** for performance and modern features.
- Integration with **OpenAI GPT-4 API** for advanced natural language understanding.
- Secure CORS configuration to restrict access to specific frontend domains.
- Fully configurable using environment variables.
- Dockerized for ease of deployment and scalability.

---

## Prerequisites

### 1. Install Required Tools
- [Python 3.10](https://www.python.org/downloads/)
- [Docker](https://www.docker.com/products/docker-desktop)
- [AWS CLI](https://aws.amazon.com/cli/)
- [OpenAI API Key](https://platform.openai.com/)

### 2. Environment Variables
Ensure you have a `.env` file in the project root with the following content:
```
OPENAI_API_KEY=your_openai_api_key
FRONTEND_URLS=your_localhost_url_and_your_frontend_domain
```

## Installation
1. Clone the repository:
   ```
   git clone https://github.com/lenspira/coding-challenge-api.git
   cd coding-challenge-api
   ```
2. Create a visual environment and activate it:
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run the application locally:
   ```
   uvicorn main:app --reload
   ```

## API Endpoints
```/chat``` - POST
Description: Accepts a user's question and returns a response from GPT-4.

Request Body:
```
{
  "question": "What is the capital of France?"
}
```
Response:
```
{
  "answer": "The capital of France is Paris."
}
```

## CORS Configuration
Make sure the allow_origins in main.py restrict API access to your frontend domains:
```
allow_origins=["http://localhost:3000", "https://your-frontend-domain.com"]
```

## Deployment
### Using Docker
1. Build the Docker image:
   ```
   docker build -t chatbot-backend .
   ```
2. Run the Docker container:
   ```
   docker run -p 8000:8000 --env-file .env chatbot-backend
   ```
### Deploy to AWS ECS
1. Push the Docker image to AWS ECR:
   ```
   aws ecr create-repository --repository-name chatbot-backend
   docker tag chatbot-backend:latest <aws_account_id>.dkr.ecr.<region>.amazonaws.com/chatbot-backend:latest
   docker push <aws_account_id>.dkr.ecr.<region>.amazonaws.com/chatbot-backend:latest
   ```
2. Create an ECS cluster, task definition, and service to deploy the container.
   - Add an environment variable for your OpenAI API key to the container;
   - Ensure proper IAM roles and security groups are configured.

## Logging and Monitoring
Logs can be viewed in AWS CloudWatch or locally in Docker using:
```
docker logs <container-id>
```

## Security
- Store your OpenAI API key in a ```.env``` file or AWS Secrets Manager.
- Restrict public access to your security groups.
- Use HTTPS for secure communication.

## Acknowledgements
- Python FastAPI
- OpenAI GPT-4
- Docker
- AWS ECR and ECS
