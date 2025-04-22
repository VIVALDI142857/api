FROM python:3.10-slim


WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY st_ui.py .

# Expose the port
EXPOSE 8501


# Run the application with Uvicorn
CMD ["streamlit", "run", "st_ui.py"]
