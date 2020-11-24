FROM python:3.8-slim-buster

RUN python3 -m venv venv

# Install dependencies:
COPY requirements.txt .
RUN /venv/bin/pip install -r requirements.txt

# Run the application:
COPY main.py .
CMD ["/venv/bin/python", "main.py"]