import React, { useEffect, useState } from 'react';
import './anexos.css';
import { FaInbox } from 'react-icons/fa';
import Cabecalho from '../Cabecalho/cabecalho';
import { useNavigate } from 'react-router-dom';

const Anexos = () => {
  const navigate = useNavigate();
  const [imagemHeatmap, setImagemHeatmap] = useState(null);
  const [resultadoIA, setResultadoIA] = useState(null);
  const [historico, setHistorico] = useState([]);

  useEffect(() => {
    const usuarioId = localStorage.getItem("usuario_id");
    if (!usuarioId) {
      navigate("/acessar");
    } else {
      fetch(`http://localhost:5000/api/historico/${usuarioId}`)
        .then(res => res.json())
        .then(data => setHistorico(data));
    }
  }, [navigate]);

  const handleAnexarArquivo = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

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
        setImagemHeatmap(null);
        setResultadoIA(null);
      } else {
        setResultadoIA({
          classificacao: data.classificacao,
          probabilidade: (data.probabilidade * 100).toFixed(2),
        });
        setImagemHeatmap(`data:image/jpeg;base64,${data.imagem_heatmap}`);

        setHistorico(prev => [...prev, { imagem_base64: data.imagem_heatmap }]);
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
          Este sistema utiliza inteligência artificial para diagnóstico de pneumonia.
        </div>

        <div className="anexos-aviso">
          Os resultados não substituem o diagnóstico médico profissional.
        </div>

        {imagemHeatmap && resultadoIA && (
          <div className="anexos-preview">
            <img src={imagemHeatmap} alt="Resultado" className="anexos-imagem" />
            <div
              className="anexos-resultado"
              style={{ color: resultadoIA.classificacao === "NORMAL" ? "green" : "red" }}
            >
              <strong>Resultado:</strong> {resultadoIA.classificacao}<br />
              <strong>Probabilidade:</strong> {resultadoIA.probabilidade}%
            </div>
          </div>
        )}
      </div>
    </>
  );
};

export default Anexos;