import React from 'react';
import './anexos.css';
import { FaInbox } from 'react-icons/fa';
import Cabecalho from '../Cabecalho/cabecalho';
import { useNavigate } from 'react-router-dom';

const Anexos = () => {
  const navigate = useNavigate();

const handleAnexarArquivo = async (e) => {
  const file = e.target.files[0];
  if (!file) return;

  const usuarioId = localStorage.getItem("usuario_id");
  if (!usuarioId) {
    alert("Usuário não está logado.");
    navigate("/acessar");
    return;
  }

  const res = await fetch("http://localhost:5000/api/anexar", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      id_usuarios: parseInt(usuarioId),
      anexos: file.name
    })
  });

  const data = await res.json();
  alert(data.mensagem || data.erro);
};

  return (
    <>
      <Cabecalho />
      <div className="anexos-container">
        <h1 className="anexos-titulo">Anexar Arquivos de Radiografia</h1>

        <div className="anexos-upload-box">
          <input type="file" id="fileInput" hidden multiple onChange={handleAnexarArquivo} />
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
      </div>
    </>
  );
};

export default Anexos;