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
import HomeSData from './pages/HomeSData';
import UserChat from './components/UserChat'

function App() {
  return (
    <Router>
      <AuthProvider>
      <Routes>

      <Route path="/data_search" element={
           <PrivateRoute>
             <Navbar />
             <HomeSData />
          </PrivateRoute>
          }
        ></Route>
        
        <Route path="/" element={
           <PrivateRoute>
             <Navbar />
             <HomeS />
          </PrivateRoute>
          }
        ></Route>

      {/* {/* <Route path='/profil' element={<UserProfile/>} userEmail="johndoe@example.com" /> */}
      
        <Route path="/userData" element={
            <PrivateRoute>
              <UpdateUserForm />
              </PrivateRoute>} >
              </Route>

        <Route path="/search" element={
              <SearchBar /> } ></Route>
        
        <Route path="/chat" element={<Chat />} />
        <Route path="/userchat" element={<UserChat />} />


        <Route path='/login' element={<Login/>} />
        <Route path='/signup' element={<Signup/>} />
      </Routes>
      </AuthProvider>
    </Router>
  );
}

export default App;
