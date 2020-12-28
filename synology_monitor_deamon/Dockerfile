FROM python:3.8-alpine
COPY . /app
WORKDIR /app
RUN apk add --update alpine-sdk linux-headers
RUN pip3 install pipenv
RUN pipenv install
CMD ["pipenv", "run", "python3", "app.py", "--loglevel", "debug"]
