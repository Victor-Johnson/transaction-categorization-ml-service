FROM python:3.11-slim

WORKDIR /app 

ENV PYTHONDONTWRITEBYTECODE=1 
ENV PYTHONBUFFERED=1

RUN pip install --no-cache-dir -U pip 
COPY requirements.txt  .
RUN pip install --no-cache-dir -r requirements.txt

## Copying the model artifacts 
COPY app ./app 
COPY artifacts ./artifacts

EXPOSE 8000
CMD ["python","-m","uvicorn", "app.api:app" ,"--host", "0.0.0.0", "--port", "8000" ]

