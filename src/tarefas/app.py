from flask import Flask, redirect, render_template, request, url_for
 
from tarefas.models.database import init_db
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
        titulo_form = request.form['tituloTarefa'] # casa com o nome do input no form
        data_conclusao_form = request.form['dataConclusao'] #casa com o nome do input no form
 
        data_corrigida = data_conclusao_form or None
        # 'or' nesse caso é um operador de
 
        # Instnaciamos uma nova tarefa com os dados recebidos do form
        tarefa = Tarefa(titulo=titulo_form, data_conclusao=data_corrigida)
       
        # Salvamos a tarefa no banco
        tarefa.salvarTarefa()
 
        return redirect(url_for('home'))
 
    tarefas = Tarefa.listarTarefas()
 
    return render_template(
        'base.html',
        titulo_da_pagina='Minha lista de tarefas',
        titulo='Minha lista de tarefas',
        tarefas_da_pagina=tarefas,
        tarefa=None
    )
 
# Crie uma nova funcionalidade para apagar casa uma das tarefas cadastradas
@app.route('/delete/<int:id>')
def apagar_id_especificado(id):
    Tarefa.apagarTarefa(id)
    return redirect(url_for('home'))
 
 
# NOVA ROTA: Atualizar uma tarefa específica
@app.route('/atualizar/<int:id_tarefa>', methods=['GET', 'POST'])
def atualizar_tarefa(id_tarefa):
 
    # Carrega a tarefa do banco para a memória
    tarefa = Tarefa.buscarTarefa(id_tarefa)
 
    if tarefa is None:
        return redirect(url_for('home'))
 
    if request.method == 'POST':
        titulo_form = request.form['tituloTarefa'] # casa com o nome do input no form
        data_conclusao_form = request.form['dataConclusao'] #casa com o nome do input no form
 
        data_corrigida = data_conclusao_form or None
        # 'or' nesse caso é um operador de
 
        # Envia os dados alterados para o banco
        Tarefa.atualizarTarefa(
            id_tarefa,
            titulo_form,
            data_corrigida
        )
 
        return redirect(url_for('home'))
 
    return render_template(
        'base.html',
        titulo='Atualizar tarefa',
        titulo_da_pagina='Atualizar tarefa',
        tarefas_da_pagina=Tarefa.listarTarefas(),
        tarefa=tarefa
    )
 
 
if __name__ == '__main__':
    app.run()