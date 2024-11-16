import React from 'react';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from './components/NavBar';
import HomeS from './pages/HomeS';
import Signup from './components/Signup';
import Login from './components/Login';
import UpdateUserForm from './components/userSettings';
import Chat from './components/Chat';
import UserProfile from './pages/UserProfile';
import { AuthProvider } from './utilis/Auth';

function App() {
  return (
    <Router>
      <AuthProvider>
      {/* Navbar is displayed on all pages */}
      {/* <Navbar /> */}
      {/* <PrivateRoute> */}
      {/* <Route path='/profil' element={<UserProfile/>} userEmail="johndoe@example.com" /> */}
      
      <Routes>
        <Route path="/" element={<HomeS />} />
        <Route path="/userData" element={<UpdateUserForm />} />
        <Route path="/chat" element={<Chat />} />

        <Route path='/login' element={<Login/>} />
        <Route path='/signup' element={<Signup/>} />
      </Routes>
      </AuthProvider>
    </Router>
  );
}

export default App;
