FROM python:3.9

WORKDIR /app

RUN pip install Flask requests pandas

COPY . .
CMD ["python", "app.py"]
