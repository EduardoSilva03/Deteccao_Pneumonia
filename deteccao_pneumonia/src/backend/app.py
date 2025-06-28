from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

# IA - imports
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from PIL import Image
import numpy as np

# Flask app config
app = Flask(__name__)
CORS(app)

# Pasta para uploads
UPLOAD_FOLDER = 'Images_Usuario'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost:5432/deteccao_pneumonia'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Carregando o modelo treinado
modelo_pneumonia = load_model("../Components/Treinamento/modelo_pneumonia.h5")  # Certifique-se de que o arquivo está no mesmo diretório

# Tabelas
class Usuarios(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)

class Anexos(db.Model):
    id = db.Column(db.Integer, primary_key=True, server_default=db.text("nextval('usuarios_id_seq'::regclass)"))
    id_usuarios = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    anexos = db.Column(db.String(255))

# Rotas
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
    email = data.get('email')
    senha = data.get('senha')

    usuario = Usuarios.query.filter_by(email=email, senha=senha).first()

    if usuario:
        return jsonify({
            'mensagem': 'Login bem-sucedido!',
            'usuario_id': usuario.id
        })

    return jsonify({'erro': 'Credenciais inválidas'}), 401

@app.route('/api/anexar', methods=['POST'])
def anexar():
    if 'arquivo' not in request.files:
        return jsonify({'erro': 'Nenhum arquivo enviado'}), 400

    arquivo = request.files['arquivo']
    id_usuarios = request.form.get('id_usuarios')

    if not id_usuarios or arquivo.filename == '':
        return jsonify({'erro': 'Dados incompletos ou arquivo inválido'}), 400

    # Salva o arquivo
    caminho_arquivo = os.path.join(app.config['UPLOAD_FOLDER'], arquivo.filename)
    arquivo.save(caminho_arquivo)

    # Processa a imagem
    try:
        imagem = Image.open(caminho_arquivo).convert('RGB')
        imagem = imagem.resize((224, 224))  # Mesmo tamanho usado no treino
        imagem_array = img_to_array(imagem) / 255.0
        imagem_array = np.expand_dims(imagem_array, axis=0)
    except Exception as e:
        return jsonify({'erro': f'Erro ao processar imagem: {str(e)}'}), 400

    # Faz a predição com IA
    try:
        predicao = modelo_pneumonia.predict(imagem_array)[0][0]
        resultado = "PNEUMONIA" if predicao > 0.5 else "NORMAL"
    except Exception as e:
        return jsonify({'erro': f'Erro ao classificar a imagem: {str(e)}'}), 500

    # Salva no banco
    novo_anexo = Anexos(id_usuarios=int(id_usuarios), anexos=arquivo.filename)
    db.session.add(novo_anexo)
    db.session.commit()

    return jsonify({
        'mensagem': 'Arquivo salvo e analisado com sucesso!',
        'classificacao': resultado,
        'probabilidade': float(predicao)
    })

# Inicia servidor
if __name__ == '__main__':
    app.run(debug=True)