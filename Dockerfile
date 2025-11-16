FROM python:3.11-slim
WORKDIR /app

COPY requirements.txt .
RUN python3 -m pip install --upgrade uv
RUN uv pip install --system -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
