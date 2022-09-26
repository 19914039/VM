FROM python:3.8-alpine
COPY ./requirements.txt /app/requirements.txt
COPY ./sql-read.py /app/sql-read.py
WORKDIR /app
RUN pip3 install -r requirements.txt
COPY . /app
ENTRYPOINT ["python3"]
CMD ["-u", "sql-read.py"]
