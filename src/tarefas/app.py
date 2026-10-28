from flask import Flask, render_template

app = Flask(__name__)

@app.route('/test')
def test():
    return 'Servidor online!'

@app.route('/')
def home():
    return render_template('base.html', titulo='Minha lista de tarefas para procastinar')

if __name__ == '__main__':
    app.run()