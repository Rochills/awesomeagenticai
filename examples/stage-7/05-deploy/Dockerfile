FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY starter.py starter_anthropic.py ./

# Default to Ollama path — override APP_MODULE for Anthropic
ENV APP_MODULE=starter:app

EXPOSE 8000

CMD ["sh", "-c", "uvicorn ${APP_MODULE} --host 0.0.0.0 --port 8000"]

# Build:
#   docker build -t agent-api .
# Run (Ollama path; needs ollama on host):
#   docker run -p 8000:8000 -e OLLAMA_API_BASE=http://host.docker.internal:11434/v1 agent-api
# Run (Anthropic path):
#   docker run -p 8000:8000 -e APP_MODULE=starter_anthropic:app -e ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY agent-api
