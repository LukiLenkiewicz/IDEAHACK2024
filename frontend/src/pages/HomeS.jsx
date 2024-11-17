import React, { useEffect, useState } from 'react';
import Row from '../components/Row';
import axios from 'axios';

function HomeS() {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const feed = JSON.parse(localStorage.getItem("authUser"));
                console.log(feed)
                
                const response = await axios.get(`http://localhost:8000/api/create-project/${feed.email}/${feed.id}`);

                setData(response.data); // Set the response data
                setLoading(false); // Set loading to false after data is fetched
            } catch (err) {
                setError('Failed to fetch data');
                setLoading(false);
            }
        };

        fetchData(); // Call the fetchData function

    }, []); // The e

    return (
        <div className='bg-gray-500'>
            {loading && <p>Loading...</p>}
            {error && <p>Error: {error}</p>}
            {data && (
                <>
                    <Row rowID='3' title='Projects' list={data.projects} />
                    <Row rowID='2' title='Companies' list={data.companies} />
                    <Row rowID='1' title='Users' list={data.users} />
                </>
            )}
        </div>
    );
}

export default HomeS;
