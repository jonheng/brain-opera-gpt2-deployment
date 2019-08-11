# Brain Opera GPT-2 deployment

## Starting gunicorn server

```sh
gunicorn -b :8000 server:app
```

## Building docker image

```sh
docker build -t brain-opera-gpt2 .
```

## Running docker image

```sh
This will run the docker image in the background
docker run -d -p 8000:8000 brain-opera-gpt2
```
