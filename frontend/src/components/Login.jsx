import React, { useRef, useState } from "react"
import { Link, useNavigate } from "react-router-dom"
import axios from "axios";
import { useAuth } from "../utilis/Auth";
import Select from 'react-tailwindcss-select'


export default function Login() {

    const { handleUserChange } = useAuth();
    const emailRef = useRef();
    const passwordRef = useRef();
    const [userType, setUserType] = useState(null);

    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const types = [
        { value: "user", label: "User" },
        { value: "company", label: "Company" },
        { value: "investor", label: "Investor" },
      ];

    const handleUserTypeChange = (value) => {
        setUserType(value);
      };

    async function handleSubmit(e) {
        e.preventDefault();

        const credentials = {
            email: emailRef.current.value,
            password: passwordRef.current.value,
            user_type: userType.value,
        };

        try {
            setError("");
            setLoading(true);

            const response = await axios.post('http://localhost:8000/api/login/', credentials, {
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            console.log(response)
            if (response.status == 200) {
                const {email: userEmail, type: userType } = response.data;
                handleUserChange({email: userEmail, type: userType})
                localStorage.setItem("authUser", JSON.stringify({email: userEmail, type: userType}));
                navigate('/');
            }
        } catch (err) {
            setError("Failed to sign in");
        }

        setLoading(false);
    }

  return (

    <div className='relative w-full h-screen bg-zinc-900/90'>
        <img src='https://media.istockphoto.com/photos/wooden-brown-books-shelves-with-a-lamp-picture-id1085770318' className="absolute w-full h-full object-cover mix-blend-overlay" />
       
        <div className='flex items-center justify-center pt-10 pb-5'>
            <form className='max-w-[400px] w-full mx-auto rounded-lg bg-white p-10'>
                <h2 className='text-4xl font-bold text-center py-5'>InCommon</h2>
                {error && <div role="alert"> <div className="border relative  border-red-400 rounded-b bg-red-100 px-4 py-3 text-red-700"> <p>{error}</p> </div> </div>}
                <div className='flex flex-col mb-4'>
                    <label className="border-none relative">Email</label>
                    <input className='rounded-lg border relative  bg-gray-100 p-2' type="text" ref={emailRef} required />
                </div>
                <div className='flex flex-col'>
                    <label className="border-none relative">Password</label>
                    <input className='p-2 border relative rounded-lg bg-gray-100  text-whitemt-2 ' type="password" ref={passwordRef} required />
                </div>
                <div className='flex flex-col border-none relative pb-2'>
                    <label htmlFor="type">Type</label>
                    <Select value={userType} onChange={handleUserTypeChange} options={types} />
                </div>
                <p className="text-center mt-4 border-none relative ">
                    Need an account? <Link to={"/signup"} className="underline"> Sign up</Link>
                </p>
                <button disabled={loading} onClick={handleSubmit} className='w-full my-5 py-2 border relative bg-teal-500 shadow-lg shadow-teal-500/50 hover:shadow-teal-500/40 text-white font-semibold rounded-lg'>Sign in</button>
                
            </form>
        </div>
    </div>
  )
}