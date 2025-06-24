import React, { useState } from "react";
import './acessar.css';
import { FaEnvelope, FaLock } from "react-icons/fa";
import { Link, useNavigate } from 'react-router-dom';

const Acessar = () => {
    const [email, setEmail] = useState("");
    const [senha, setSenha] = useState("");
    const navigate = useNavigate();

    const handleLogin = async () => {
        try {
            const res = await fetch("http://localhost:5000/api/login", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email, senha })
            });

            const data = await res.json();

            if (res.ok) {
                alert(data.mensagem || "Login bem-sucedido!");
                localStorage.setItem("usuario_id", data.usuario_id);
                navigate("/anexos");
            } else {
                alert(data.erro || "Erro no login.");
            }
        } catch (err) {
            console.error("Erro na requisição:", err);
            alert("Erro ao conectar com o servidor.");
        }
    };

    return (
        <div className="acessar-container">
            <div className="acessar-header">
                <div className="left">
                    <div>Detecção de Pneumonia por DeepLearning</div>
                </div>
                <div className="right">
                    <div className="acessar-text">Acessar conta</div>
                    <div className="acessar-inputs">
                        <div className="acessar-input">
                            <FaEnvelope />
                            <input
                                type="email"
                                placeholder="E-mail"
                                value={email}
                                onChange={e => setEmail(e.target.value)}
                            />
                        </div>
                        <div className="acessar-input">
                            <FaLock />
                            <input
                                type="password"
                                placeholder="Senha"
                                maxLength="6"
                                value={senha}
                                onChange={e => setSenha(e.target.value)}
                            />
                        </div>
                        <div className="acessar-submit">
                            <button type="button" onClick={handleLogin}>Acessar</button>
                        </div>
                        <div className="acessar-registro">
                            <p>Não tem uma conta ?</p>
                            <Link to="/registrar" className="acessar-registro-link">&nbsp;Criar conta</Link>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Acessar;