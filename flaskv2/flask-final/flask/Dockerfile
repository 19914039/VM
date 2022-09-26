FROM python:3.8-alpine
COPY ./requirements.txt /app/requirements.txt
COPY ./flask-docker.py /app/flask-docker.py
COPY ./cert.pem /app/cert.pem
COPY ./key.pem /app/key.pem
WORKDIR /app
RUN pip3 install -r requirements.txt
COPY . /app
ENTRYPOINT ["python3"]
CMD ["-u", "flask-docker.py"]
