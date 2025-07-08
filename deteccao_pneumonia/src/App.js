// App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Acessar from './Components/Acessar/acessar';
import Registrar from './Components/Registrar/registrar';
import Anexos from './Components/Anexos/anexos';
import { Navigate } from 'react-router-dom';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Navigate to="/acessar" />} />
        <Route path="/acessar" element={<Acessar />} />
        <Route path="/registrar" element={<Registrar />} />
        <Route path="/anexos" element={<Anexos />} />
      </Routes>
    </Router>
  );
}

export default App;