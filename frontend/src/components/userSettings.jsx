import React, { useRef, useState, useEffect } from "react"
import Select from 'react-tailwindcss-select'

const UpdateUserForm = ({ user }) => {
    const descRef = useRef();
    const expRef = useRef();
    const websiteRef = useRef();
    const socialRef = useRef();
    const [errorMess, setError] = useState("");
    const [loadingtype, setLoading] = useState(false);
    const [skills, setSkills] = useState([]); // Holds the list of skills for the selected type
    const [userSkillsTypes, setUserSkillsTypes] = useState(null);
    const [userSkills, setUserSkills] = useState(null);
    
    
    const skillsData = {
        'marketing': [
          { value: 0, label: "Digital Marketing   " },
          { value: 1, label: "Content Marketing   " },
          { value: 2, label: "SEO (Search Engine Optimization)   " },
          { value: 3, label: "PPC Advertising   " },
          { value: 4, label: "Social Media Strategy   " },
          { value: 5, label: "Email Marketing   " },
          { value: 6, label: "Brand Management   " },
          { value: 7, label: "Market Research   " },
          { value: 8, label: "Analytics & Data Interpretation   " },
          { value: 9, label: "Consumer Behavior Analysis   " },
          { value: 10, label: "Influencer Marketing   " },
          { value: 11, label: "Growth Hacking   " },
        ],
        'business_startup': [
          { value: 12, label: "Business Model Development   " },
          { value: 13, label: "Business Plan Writing   " },
          { value: 14, label: "Startup Financing   " },
          { value: 15, label: "Pitch Deck Creation   " },
          { value: 16, label: "Entrepreneurship   " },
          { value: 17, label: "Product Development   " },
          { value: 18, label: "Go-To-Market Strategy   " },
          { value: 19, label: "Operations Management   " },
          { value: 20, label: "Customer Acquisition Strategy   " },
          { value: 21, label: "Team Building & Leadership   " },
          { value: 22, label: "Scalability Planning   " },
        ],
        'research': [
          { value: 23, label: "Market Research   " },
          { value: 24, label: "Competitive Analysis   " },
          { value: 25, label: "Consumer Insights   " },
          { value: 26, label: "Trend Analysis   " },
          { value: 27, label: "Statistical Analysis   " },
          { value: 28, label: "Survey Design & Implementation   " },
          { value: 29, label: "Data Collection & Sampling   " },
          { value: 30, label: "Report Writing & Presentation   " },
          { value: 31, label: "Academic Research   " },
          { value: 32, label: "Qualitative & Quantitative Research   " },
        ],
        'investing': [
          { value: 33, label: "Stock Market Analysis   " },
          { value: 34, label: "Venture Capital   " },
          { value: 35, label: "Private Equity   " },
          { value: 36, label: "Risk Management   " },
          { value: 37, label: "Financial Modeling   " },
          { value: 38, label: "Investment Strategies   " },
          { value: 39, label: "Portfolio Management   " },
          { value: 40, label: "Due Diligence   " },
          { value: 41, label: "Startup Valuation   " },
          { value: 42, label: "Crowdfunding & Angel Investing   " },
          { value: 43, label: "Cryptocurrency Investing   " },
        ],
        'programming_and_technology': [
          { value: 44, label: "Python   " },
          { value: 45, label: "R   " },
          { value: 46, label: "Java   " },
          { value: 47, label: "C++   " },
          { value: 48, label: "JavaScript   " },
          { value: 49, label: "SQL   " },
          { value: 50, label: "HTML & CSS   " },
          { value: 51, label: "Machine Learning   " },
          { value: 52, label: "Deep Learning   " },
          { value: 53, label: "Data Structures & Algorithms   " },
          { value: 54, label: "Cloud Computing   " },
          { value: 55, label: "Web Development   " },
          { value: 56, label: "Software Development   " },
          { value: 57, label: "App Development   " },
          { value: 58, label: "Version Control (Git)   " },
          { value: 59, label: "Automation & Scripting   " },
          { value: 60, label: "Database Management   " },
          { value: 61, label: "API Development & Integration   " },
          { value: 62, label: "Cybersecurity   " },
          { value: 63, label: "DevOps   " },
          { value: 64, label: "Networking   " },
          { value: 65, label: "Blockchain Development   " },
          { value: 66, label: "Artificial Intelligence   " },
          { value: 67, label: "Natural Language Processing   " },
          { value: 68, label: "Data Visualization   " },
          { value: 69, label: "Big Data Technologies (Hadoop, Spark)   " },
          { value: 70, label: "Docker & Kubernetes   " },
        ],
      };
      

    const skills_types = [
        {value: 'investing', label: 'investing'},
        {value: 'programming_and_technology', label: 'programming_and_technology'},
        {value: 'research', label: 'research'},
        {value: 'business_startup', label: 'business_startup' },
        {value: 'marketing', label: 'marketing'},
    ]


    const handleUserSkillChange = (value) => {
        console.log(value)
        setUserSkills(value);
      };

    const handleUserSkillTypesChange = (value) => {
        setSkills(skillsData[value.value])
        setUserSkillsTypes(value);
    };


    

async function handleSubmit(e) {
    e.preventDefault();
    console.log(userSkills)
    const payload = {
      description: descRef.current.value,
      experience: expRef.current.value,
      skills: userSkills,
      webiste: websiteRef.current.value,
      social: socialRef.current.value,
    };


    console.log(payload);  // Optional: To inspect the payload before sending

    setLoading(true);  // Start loading

    // try {
    //   // Use Axios to send POST request to your Django API
    //   const response = await axios.post("http://127.0.0.1:8000/api/usersettings/", payload, {
    //     headers: {
    //       "Content-Type": "application/json",
    //     },
    //   });

    //   // Handle the response
    //   if (response.status === 201) {
    //     console.log("Account created successfully!", response.data);
    //     setError("");  // Clear any existing error messages
    //   } else {
    //     setError(response.data.message || "Failed to create an account.");
    //   }
    // } catch (err) {
    //   setError("An error occurred while creating the account.");
    //   console.error(err);
    // } finally {
    //   setLoading(false);  // Stop loading
    // }

  }

  return (
    <div className="relative w-full h-screen bg-zinc-900/90">
      <img
        src="https://media.istockphoto.com/photos/wooden-brown-books-shelves-with-a-lamp-picture-id1085770318"
        className="h-full absolute w-full object-cover mix-blend-overlay"
        alt="Background"
      />
      <div className="flex items-center justify-center h-auto pt-10 pb-5">
        <form className="max-w-[400px] w-full mx-auto rounded-lg bg-white p-10">
          <h2 className="text-4xl font-bold text-center py-5">Update Profile</h2>
          {errorMess && <div role="alert"> <div className="border relative border-red-400 rounded-b bg-red-100 px-4 py-3 text-red-700"> <p>{errorMess}</p> </div> </div>}
          <div className='flex flex-col pb-2'>
                    <label className="border-none relative">Description</label>
                    <textarea className='rounded-lg border relative  bg-gray-100 p-5' ref={descRef} />
            </div>
            <div className='flex flex-col pb-2'>
                    <label className="border-none relative">Experience</label>
                    <textarea className='rounded-lg border relative  bg-gray-100 p-5'  ref={expRef} />
            </div>
            <div className='flex flex-col border-none relative pb-2'>
                    <label className="border-none relative">Skills Types</label>
                    <Select value={userSkillsTypes} onChange={handleUserSkillTypesChange} options={skills_types} />
            </div>

            <div className='flex flex-col mb-4 border-none relative pb-2'>
                    <label className="border-none relative">Skills</label>
                    <Select value={userSkills} onChange={handleUserSkillChange} options={skills} isMultiple={true}/>
            </div>
            
            <div className='flex flex-col pb-2'>
                    <label className="border-none relative">Webiste</label>
                    <textarea className='rounded-lg border relative  bg-gray-100 p-5' ref={websiteRef} />
            </div>
            <div className='flex flex-col pb-2'>
                    <label className="border-none relative">Social Media</label>
                    <textarea className='rounded-lg border relative  bg-gray-100 p-5' ref={socialRef}/>
            </div>
          <button disabled={loadingtype} onClick={handleSubmit}  
                className='w-full p-3 border relative bg-teal-500 shadow-lg shadow-teal-500/50 hover:shadow-teal-500/40 text-white font-semibold rounded-lg justify-center'>
                Save User Data</button>
        </form>
      </div>
    </div>
  );
};

export default UpdateUserForm;
