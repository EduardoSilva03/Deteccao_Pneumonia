from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
import io
import base64
import numpy as np
import matplotlib.cm as cm
from PIL import Image
import tensorflow as tf
from tensorflow.keras.models import load_model, Model
from tensorflow.keras.preprocessing.image import img_to_array

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'Images_Usuario'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost:5432/deteccao_pneumonia'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

modelo_pneumonia = load_model("../Components/Treinamento/modelo_pneumonia.h5")

class Usuarios(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)

class Anexos(db.Model):
    id = db.Column(db.Integer, primary_key=True, server_default=db.text("nextval('usuarios_id_seq'::regclass)"))
    id_usuarios = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    anexos = db.Column(db.String(255))

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

@app.route('/api/anexar', methods=['POST'])
def anexar():
    if 'arquivo' not in request.files:
        return jsonify({'erro': 'Nenhum arquivo enviado'}), 400

    arquivo = request.files['arquivo']
    id_usuarios = request.form.get('id_usuarios')

    if not id_usuarios or arquivo.filename == '':
        return jsonify({'erro': 'Dados incompletos ou arquivo inválido'}), 400

    pasta_usuario = os.path.join(app.config['UPLOAD_FOLDER'], str(id_usuarios))
    os.makedirs(pasta_usuario, exist_ok=True)

    caminho_arquivo = os.path.join(pasta_usuario, arquivo.filename)
    arquivo.save(caminho_arquivo)

    try:
        imagem = Image.open(caminho_arquivo).convert('RGB')
        imagem = imagem.resize((224, 224))
        imagem_array = img_to_array(imagem) / 255.0
        imagem_array = np.expand_dims(imagem_array, axis=0)

        predicao = modelo_pneumonia.predict(imagem_array)[0][0]
        resultado = "PNEUMONIA" if predicao > 0.5 else "NORMAL"

        if resultado == "NORMAL":
            buffer = io.BytesIO()
            imagem.save(buffer, format="JPEG")
            imagem_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
        else:
            # Grad-CAM
            last_conv_layer = modelo_pneumonia.get_layer("Conv_1")  # Substitua pelo nome da última conv layer do seu modelo se necessário
            grad_model = Model([modelo_pneumonia.inputs], [last_conv_layer.output, modelo_pneumonia.output])

            with tf.GradientTape() as tape:
                conv_outputs, predictions = grad_model(imagem_array)
                loss = predictions[:, 0]

            grads = tape.gradient(loss, conv_outputs)[0]
            pooled_grads = tf.reduce_mean(grads, axis=(0, 1))
            conv_outputs = conv_outputs[0]
            heatmap = tf.reduce_sum(tf.multiply(pooled_grads, conv_outputs), axis=-1)

            heatmap = np.maximum(heatmap, 0)
            if np.max(heatmap) != 0:
                heatmap /= np.max(heatmap)
            heatmap = np.uint8(255 * heatmap)

            heatmap_img = Image.fromarray(heatmap).resize((224, 224))
            colored_heatmap = cm.jet(np.array(heatmap_img) / 255.0)
            colored_heatmap = np.uint8(255 * colored_heatmap[..., :3])

            imagem_np = np.array(imagem)
            superimposed_img = np.uint8(imagem_np * 0.6 + colored_heatmap * 0.4)

            final_img = Image.fromarray(superimposed_img)
            buffer = io.BytesIO()
            final_img.save(buffer, format="JPEG")
            imagem_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

        novo_anexo = Anexos(id_usuarios=int(id_usuarios), anexos=arquivo.filename)
        db.session.add(novo_anexo)
        db.session.commit()

        return jsonify({
            'mensagem': 'Arquivo salvo e analisado com sucesso!',
            'classificacao': resultado,
            'probabilidade': float(predicao),
            'imagem_heatmap': imagem_base64
        })

    except Exception as e:
        return jsonify({'erro': f'Erro ao processar imagem: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)