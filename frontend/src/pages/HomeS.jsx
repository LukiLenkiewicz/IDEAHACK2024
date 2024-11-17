import React, { useEffect, useState } from 'react';
import Row from '../components/Row';

// Dummy JSON data
const dummyData = {
    projects: [
        { 
            id: 1, 
            name: "Project A", 
            description: "Project A is an innovative endeavor focused on building a scalable solution for modern cloud-based applications, ensuring high availability, performance, and seamless user experience.", 
            rowID: 1 
        },
        { 
            id: 2, 
            name: "Project B", 
            description: "Project B explores cutting-edge technologies in artificial intelligence and machine learning, aiming to revolutionize data-driven decision-making processes for enterprises.", 
            rowID: 1 
        }
    ],
    companies: [
        { 
            id: 1, 
            name: "Company X", 
            description: "Company X is a global leader in renewable energy solutions, dedicated to providing sustainable and innovative technologies to combat climate change and support a greener future.", 
            rowID: 2 
        },
        { 
            id: 2, 
            name: "Company Y", 
            description: "Company Y specializes in advanced cybersecurity solutions, offering robust systems to safeguard critical data against evolving digital threats in a hyper-connected world.", 
            rowID: 2 
        }
    ],
    users: [
        { 
            id: 1, 
            name: "User 1", 
            description: "User 1 is a software engineer with over a decade of experience in developing enterprise-grade applications, skilled in various programming languages and passionate about mentoring aspiring developers.", 
            rowID: 3 
        },
        { 
            id: 2, 
            name: "User 2", 
            description: "User 2 is a data scientist with a strong background in statistical analysis and machine learning, driven by a commitment to leveraging data insights to solve real-world challenges.", 
            rowID: 3 
        }
    ]
};


function HomeS() {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        // Simulate fetching data
        try {
            setTimeout(() => {
                setData(dummyData); // Replace this with API call later
                setLoading(false);
            }, 500); // Simulating delay
        } catch (err) {
            setError('Failed to fetch data');
            setLoading(false);
        }
    }, []);

    return (
        <div className='bg-gray-500'>
            {loading && <p>Loading...</p>}
            {error && <p>Error: {error}</p>}
            {data && (
                <>
                    <Row rowID='1' title='Projects' list={data.projects} />
                    <Row rowID='2' title='Companies' list={data.companies} />
                    <Row rowID='3' title='Users' list={data.users} />
                </>
            )}
        </div>
    );
}

export default HomeS;
