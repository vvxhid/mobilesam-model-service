FROM python:3.11

WORKDIR /usr/src/streamlit_app

COPY ../requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501