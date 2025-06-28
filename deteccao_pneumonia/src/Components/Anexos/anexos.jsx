import React, { useEffect } from 'react';
import './anexos.css';
import { FaInbox } from 'react-icons/fa';
import Cabecalho from '../Cabecalho/cabecalho';
import { useNavigate } from 'react-router-dom';
import { useState } from 'react';

const Anexos = () => {
  const navigate = useNavigate();

  const [imagemPreview, setImagemPreview] = useState(null);
  const [resultadoIA, setResultadoIA] = useState(null);

  useEffect(() => {
    const usuarioId = localStorage.getItem("usuario_id");
    if (!usuarioId) {
      navigate("/acessar");
    }
  }, [navigate]);

    const handleAnexarArquivo = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    // Mostra preview
    setImagemPreview(URL.createObjectURL(file));
    setResultadoIA(null); // limpa resultado anterior

    const usuarioId = localStorage.getItem("usuario_id");
    if (!usuarioId) {
      alert("Usuário não está logado.");
      navigate("/acessar");
      return;
    }

    const formData = new FormData();
    formData.append("arquivo", file);
    formData.append("id_usuarios", usuarioId);

    try {
      const res = await fetch("http://localhost:5000/api/anexar", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();

      if (data.erro) {
        alert(data.erro);
      } else {
        setResultadoIA({
          classificacao: data.classificacao,
          probabilidade: (data.probabilidade * 100).toFixed(2),
        });
      }
    } catch (err) {
      console.error("Erro ao enviar o arquivo:", err);
      alert("Erro ao enviar o arquivo.");
    }
  };


  return (
    <>
      <Cabecalho />
      <div className="anexos-container">
        <h1 className="anexos-titulo">Anexar Arquivos de Radiografia</h1>

        <div className="anexos-upload-box">
          <input type="file" id="fileInput" hidden onChange={handleAnexarArquivo} />
          <label htmlFor="fileInput" className="anexos-label">
            Selecionar arquivos
            <FaInbox className="anexos-icon" />
          </label>
          <p className="anexos-instrucao">ou arraste e solte os arquivos aqui</p>
        </div>

        <div className="anexos-descricao">
          Este sistema utiliza inteligência artificial para auxílio de diagnósticos de pneumonia em radiografias torácicas.
        </div>
        <div className="anexos-aviso">
          Os resultados não substituem o diagnóstico médico profissional.
        </div>
                {imagemPreview && (
          <div className="anexos-preview">
            <img src={imagemPreview} alt="Preview" className="anexos-imagem" />
            {resultadoIA && (
              <div className="anexos-resultado">
                <strong>Resultado:</strong> {resultadoIA.classificacao}<br />
                <strong>Probabilidade:</strong> {resultadoIA.probabilidade}%
              </div>
            )}
          </div>
        )}

      </div>
    </>
  );
};

export default Anexos;