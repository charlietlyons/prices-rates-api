FROM alpine:latest

RUN apk update
RUN apk add py-pip
RUN apk add --no-cache python3-dev 
RUN pip install --upgrade pip
RUN pip install flask

WORKDIR /app
COPY . /app
RUN pip --no-cache-dir install -r requirements.txt

CMD ["python3", "app.py"]

EXPOSE 5000