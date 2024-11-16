import React from 'react';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from './components/NavBar';
import HomeS from './pages/HomeS';
import Signup from './components/Signup';
import Login from './components/Login';
import UpdateUserForm from './components/userSettings';
import Chat from './components/Chat';
import UserProfile from './pages/UserProfile';

function App() {
  return (
    <Router>
      {/* Navbar is displayed on all pages */}
      {/* <Navbar /> */}
      {/* <PrivateRoute> */}
      
      <Routes>
        <Route path="/" element={<HomeS />} />
        <Route path="/userData" element={<UpdateUserForm />} />
        <Route path="/chat" element={<Chat />} />
        <Route path='/login' element={<Login/>} />
        <Route path='/signup' element={<Signup/>} />
        <Route path='profil' element={<UserProfile/>} userEmail="johndoe@example.com" />
      </Routes>
    </Router>
  );
}

export default App;
