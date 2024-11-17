import React from 'react';
import { useNavigate } from "react-router-dom";
import { FaBook } from 'react-icons/fa'; // Example icon library import

export default function BookSlicer({ name, id, desc }) {
  const navigate = useNavigate();

  function handleClick(e) {
    console.log(e)
    e.preventDefault();
    if (name === 'Project') {
        navigate(`/projects/${id}`);
    } else if (name === 'Company') {
        navigate(`/company/${id}`);
    } else if (name === 'User') {
        navigate(`/user/${id}`);
    }

    // window.location.reload(); // Optional: Only if you need a complete reload
  }

  return (
    <div className="w-[160px] max-[640px]:h-60 sm:h-64 md:h-72 lg:h-96 sm:w-[200px] md:w-[240px] lg:w-[280px] inline-block cursor-pointer relative p-2">
  {/* Replace image with an icon */}
  <div onClick={handleClick} className="w-full h-full flex justify-center items-center bg-gray-200">
    <FaBook className="text-gray-700 text-4xl" /> {/* Icon */}
  </div>
  
  {/* Description bar at the bottom */}
  <div className="absolute bottom-0 left-0 w-full h-full bg-black/70 text-white text-xs md:text-sm py-1 px-4 text-center">
  <p className="font-bold pt-5 text-xl">{name}</p>
    <div className="py-2">
  <p className="mt-1 whitespace text-wrap text-xl">{desc}</p>
  </div>

    </div>
    </div>

  );
};
