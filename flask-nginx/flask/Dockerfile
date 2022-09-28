FROM python:3.8-alpine

COPY ./requirements.txt /app/requirements.txt
COPY ./flask-http.py /app/flask-http.py

WORKDIR /app
RUN pip3 install -r requirements.txt
RUN pip3 install waitress
COPY . /app

ENTRYPOINT ["python3"]
CMD ["-u", "flask-http.py"]
