FROM python:3.8-alpine
COPY ./requirements.txt /app/requirements.txt
COPY ./req-https.py /app/req-https.py
COPY ./cert.pem /app/cert.pem
WORKDIR /app
RUN pip3 install -r requirements.txt
COPY . /app
ENTRYPOINT ["python3"]
CMD ["-u", "req-https.py"]
