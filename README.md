# MobileSam segmentation with FastAPI & Streamlit

This repo packages the MobileSam model, served via FastAPI. Alongside, it comes with a user-friendly Streamlit UI, enabling the user to easily upload images and view the results of image segmentation.

## Run Locally
> Prerequisites: python3.11 & git

Follow these steps to set up local development environment:
- Clone the Repository
  ```bash
  git clone https://github.com/vvxhid/mobilesam-model-service/
  # Go to repo directory
  cd mobilesam-model-service
  ```
- Set Up a Virtual Environment (Optional but Recommended)
  ```bash
  # Unix/macOS
  python3.11 -m venv .venv
  source .venv/bin/activate
  # Windows
  python -m venv venv
  .\venv\Scripts\activate
  ```
- Install Dependencies
  ```bash
  # Backend dependencies (fastapi)
  pip install -r app/requirements.txt
  # Frontend dependencies (streamlit)
  pip install -r frontend/requirements.txt
  ```
- Running the Application
  > Note: Streamlit reads the FastAPI api location from an environment variable API_URL and defaults to http://127.0.0.1:8000/api.
  ```bash
  # Run the backend server
  uvicorn app.main:app --reload
  # Run streamlit
  export API_URL=http://127.0.0.1:8000/api # Api base url
  streamlit run frontend/app.py
  ```
- Accessing the Application
  - FastAPI: http://127.0.0.1:8000/api/health
  - Streamlit: http://127.0.0.1:8501/
  - API docs: http://127.0.0.1:8000/api/docs & http://127.0.0.1:8000/api/redoc

## Docker
> Prerequisites: docker & docker compose plugin (or docker compose standalone)
```bash
docker compose up -d --build # After the initial build, you can omit --build for subsequent runs.
# Stopping the app
docker compose down
```
## Tests
The backend app uses pytest for unit testing. To run the tests:
```bash
pytest -W ignore
```
  
