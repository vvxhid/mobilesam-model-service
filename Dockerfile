FROM python:3.11

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       git \
       libgl1-mesa-dev \
       libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/

COPY ./requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
