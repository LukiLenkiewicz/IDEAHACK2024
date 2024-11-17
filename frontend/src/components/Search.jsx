import React, { useState, useEffect} from "react";
import {BiSearch} from 'react-icons/bi'
import {useDispatch, useSelector} from 'react-redux'
import data  from '../assets/filters.json'
import Select from 'react-tailwindcss-select'

export default function SearchBar() {

    const [profilTypes, setProfileTypes] = useState(null);
    const [technology, setTechnology] = useState(null);
    const [industry, setInudstry] = useState(null);
    const [role, setRole] = useState(null);
    const [experience, setExperience] = useState(null);


    const handleProfileTypeChange = (value) => {
        setProfileTypes(value);
      };
    
    const handleTechnologyChange = (value) => {
        setTechnology(value);
      };
    
    const handleInudstryChange = (value) => {
        setInudstry(value);
      };

    const handleRoleChange = (value) => {
        setRole(value);
      };
    
    const handleExpChange = (value) => {
        setExperience(value);
      };

    const [filterOnData, setFilterOnData] = useState([]);
    const [words, setWords] = useState("");
    const dispatch = useDispatch()

    // useEffect(() => {
    //   dispatch(listBooks())
    // },[dispatch])
    const handleFilter = (event) => {
    };
    // const handleFilter = (event) => {
    //     const wordWeLookFor = event.target.value;
    //     setWords(wordWeLookFor); 
    //     const newFilter = books.filter((value) => {
    //         return value.Name.toLowerCase().includes(words.toLowerCase());
    //     })
    //     console.log(newFilter)
    //     if (wordWeLookFor === "") {
    //         setFilterOnData([]);
    //     } else {
    //         setFilterOnData(newFilter);
    //     }};
      
    //     const clearInput = () => {
    //         setFilterOnData([]);
    //         setWords("");
    //     };
      
    return (
        <div className="h-screen bg-gray-500 flex items-center justify-center pt-6">
          <div className="w-full max-w-2xl bg-white p-6 rounded-lg shadow-lg">
            <form className="space-y-6">
              {/* Select Inputs */}
              <div className="space-y-4">
                <div className="flex flex-col">
                  <label htmlFor="profileType" className="font-medium">Profile Type</label>
                  <Select
                    value={profilTypes}
                    onChange={handleProfileTypeChange}
                    options={data.PROFILE_TYPES}
                    id="profileType"
                  />
                </div>
      
                <div className="flex flex-col">
                  <label htmlFor="technology" className="font-medium">Technology</label>
                  <Select
                    value={technology}
                    onChange={handleTechnologyChange}
                    options={data.FILTER_TYPES.TECHNOLOGY}
                    id="technology"
                  />
                </div>
      
                <div className="flex flex-col">
                  <label htmlFor="industry" className="font-medium">Industry</label>
                  <Select
                    value={industry}
                    onChange={handleInudstryChange}
                    options={data.FILTER_TYPES.INDUSTRY}
                    id="industry"
                  />
                </div>
      
                <div className="flex flex-col">
                  <label htmlFor="role" className="font-medium">Role</label>
                  <Select
                    value={role}
                    onChange={handleRoleChange}
                    options={data.FILTER_TYPES.ROLE}
                    id="role"
                  />
                </div>
      
                <div className="flex flex-col">
                  <label htmlFor="experience" className="font-medium">Experience</label>
                  <Select
                    value={experience}
                    onChange={handleExpChange}
                    options={data.FILTER_TYPES.EXPERIENCE}
                    id="experience"
                  />
                </div>
              </div>
      
              {/* Search Bar */}
              <div className="relative mt-6">
                <input
                  value={words}
                  onChange={handleFilter}
                  className="bg-primary p-3 md:text-md font-medium border-2 border-green-900 focus:outline-none focus:border-2 focus:border-gray-300 w-full md:w-[350px] rounded-full"
                  placeholder="Search for books"
                  type="text"
                />
                <button
                  className="absolute right-4 top-4 border-l-2 border-pink-300 pl-4 text-2xl text-gray-400"
                  type="submit"
                >
                  <BiSearch />
                </button>
              </div>
            </form>
          </div>
      
          {/* Filtered Results */}
          {/* {filterOnData.length !== 0 && (
            <div className="bg-white overflow-hidden mt-4">
              {filterOnData.slice(0, 8).map((value, key) => (
                <a key={key} href={`/books/${value.Book_ID}`} className="block px-4 py-2 hover:bg-gray-100">
                  <p>{value.Name}</p>
                </a>
              ))}
            </div>
          )} */}
        </div>
      );
    }
      