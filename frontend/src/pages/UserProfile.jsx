import React, { useEffect, useState } from 'react';

const UserProfile = ({ userEmail }) => {
  const [userData, setUserData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Using dummy data for testing
    const fetchData = async () => {
      try {
        // Simulating a delay for the API call
        await new Promise((resolve) => setTimeout(resolve, 500));

        // Dummy data
        const data = {
          name: 'John Doe',
          email: 'john.doe@example.com',
          description: 'Software engineer with a passion for building web applications.',
          experience: '5+ years in full-stack development, specializing in React and Node.js.',
          skills: ['JavaScript', 'React', 'Node.js', 'CSS', 'Python'],
          website: 'https://johndoe.dev',
          social_media: {
            LinkedIn: 'https://linkedin.com/in/johndoe',
            GitHub: 'https://github.com/johndoe',
            Twitter: 'https://twitter.com/johndoe',
          },
        };

        setUserData(data);
      } catch (err) {
        setError('Failed to load data');
      }
    };

    fetchData();
  }, [userEmail]);

  if (error) return <p className="text-red-500 text-center mt-4">{error}</p>;
  if (!userData) return <p className="text-gray-500 text-center mt-4">Loading...</p>;

  return (
    <div className="max-w-md mx-auto bg-white shadow-lg rounded-lg overflow-hidden mt-16">
      {/* Profile Image */}
      <div className="flex justify-center mt-6">
        <img
          className="w-32 h-32 rounded-full border-2 border-blue-500"
          src="https://via.placeholder.com/150"
          alt={userData.name}
        />
      </div>

      {/* User Details */}
      <div className="p-6">
        {/* Name */}
        <h1 className="text-2xl font-bold text-center text-gray-800">{userData.name}</h1>
        {/* Email */}
        <p className="text-center text-gray-600">{userData.email}</p>

        {/* Description */}
        <p className="text-center text-gray-700 mt-4">{userData.description}</p>

        {/* Experience */}
        <div className="mt-6">
          <h2 className="text-lg font-semibold text-gray-800">Experience</h2>
          <p className="text-gray-700">{userData.experience}</p>
        </div>

        {/* Skills */}
        <div className="mt-6">
          <h2 className="text-lg font-semibold text-gray-800">Skills</h2>
          <ul className="list-disc list-inside text-gray-700">
            {userData.skills.map((skill, index) => (
              <li key={index}>{skill}</li>
            ))}
          </ul>
        </div>

        {/* Website */}
        <div className="mt-6">
          <h2 className="text-lg font-semibold text-gray-800">Website</h2>
          <a
            href={userData.website}
            target="_blank"
            rel="noopener noreferrer"
            className="text-blue-500 hover:underline"
          >
            {userData.website}
          </a>
        </div>

        {/* Social Media */}
        <div className="mt-6">
          <h2 className="text-lg font-semibold text-gray-800">Social Media</h2>
          <div className="flex space-x-4">
            {Object.entries(userData.social_media).map(([platform, link]) => (
              <a
                key={platform}
                href={link}
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-500 hover:underline"
              >
                {platform}
              </a>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default UserProfile;
