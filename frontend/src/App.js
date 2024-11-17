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
import PrivateRoute from './utilis/PrivateRoute'
import SearchBar from './components/Search';

function App() {
  return (
    <Router>
      <AuthProvider>
      <Routes>

      <Route path="/" element={
          // <PrivateRoute>
            //  <Navbar />
             <HomeS />
          // </PrivateRoute>
          }
        ></Route>
      {/* Navbar is displayed on all pages */}
      {/* <Navbar /> */}
      {/* <PrivateRoute> */}
      {/* <Route path='/profil' element={<UserProfile/>} userEmail="johndoe@example.com" /> */}
      
        <Route path="/userData" element={
            <PrivateRoute>
              <UpdateUserForm />
              </PrivateRoute>} >
              </Route>

        <Route path="/search" element={
            // <PrivateRoute>
              //  <Navbar />
              <SearchBar /> } ></Route>
            {/* // </PrivateRoute>} > */}
        
        <Route path="/chat" element={<Chat />} />

        <Route path='/login' element={<Login/>} />
        <Route path='/signup' element={<Signup/>} />
      </Routes>
      </AuthProvider>
    </Router>
  );
}

export default App;
