import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './cabecalho.css';

const Cabecalho = () => {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("usuario_logado");
    localStorage.removeItem("usuario_id");
    navigate("/acessar");
  };


  return (
    <header className="cabecalho">
      <nav className="cabecalho-nav">
        <div className="cabecalho-links"></div>
        <button className="cabecalho-sair" onClick={handleLogout}>Sair</button>
      </nav>
    </header>
  );
};

export default Cabecalho;