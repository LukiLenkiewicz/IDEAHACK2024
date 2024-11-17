import React, { useEffect, useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom'; // Import useNavigate for navigation
import Row from '../components/Row';

function HomeSData() {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const navigate = useNavigate(); // Initialize navigate

    const feed = JSON.parse(localStorage.getItem("search"));

    console.log(feed)

    return (
        <div className='bg-gray-500 w-screen h-screen'>
            {feed && (
                <>
                    <Row rowID='3' title='Projects' list={feed.PROJECT} />
                    <Row rowID='2' title='Companies' list={feed.COMPANY} />
                    <Row rowID='1' title='Users' list={feed.USER} />
                </>
            )}
        </div>
    );
}

export default HomeSData;
