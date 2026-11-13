from flask import Flask, redirect, render_template, request, url_for

from tarefas.models.database import Database, init_db
from tarefas.models.tarefa import Tarefa

app = Flask(__name__)

with app.app_context():
    init_db()

@app.route('/test')
def test():
    return 'Servidor online!'

@app.route('/', methods=['GET', 'POST'])
def home():

    if request.method == 'POST':
        titulo_form = request.form['tituloTarefa']
        data_conclusao_form = request.form['dataConclusao']

        data_corrigida = data_conclusao_form or None

        # Instanciamos uma tarefa com os dados recebidos do from
        tarefa = Tarefa(titulo = titulo_form, data_conclusao = data_conclusao_form)

        # Salvamos a tarefa no banco
        tarefa.salvarTarefa()

        return redirect(url_for('home'))

    tarefas = Tarefa.listarTarefas()
    
    return render_template(
        'base.html', 
        titulo_da_pagina='Minha lista de tarefas para procastinar', 
        tarefas_da_pagina=tarefas
    )


# Faça uma nova funcionalidade para apagar cada uma das tarefas cadastradas 
@app.route('/delete/<int:id>')
def apagar_id_especificado(id):
    sql = 'DELETE FROM tarefa WHERE id_tarefa = %s'

    with Database as db:
        db.executar(sql, (id))

    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run()