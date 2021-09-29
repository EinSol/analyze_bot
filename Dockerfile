FROM python:3.8.3-slim

COPY requirements.txt /analize_bot/requirements.txt

WORKDIR /analize_bot

RUN pip install --no-cache-dir -r requirements.txt

COPY . /analize_bot

CMD ["python", "./core.py"]