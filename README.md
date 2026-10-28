# Gerenciador de tarefas

Esse projeto servirá para aprimorar nossa lógica de programação ao mesmo tempo em que exploramos conceitos e técnicas de programação back-end e fullstack. Vamos utilizar e desenvolver o conceito de MVC (Model-View-Controller) , algumas particularidades da Programação Orientada a Objetos, Programação Funcional, persistência de dados (MySQL) , microframework Flask e gerenciador de pacotes do Python (Astral uv).

Alguns passos iniciais para preparar o projeto:
1. Caso não esteja instalado, prepare o uv no seu OS. Você encontra o script de instalação no site <https://docs.astral.sh/uv/#installation>
```bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

2. Faça a inicialização do projeto com o comando:
```bash
uv init
```

Até então utilizávamos um Layout de Pacotes (Packet Layout) denominado flat-layout. O uv adota uma estruturação mais moderna chamada src-layout, que previne erros de importação comuns chamadas `import shadowing` (importações mascaradas).

3. Crie um ambiente virtual do Python:
```bash
uv venv
```

Ative o ambiente virtual:
```powershell
.\.venv\Scripts\activate.ps1 # no Powershell do Windows
source .venv/Scripts/activate # no Git Bash do Windows
source .venv/bin/activate # no Bash do Linux 
```

4. Instale o Flask
```bash
uv add Flask
```

Será criado um arquivo `uv.lock` cintendo as dependências (requerimentos) e versões dos pacotes do seu projeto.

5. Crie um arquivo `app.py` contendo o código inicial do projeto
```python
from flask import Flask

app = Flask(__name__)

@app.route('/test')
def test():
    return 'Servidor online!'
```

6. Teste a aplicação iniciando o servidor do Flask
```bash
uv ren flask run
```