#!/usr/bin/env python3
from flask import Flask, request, json, jsonify
import sqlite3
import uuid
from  werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps

app=Flask(__name__)
key='Mit@l'

def token_required(f):
    @wraps(f)
    def decorator(*args,**kwargs):
        token=None
        token=request.headers.get('authorization',None)
        if token:
            try:
                data=jwt.decode(token,key,algorithms="HS256")
            except (jwt.DecodeError, jwt.ExpiredSignatureError):
                return jsonify({'message': 'token is invalid'})
            current_user=get_user_by_pubId(data['public_id'])
            return f(current_user,*args,**kwargs)
        else:
            return jsonify({'message' : 'Token is missing !!'})
    return decorator

@app.route('/api/login',  methods = ['POST'])
def api_login():
    data = request.get_json(force=True)
    name=data['name']
    password=data['password']
    return verify_user(name,password)

@app.route('/api/dht',  methods = ['POST'])
@token_required
def api_insert_dht_reading(current_user):
    if current_user=='dht':
        data = request.get_json(force=True)
        ts = data['timestamp']
        temp = data['temperature']
        hum = data['humidity']
        return (insert_dht_reading(ts,temp,hum))
    else:
        return jsonify({'msg' : 'Not Authorised'})

@app.route('/api/arduino',  methods = ['POST'])
@token_required
def api_insert_arduino_reading(current_user):
    if current_user=='arduino':
        data = request.get_json(force=True)
        ts = data['timestamp']
        wg = data['windGen']
        sg = data['solarGen']
        return (insert_arduino_reading(ts,wg,sg))
    else:
        return jsonify({'msg' : 'Not Authorised'})

@app.route('/api/psa',  methods = ['POST'])
@token_required
def api_insert_psa_result(current_user):
    if current_user=='psa':
        data = request.get_json(force=True)
        ts = data['timestamp']
        res1 = data['result1']
        res2 = data['result2']
        return (insert_psa_result(ts,res1,res2))
    else:
        return jsonify({'msg' : 'Not Authorised'})

@app.route('/api/camt',  methods = ['POST'])
@token_required
def api_insert_camt_result(current_user):
    if current_user=='camt':
        data = request.get_json(force=True)
        ts = data['timestamp']
        res1 = data['result1']
        res2 = data['result2']
        return (insert_camt_result(ts,res1,res2))
    else:
        return jsonify({'msg' : 'Not Authorised'})

@app.route('/api/edge',  methods = ['POST'])
@token_required
def api_insert_edge_result(current_user):
    if current_user=='edge':
        data = request.get_json(force=True)
        ts = data['timestamp']
        res1 = data['result1']
        res2 = data['result2']
        return (insert_edge_result(ts,res1,res2))
    else:
        return jsonify({'msg' : 'Not Authorised'})

def connect_to_db():
    conn=sqlite3.connect('/DataVolume/Database.db', isolation_level=None)
    conn.execute('pragma journal_mode=wal')
    return conn

def create_db_table_user():
    conn=connect_to_db()
    cursor=conn.cursor()    
    cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='USER' ''')
    if cursor.fetchone()[0]==1:
        return
    else:
        cursor.execute('''CREATE TABLE USER (id INTEGER PRIMARY KEY, name TEXT, public_id TEXT, password TEXT)''')
        cursor.execute('''INSERT INTO USER (name, public_id, password) VALUES(?,?,?)''',('dht', str(uuid.uuid4()),generate_password_hash('user1')))
        cursor.execute('''INSERT INTO USER (name, public_id, password) VALUES(?,?,?)''',('arduino', str(uuid.uuid4()),generate_password_hash('user2')))
        cursor.execute('''INSERT INTO USER (name, public_id, password) VALUES(?,?,?)''',('psa', str(uuid.uuid4()),generate_password_hash('user3')))
        cursor.execute('''INSERT INTO USER (name, public_id, password) VALUES(?,?,?)''',('camt', str(uuid.uuid4()),generate_password_hash('user4')))
        cursor.execute('''INSERT INTO USER (name, public_id, password) VALUES(?,?,?)''',('edge', str(uuid.uuid4()),generate_password_hash('user5')))
        cursor.execute('''INSERT INTO USER (name, public_id, password) VALUES(?,?,?)''',('user6', str(uuid.uuid4()),generate_password_hash('user6')))
    conn.commit()
    conn.close()

def get_user_by_pubId(public_id):
    conn=connect_to_db()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM user WHERE public_id=?", (public_id,))
    row=cursor.fetchone()
    current_user=row[1]
    return current_user

def verify_user(name,password):
    conn=connect_to_db()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM user WHERE name=?",(name,))
    row = cursor.fetchone()
    if row is None:
        return jsonify({'message' : 'User does Not Exists !!'})
    elif check_password_hash(row[3],password):
        token = jwt.encode({'public_id' : str(row[2]), 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=45)}, key, algorithm="HS256")
        return jsonify({'token' : token})
    else:
        return jsonify({'message' : 'Could not Verfy the user !!'})
    conn.close()

def create_db_table_dht():
    conn=connect_to_db()
    cur=conn.cursor()
    cur.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='dht' ''')
    if cur.fetchone()[0]==1:
        return
    else:
        conn.execute('''CREATE TABLE dht (readingNum INTEGER PRIMARY KEY NOT NULL , timestamp TEXT, temperature REAL, humidity REAL)''')
    conn.commit()
    conn.close()

def insert_dht_reading(ts,temp,hum):    
    conn=connect_to_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO dht (timestamp,temperature,humidity) VALUES (?,?,?)",(ts,temp,hum))
    conn.commit()
    conn.close()
    return jsonify({'message' : 'Done'})

def create_db_table_arduino():
    conn=connect_to_db()
    cur=conn.cursor()
    cur.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='arduino' ''')
    if cur.fetchone()[0]==1:
        return
    else:
        conn.execute('''CREATE TABLE arduino (readingNum INTEGER PRIMARY KEY NOT NULL , timestamp TEXT, windGen REAL, solarGen REAL)''')
    conn.commit()
    conn.close()

def insert_arduino_reading(ts,wg,sg):
    conn=connect_to_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO arduino (timestamp,windGen,solarGen) VALUES (?,?,?)",(ts,wg,sg))
    conn.commit()
    conn.close()
    return jsonify({'message' : 'Done'})

def create_db_table_psa():
    conn=connect_to_db()
    cur=conn.cursor()
    cur.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='psa' ''')
    if cur.fetchone()[0]==1:
        return
    else:
        conn.execute('''CREATE TABLE psa (ID INTEGER PRIMARY KEY NOT NULL , timestamp TEXT, result1 REAL, result2 REAL)''')
    conn.commit()
    conn.close()

def insert_psa_result(ts,res1,res2):
    conn=connect_to_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO psa (timestamp,result1,result2) VALUES (?,?,?)",(ts,res1,res2))
    conn.commit()
    conn.close()
    return jsonify({'message' : 'Done'})

def create_db_table_camt():
    conn=connect_to_db()
    cur=conn.cursor()
    cur.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='camt' ''')
    if cur.fetchone()[0]==1:
        return
    else:
        conn.execute('''CREATE TABLE camt (ID INTEGER PRIMARY KEY NOT NULL , timestamp TEXT, result1 REAL, result2 REAL)''')
    conn.commit()
    conn.close()

def insert_camt_result(ts,res1,res2):
    conn=connect_to_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO camt (timestamp,result1,result2) VALUES (?,?,?)",(ts,res1,res2))
    conn.commit()
    conn.close()
    return jsonify({'message' : 'Done'})

def create_db_table_edge():
    conn=connect_to_db()
    cur=conn.cursor()
    cur.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='edge' ''')
    if cur.fetchone()[0]==1:
        return
    else:
        conn.execute('''CREATE TABLE edge (ID INTEGER PRIMARY KEY NOT NULL , timestamp TEXT, result1 REAL, result2 REAL)''')
    conn.commit()
    conn.close()

def insert_edge_result(ts,res1,res2):
    conn=connect_to_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO edge (timestamp,result1,result2) VALUES (?,?,?)",(ts,res1,res2))
    conn.commit()
    conn.close()
    return jsonify({'message' : 'Done'})


if __name__ == '__main__':
    connect_to_db()
    create_db_table_user()
    create_db_table_dht()
    create_db_table_arduino()
    create_db_table_psa()
    create_db_table_camt()
    create_db_table_edge()
    app.run(host="0.0.0.0", port=5000, ssl_context=('cert.pem', 'key.pem'))
    
