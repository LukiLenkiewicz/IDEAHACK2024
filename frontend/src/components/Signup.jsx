import React, { useRef, useState, useEffect } from "react"
// import { useAuth } from "../context/AuthContext"
// import {useDispatch, useSelector} from 'react-redux'
import { Link, useNavigate } from "react-router-dom"
import axios from "axios";
import Select from 'react-tailwindcss-select'

export default function Signup() {
  const emailRef = useRef();
  const passwordRef = useRef();
  const passwordConfirmRef = useRef();
  const userNameRef = useRef();
  const userSureNameRef = useRef();
  const [errorMess, setError] = useState("");
  const [userType, setUserType] = useState(null);
  const [loadingtype, setLoading] = useState(false);

  const types = [
    { value: "0", label: "User" },
    { value: "1", label: "Inve" },
    { value: "2", label: "RND" },
    { value: "3", label: "Business" },
  ];

  const handleUserTypeChange = (value) => {
    setUserType(value);
  };

  async function handleSubmit(e) {
    e.preventDefault();

    // Check if passwords match
    if (passwordRef.current.value !== passwordConfirmRef.current.value) {
      setError("Passwords do not match");
      return;
    }

    // Ensure a user type is selected
    if (userType === null) {
      setError("Please select a user type");
      return;
    }

    const payload = {
      email: emailRef.current.value,
      password: passwordRef.current.value,
      username: userNameRef.current.value,
      surname: userSureNameRef.current.value,
      user_type: userType.value,
    };

    console.log(payload);  // Optional: To inspect the payload before sending

    setLoading(true);  // Start loading

    try {
      // Use Axios to send POST request to your Django API
      const response = await axios.post("http://127.0.0.1:8000/api/signup/", payload, {
        headers: {
          "Content-Type": "application/json",
        },
      });

      // Handle the response
      if (response.status === 201) {
        console.log("Account created successfully!", response.data);
        setError("");  // Clear any existing error messages
      } else {
        setError(response.data.message || "Failed to create an account.");
      }
    } catch (err) {
      setError("An error occurred while creating the account.");
      console.error(err);
    } finally {
      setLoading(false);  // Stop loading
    }
  }

  return (
    <div className="relative w-full h-screen">
    <div className='w-full h-auto min-h-full bg-zinc-900/90'>
      <img className=' absolute w-full h-full min-h-full object-cover mix-blend-overlay overflow-hidden' src={'https://media.istockphoto.com/photos/wooden-brown-books-shelves-with-a-lamp-picture-id1085770318'} alt="/" />
        <div className='flex items-center justify-center h-auto pt-3 pb-2'>
            <form className='max-w-[400px] w-full mx-auto rounded-lg bg-white p-10'>
                <h2 className='text-4xl font-bold text-center py-5'>XDDD Tool</h2>
                {errorMess && <div role="alert"> <div className="border relative border-red-400 rounded-b bg-red-100 px-4 py-3 text-red-700"> <p>{errorMess}</p> </div> </div>}
                <div className='flex flex-col pb-2'>
                    <label className="border-none relative">Email</label>
                    <input className='rounded-lg border relative  bg-gray-100 p-2' type="text" ref={emailRef} required />
                </div>
                <div className='flex flex-col pb-2'>
                    <label className="border-none relative">Password</label>
                    <input className='p-2 border relative rounded-lg bg-gray-100  text-whitemt-2 ' type="password" ref={passwordRef} required />
                </div>
                <div className='flex flex-col pb-2'>
                    <label className="border-none relative">Password Confirmation</label>
                    <input className='p-2 border relative rounded-lg bg-gray-100  text-whitemt-2 ' type="password" ref={passwordConfirmRef} required />
                </div>
                <div className='flex flex-col pb-2'>
                    <label className="border-none relative">Username</label>
                    <input className='rounded-lg border relative  bg-gray-100 p-2' type="text" ref={userNameRef} required />
                </div>
                <div className='flex flex-col pb-2'>
                    <label className="border-none relative">SureName</label>
                    <input className='rounded-lg border relative  bg-gray-100 p-2' type="text" ref={userSureNameRef} required />
                </div>

                <div className='flex flex-col border-none relative pb-2'>
                    <label htmlFor="type">Type</label>
                    <Select value={userType} onChange={handleUserTypeChange} options={types} />
                </div>
                <p className="text-center pb-2 border-none relative ">
                    aaa
                    {/* Already have an account? <Link to={"/login"} className="underline"> Log In</Link> */}
                </p>
                <button disabled={loadingtype} onClick={handleSubmit} 
                className='w-full p-3 border relative bg-teal-500 shadow-lg shadow-teal-500/50 hover:shadow-teal-500/40 text-white font-semibold rounded-lg justify-center'>
                SIGN IN</button>
            </form >
        </div>
    </div>
    </div>
  )
}