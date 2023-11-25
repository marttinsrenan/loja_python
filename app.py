from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Lista de produtos (poderia ser uma base de dados real)
produtos = [
    {'id': 1, 'nome': 'Produto 1', 'preco': 20.0},
    {'id': 2, 'nome': 'Produto 2', 'preco': 30.0},
    # Adicione mais produtos conforme necessário
]

# Configurações para o upload de arquivos
UPLOAD_FOLDER = 'static'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html', produtos=produtos)

@app.route('/adicionar_produto', methods=['GET', 'POST'])
def adicionar_produto():
    if request.method == 'POST':
        novo_produto = {
            'id': len(produtos) + 1,
            'nome': request.form['nome'],
            'preco': float(request.form['preco'])
        }

        # Lidar com o upload da imagem
        imagem = request.files['imagem']
        if imagem and allowed_file(imagem.filename):
            filename = secure_filename(imagem.filename)
            imagem.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            novo_produto['imagem'] = filename

        produtos.append(novo_produto)
        return redirect(url_for('index'))

    return render_template('adicionar_produto.html')

@app.route('/editar_produto/<int:produto_id>', methods=['GET', 'POST'])
def editar_produto(produto_id):
    produto = next((p for p in produtos if p['id'] == produto_id), None)

    if produto is None:
        return redirect(url_for('index'))

    if request.method == 'POST':
        produto['nome'] = request.form['nome']
        produto['preco'] = float(request.form['preco'])

        # Lidar com o upload da nova imagem
        nova_imagem = request.files['nova_imagem']
        if nova_imagem and allowed_file(nova_imagem.filename):
            filename = secure_filename(nova_imagem.filename)
            nova_imagem.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            produto['imagem'] = filename

        return redirect(url_for('index'))

    return render_template('editar_produto.html', produto=produto)

@app.route('/excluir_produto/<int:produto_id>')
def excluir_produto(produto_id):
    global produtos
    produtos = [p for p in produtos if p['id'] != produto_id]
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
