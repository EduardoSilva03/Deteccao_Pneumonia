import React, { useState } from 'react';
import './registrar.css';
import { FaEnvelope, FaLock } from "react-icons/fa";
import { useNavigate } from 'react-router-dom'; // <- IMPORTANTE

const Registrar = () => {
    const [email, setEmail] = useState("");
    const [senha, setSenha] = useState("");
    const navigate = useNavigate(); // <- INSTANCIAR

    const handleSubmit = async () => {
        try {
            const res = await fetch("http://localhost:5000/api/registrar", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email, senha })
            });

            const data = await res.json();

            if (res.ok) {
                alert(data.mensagem || "Usuário registrado com sucesso!");
                navigate("/acessar"); // <- REDIRECIONAMENTO
            } else {
                alert(data.erro || "Erro ao registrar.");
            }
        } catch (err) {
            console.error("Erro na requisição:", err);
            alert("Erro na comunicação com o servidor.");
        }
    };

    return (
        <div className="registrar-container">
            <div className="registrar-header">
                <div className="left">Detecção de Pneumonia por DeepLearning</div>
                <div className="right">
                    <div className="registrar-text">Criar conta</div>
                    <div className="registrar-inputs">
                        <div className="registrar-input">
                            <FaEnvelope />
                            <input type="email" placeholder="E-mail" onChange={e => setEmail(e.target.value)} />
                        </div>
                        <div className="registrar-input">
                            <FaLock />
                            <input type="password" placeholder="Senha" maxLength="6" onChange={e => setSenha(e.target.value)} />
                        </div>
                        <div className="registrar-submit">
                            <button onClick={handleSubmit}>Registrar</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Registrar;