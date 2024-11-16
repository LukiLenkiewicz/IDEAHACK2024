import React from 'react';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from './components/NavBar';
import HomeS from './pages/HomeS';
import Signup from './components/Signup';
import Login from './components/Login';

function App() {
  return (
    <Router>
      {/* Navbar is displayed on all pages */}
      {/* <Navbar /> */}
      
      <Routes>
        <Route path="/" element={<HomeS />} />
        <Route path='/login' element={<Login/>} />
        <Route path='/signup' element={<Signup/>} />
      </Routes>
    </Router>
  );
}

export default App;
