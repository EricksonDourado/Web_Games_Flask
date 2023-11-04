from flask import Flask, render_template, request, redirect, url_for, session, flash
from jogos import Jogo
from usuario import Usuario

game01 = Jogo('Gran Turismo', 'Corrida', 'PS2')
game02 = Jogo('Endurece', 'Corrida', 'Atari')
game03 = Jogo('Fifa Soccer', 'Futebol', 'PS1')
list_gammer = [game01, game02, game03]

user01 = Usuario('Administrador', 'Admin', '1')
user02 = Usuario('Jones', 'Jon', '123')
usuarios ={ user01.nome_resumo : user01,
            user02.nome_resumo : user02 }

app = Flask(__name__)
app.secret_key = 'secreto_top_gammer'

@app.route('/')
def index():
    return render_template('index.html', titulo='Library Gammer', gammers=list_gammer)

@app.route('/novo/')
def novo():
        if 'usuario_logado' not in session or session['usuario_logado'] == None:
            return redirect(url_for('login', proxima =url_for('novo')))
        return render_template('novo.html', titulo="Libray Gammer")

@app.route('/criar/', methods=['POST'])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    novo_gammer = Jogo(nome, categoria, console)    
    list_gammer.append(novo_gammer)
    return  redirect(url_for('index'))

@app.route('/login/')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', titulo='Library Gammer', proxima=proxima)

@app.route('/autenticar', methods=['POST',])
def autenticar():
    if request.form['usuario'] in usuarios:        
        usuario = usuarios[request.form['usuario']]
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.nome_resumo
            flash(usuario.nome + ' logou com sucesso!')
            proxima_page = request.form['proxima']
            return redirect('/novo/')
    else:
        flash('Usuário ou Senha Incorreto, tente novamente!')
        return redirect(url_for('login'))

@app.route('/logout/')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('index'))

app.run(debug=True)

