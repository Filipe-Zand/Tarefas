from flask import Flask, render_template

from tarefas.models.database import init_db

app = Flask(__name__)

with app.app_context():
    init_db()

@app.route('/test')
def test():
    return 'Servidor online!'

@app.route('/')
def home():
    return render_template('base.html', titulo='Minha lista de tarefas para procastinar')

if __name__ == '__main__':
    app.run()