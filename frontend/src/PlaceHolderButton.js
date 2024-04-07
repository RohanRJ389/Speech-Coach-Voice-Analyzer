import React, { useState } from 'react';
// import example from "./example.txt"



const PlaceholderButton = () => {

const [data, setdata] = useState("")

    const [isOpen, setIsOpen] = useState(false);

    const openModal = () => setIsOpen(true);
    const closeModal = () => setIsOpen(false);

    const handleClick = async () => {
        
        try {
            const response = await fetch("http://127.0.0.1:5000/get_text");
            const dt = await response.text();
            setdata(dt)
            openModal()
        } catch (error) {
            console.error('Error fetching text file:', error);
        }

    };

    return (
        <button
            style={{
                backgroundColor: 'rgb(51, 161, 201)',
                color: 'white',
                border: 'none',
                padding: '10px 20px',
                borderRadius: '5px',
                cursor: 'pointer',
                marginTop: '20px',
                marginBottom: '20px'
            }}
            onClick={handleClick}
        >
            Grammatical Feedback
            <p>
            {data}
            </p>
        </button>
    );
};

export default PlaceholderButton;
