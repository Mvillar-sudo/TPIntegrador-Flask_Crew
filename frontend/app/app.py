from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return 'Frontend funcionando correctamente en el puerto 3000'

if __name__ == '__main__':
    app.run(port=3000, debug=True)