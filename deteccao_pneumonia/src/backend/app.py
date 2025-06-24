from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost:5432/deteccao_pneumonia'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Usuarios(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)

@app.route('/api/registrar', methods=['POST'])
def registrar():
    data = request.json
    novo_usuario = Usuarios(email=data['email'], senha=data['senha'])
    db.session.add(novo_usuario)
    db.session.commit()
    return jsonify({'mensagem': 'Usuário registrado com sucesso!'})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    usuario = Usuarios.query.filter_by(email=data['email'], senha=data['senha']).first()
    if usuario:
        return jsonify({
            'mensagem': 'Login bem-sucedido!',
            'usuario_id': usuario.id
        })
    return jsonify({'erro': 'Credenciais inválidas'}), 401

class Anexos(db.Model):
    id = db.Column(db.Integer, primary_key=True, server_default=db.text("nextval('usuarios_id_seq'::regclass)"))
    id_usuarios = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    anexos = db.Column(db.String(255))

@app.route('/api/anexar', methods=['POST'])
def anexar():
    data = request.json
    id_usuarios = data.get('id_usuarios')
    nome_arquivo = data.get('anexos')

    if not id_usuarios or not nome_arquivo:
        return jsonify({'erro': 'Dados incompletos'}), 400

    novo_anexo = Anexos(id_usuarios=id_usuarios, anexos=nome_arquivo)
    db.session.add(novo_anexo)
    db.session.commit()

    return jsonify({'mensagem': 'Arquivo anexado com sucesso'})

if __name__ == '__main__':
    app.run(debug=True)