import React, { useEffect, useState } from 'react';
import Row from '../components/Row';

// Dummy JSON data
const dummyData = {
    "projects": [
      {
        "id": 1,
        "name": "Project A",
        "bio": "Project A is an innovative endeavor focused on building a scalable solution for modern cloud-based applications, ensuring high availability, performance, and seamless user experience.",
        "rowID": 1
      },
      {
        "id": 2,
        "name": "Project B",
        "bio": "Project B explores cutting-edge technologies in artificial intelligence and machine learning, aiming to revolutionize data-driven decision-making processes for enterprises.",
        "rowID": 1
      },
      {
        "id": 3,
        "name": "Project C",
        "bio": "Project C aims to develop next-generation blockchain solutions to enhance security and transparency in supply chain management.",
        "rowID": 1
      },
      {
        "id": 4,
        "name": "Project D",
        "bio": "Project D is focused on creating immersive augmented reality experiences for the education and entertainment industries.",
        "rowID": 1
      },
      {
        "id": 5,
        "name": "Project E",
        "bio": "Project E is a groundbreaking initiative targeting advancements in quantum computing to solve complex optimization problems.",
        "rowID": 1
      },
      {
        "id": 6,
        "name": "Project F",
        "bio": "Project F is a machine learning-based platform aimed at improving predictive maintenance in manufacturing industries.",
        "rowID": 1
      },
      {
        "id": 7,
        "name": "Project G",
        "bio": "Project G is dedicated to creating an AI-powered system for personalized learning experiences in online education.",
        "rowID": 1
      },
      {
        "id": 8,
        "name": "Project H",
        "bio": "Project H works on integrating IoT devices into smart cities to enhance traffic management and energy efficiency.",
        "rowID": 1
      },
      {
        "id": 9,
        "name": "Project I",
        "bio": "Project I focuses on the development of bioinformatics tools for genomic research, aiming to accelerate breakthroughs in personalized medicine.",
        "rowID": 1
      },
      {
        "id": 10,
        "name": "Project J",
        "bio": "Project J explores the use of augmented reality for enhancing remote collaboration and communication in professional settings.",
        "rowID": 1
      }
    ],
    "companies": [
      {
        "id": 1,
        "name": "Company X",
        "bio": "Company X is a global leader in renewable energy solutions, dedicated to providing sustainable and innovative technologies to combat climate change and support a greener future.",
        "rowID": 2
      },
      {
        "id": 2,
        "name": "Company Y",
        "bio": "Company Y specializes in advanced cybersecurity solutions, offering robust systems to safeguard critical data against evolving digital threats in a hyper-connected world.",
        "rowID": 2
      },
      {
        "id": 3,
        "name": "Company Z",
        "bio": "Company Z is pioneering advancements in autonomous vehicle technologies, aiming to redefine the future of transportation.",
        "rowID": 2
      },
      {
        "id": 4,
        "name": "Company W",
        "bio": "Company W excels in biotechnology, creating innovative healthcare solutions to improve patient outcomes globally.",
        "rowID": 2
      },
      {
        "id": 5,
        "name": "Company V",
        "bio": "Company V focuses on developing high-performance semiconductors for the next generation of electronics and IoT devices.",
        "rowID": 2
      },
      {
        "id": 6,
        "name": "Company U",
        "bio": "Company U is at the forefront of creating artificial intelligence systems to automate financial trading and investment strategies.",
        "rowID": 2
      },
      {
        "id": 7,
        "name": "Company T",
        "bio": "Company T is a leader in 3D printing technologies, offering advanced solutions for rapid prototyping and production in industries like automotive and aerospace.",
        "rowID": 2
      },
      {
        "id": 8,
        "name": "Company S",
        "bio": "Company S is revolutionizing e-commerce with cutting-edge logistics and supply chain optimization technologies, offering faster and more efficient delivery systems.",
        "rowID": 2
      },
      {
        "id": 9,
        "name": "Company R",
        "bio": "Company R is a top provider of next-gen data storage solutions, catering to businesses' growing need for scalable and secure cloud storage infrastructure.",
        "rowID": 2
      },
      {
        "id": 10,
        "name": "Company Q",
        "bio": "Company Q is a leading player in the fintech sector, developing innovative solutions to streamline online payments, lending, and banking services.",
        "rowID": 2
      }
    ],
    "users": [
      {
        "id": 1,
        "name": "User 1",
        "bio": "User 1 is a software engineer with over a decade of experience in developing enterprise-grade applications, skilled in various programming languages and passionate about mentoring aspiring developers.",
        "rowID": 3
      },
      {
        "id": 2,
        "name": "User 2",
        "bio": "User 2 is a data scientist with a strong background in statistical analysis and machine learning, driven by a commitment to leveraging data insights to solve real-world challenges.",
        "rowID": 3
      },
      {
        "id": 3,
        "name": "User 3",
        "bio": "User 3 is a creative UX/UI designer with expertise in crafting user-centric interfaces for web and mobile applications, aiming to enhance the user experience through intuitive design.",
        "rowID": 3
      },
      {
        "id": 4,
        "name": "User 4",
        "bio": "User 4 is a project manager experienced in leading cross-functional teams and delivering complex projects on time and within budget.",
        "rowID": 3
      },
      {
        "id": 5,
        "name": "User 5",
        "bio": "User 5 is a cloud architect specializing in designing and implementing scalable cloud infrastructures for enterprises, ensuring reliability and cost-efficiency.",
        "rowID": 3
      },
      {
        "id": 6,
        "name": "User 6",
        "bio": "User 6 is a software developer with expertise in building mobile applications, focusing on performance optimization and delivering high-quality user experiences.",
        "rowID": 3
      },
      {
        "id": 7,
        "name": "User 7",
        "bio": "User 7 is a data engineer skilled in designing and maintaining large-scale data pipelines to support machine learning models and data analytics initiatives.",
        "rowID": 3
      },
      {
        "id": 8,
        "name": "User 8",
        "bio": "User 8 is a product manager experienced in leading teams to build innovative digital products, with a focus on aligning business objectives with technology solutions.",
        "rowID": 3
      },
      {
        "id": 9,
        "name": "User 9",
        "bio": "User 9 is a business analyst with a background in analyzing market trends and developing strategies for data-driven decision-making.",
        "rowID": 3
      },
      {
        "id": 10,
        "name": "User 10",
        "bio": "User 10 is a machine learning engineer specializing in developing deep learning models and applying them to solve complex problems in healthcare and natural language processing.",
        "rowID": 3
      }
    ]
  }
  


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