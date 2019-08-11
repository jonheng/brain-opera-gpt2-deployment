FROM python:3.5.7

COPY . /brain-opera-gpt2-deployment
WORKDIR /brain-opera-gpt2-deployment
RUN pip install -r requirements.txt

CMD gunicorn -b :8000 server:app