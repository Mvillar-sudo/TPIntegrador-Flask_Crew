import mysql.connector
from flask import g
from .config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, DB_PORT, SCHEMA_SQL_PATH

def get_db():
    if 'db' not in g or not g.db.is_connected():
        g.db = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            port=DB_PORT,
            ssl_disabled=True
        )
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    cursor = db.cursor()

    with open(SCHEMA_SQL_PATH, encoding='utf-8') as f:
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

def init_app(app):
    app.teardown_appcontext(close_db)
