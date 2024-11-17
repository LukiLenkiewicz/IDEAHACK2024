import React, { createContext, useState, useEffect } from "react";
import axios from "axios";
import { Link, useNavigate } from 'react-router-dom';


const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  // Function to handle logout

  const handleUserChange = (value) => {
    setUser(value);
  };


  const logout = async () => {
    try {
      setUser(null);
      localStorage.removeItem("authUser");
      navigate('/login');  // Redirect to home page after logout


    } catch (error) {
      console.error("Logout failed:", error);
      throw new Error("Logout failed");
    }
  };

  useEffect(() => {
    const savedUser = localStorage.getItem("authUser");
    if (savedUser) {
      setUser(JSON.parse(savedUser));
    }
    setLoading(false);
  }, []);

  return (
    <AuthContext.Provider value={{ user, handleUserChange, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => React.useContext(AuthContext);

export default AuthContext;
