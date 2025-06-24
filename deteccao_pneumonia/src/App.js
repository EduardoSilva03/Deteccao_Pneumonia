// App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Acessar from './Components/Acessar/acessar';
import Registrar from './Components/Registrar/registrar';
import Anexos from './Components/Anexos/anexos';


function App() {
  return (
    <Router>
      <Routes>
        <Route path="/acessar" element={<Acessar />} />
        <Route path="/registrar" element={<Registrar />} />
        <Route path="/anexos" element={<Anexos />} />
      </Routes>
    </Router>
  );
}

export default App;