import os
import mysql.connector
from flask import g

def get_db():
    if 'db' not in g:
        g.db = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME'),
            port=os.getenv('DB_PORT', 3306)
        )

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()
    cursor = db.cursor()

    with open('data/schema.sql', encoding='utf-8') as f:
        sql = f.read()

    for result in cursor.execute(sql, multi=True):
        pass

    db.commit()
    cursor.close()


def query_db(query, args=(), one=False):
    cursor = get_db().cursor(dictionary=True)

    cursor.execute(query, args)
    result = cursor.fetchall()

    cursor.close()

    if one:
        return result[0] if result else None

    return result


def execute_db(query, args=()):
    db = get_db()
    cursor = db.cursor()

    cursor.execute(query, args)
    db.commit()

    affected = cursor.rowcount

    cursor.close()

    return affected

import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="sitio_gastronomico"
    )

def init_app(app):
    app.teardown_appcontext(close_db)