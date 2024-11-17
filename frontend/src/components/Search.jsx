import { useState } from 'react';
import { BiSearch } from 'react-icons/bi'; // Make sure to import any required icons
import Select from 'react-tailwindcss-select';
import axios from 'axios'; // Import Axios for API calls
import { Link, useNavigate } from 'react-router-dom';
import Row from './Row';

function MyComponent() {
  const [profileType, setProfileType] = useState('');
  const [technology, setTechnology] = useState('');
  const [industry, setIndustry] = useState('');
  const [role, setRole] = useState('');
  const [experience, setExperience] = useState('');
  const [words, setWords] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [results, setResults] = useState({ projects: [], companies: [], users: [] }); // Initialize as an empty structure
  const navigate = useNavigate();

  const data = {
    PROFILE_TYPES: [
      { label: "User", value: "USER" },
      { label: "Company", value: "COMPANY" },
      { label: "Project", value: "PROJECT" },
    ],
    FILTER_TYPES: {
      TECHNOLOGY: [
        { label: "Python", value: "Python" },
        { label: "Java", value: "Java" },
        { label: "C++", value: "C++" },
      ],
      INDUSTRY: [
        { label: "Healthcare", value: "Healthcare" },
        { label: "Finance", value: "Finance" },
        { label: "Education", value: "Education" },
        { label: "Machine Learning", value: "Machine Learning" },
      ],
      ROLE: [
        { label: "Software Engineer", value: "Software Engineer" },
        { label: "Product Manager", value: "Product Manager" },
        { label: "Data Scientist", value: "Data Scientist" },
      ],
      EXPERIENCE: [
        { label: "0-1 years", value: "0-1 years" },
        { label: "1-3 years", value: "1-3 years" },
        { label: "3-5 years", value: "3-5 years" },
        { label: "5+ years", value: "5+ years" },
      ],
    },
  };

  const handleProfileTypeChange = (selectedOption) => {
    setProfileType(selectedOption);
  };

  const handleTechnologyChange = (selectedOption) => {
    setTechnology(selectedOption);
  };

  const handleIndustryChange = (selectedOption) => {
    setIndustry(selectedOption);
  };

  const handleRoleChange = (selectedOption) => {
    setRole(selectedOption);
  };

  const handleExperienceChange = (selectedOption) => {
    setExperience(selectedOption);
  };

  const handleFilter = async (event) => {
    setWords(event.target.value);
  };

  const handleKeyPress = async (event) => {
    if (event.key === 'Enter') {
      event.preventDefault(); // Prevent form submission on Enter key
      handleFilter(event);
      console.log(event.target.value);

      try {
        setLoading(true);
        const response = await axios.get('http://35.157.234.63:8000/api/feed/', {
          params: {
            search_query: event.target.value,
          },
        });

        localStorage.setItem("search", JSON.stringify(response.data.feed));
        navigate('/data_search')

      } catch (error) {
        console.error("Error fetching search results:", error);
        setError("Error fetching search results");
      } finally {
        setLoading(false);
      }
    }
  };

  return (
    <div className="h-screen bg-gray-500 flex items-center justify-center pt-6">
      <div className="w-full max-w-2xl bg-white p-6 rounded-lg shadow-lg">
        {/* Select Inputs */}
        <div className="space-y-4">
          <div className="flex flex-col">
            <label htmlFor="profileType" className="font-medium">Profile Type</label>
            <Select
              value={profileType}
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
              onChange={handleIndustryChange}
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
              onChange={handleExperienceChange}
              options={data.FILTER_TYPES.EXPERIENCE}
              id="experience"
            />
          </div>
        </div>

        {/* Search Bar */}
        <div className="grid items-center justify-center pt-6">
          <div className="w-full border-b-4 border-black py-1 px-4">
            <div className="relative block">
              <form className="static bg-white">
                <input
                  value={words}
                  onChange={handleFilter}
                  onKeyPress={handleKeyPress}
                  className="bg-primary p-3 md:text-md font-medium border-2 border-green-900 focus:outline-none focus:border-2 focus:border-gray-300 w-full md:w-[350px] rounded-full md:top-0"
                  placeholder="Search for IDEAS"
                />
                <button
                  type="submit"
                  className="absolute md:right-5 right-6 top-4 border-l-2 border-pink-300 pl-4 text-2xl text-gray-400"
                >
                  <BiSearch />
                </button>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default MyComponent;
