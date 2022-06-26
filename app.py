from flask import Flask, render_template, request, redirect 
import Banco
import werkzeug




app = Flask(__name__)



@app.route('/')
def inicio():
    return render_template('index.html')





@app.route('/container')
def container():
    return render_template('container.html')



@app.route('/movimentacao')
def movimentacao():

    lista = Banco.db_lista_container()

    return render_template('movimentacao.html', conteineres = lista)




@app.route('/relatorio')
def relatorio():


    lista = Banco.db_lista_relatario()

    categoria = Banco.db_total_categoria()

    return render_template('relatorio.html',lista = lista, categoria = categoria )





@app.route('/add_container', methods=['GET', 'POST'])
def add_container():
    
 # Extrai os dados do formulário.
    cliente = request.form["cliente"].lstrip().upper()
    numero = request.form["numero"].lstrip()
    tipo = request.form["tipo"].lstrip().capitalize()
    status = request.form["status"].lstrip().capitalize()
    categoria = request.form["categoria"].lstrip().capitalize()
    
    # Faz o processamento.
    ja_existia, container = Banco.criar_container(cliente, numero, tipo, status, categoria)
    
   
    # Monta a resposta.
    mensagem = f"O Container já existe." if ja_existia else f"O Container adicionado com sucesso."


    return render_template('index.html', mensagem = mensagem)



@app.route('/add_movimento', methods=['GET', 'POST'])
def add_movimento():
    
 # Extrai os dados do formulário.
    tipo = request.form["tipo"]
    data_inicio = request.form["data_inicio"]
    data_fim = request.form["data_fim"]
    id_container = request.form["id_container"]
    
    
    # Faz o processamento.
    ja_existia, movimento = Banco.criar_movimentacao(tipo, data_inicio, data_fim, id_container)
    
   
    # Monta a resposta.
    mensagem = f"A Movimentação já foi feita." if ja_existia else f" Container movimentado com sucesso."


    return render_template('index.html', mensagem = mensagem)














if __name__=='__main__':
    Banco.db_inicialiar()
    app.run(debug=True)