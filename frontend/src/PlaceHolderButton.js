import React, { useEffect, useState } from 'react';
// import example from "./example.txt"



const PlaceholderButton = () => {

const [datat, setdatat] = useState("")
const [datac, setdatac] = useState("")

    const [isOpen, setIsOpen] = useState(false);

    const openModal = () => setIsOpen(true);
    const closeModal = () => setIsOpen(false);

    const handleClick = async () => {
        
        try {
            let response = await fetch("http://127.0.0.1:5000/get_text");
            let dt = await response.text();
            setdatat(dt)
             response = await fetch("http://127.0.0.1:5000/getc_text");
             dt = await response.text();
            setdatac(dt)
            openModal()
        } catch (error) {
            console.error('Error fetching text file:', error);
        }

    };
    useEffect(() => {
        handleClick()
    },[])

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
            Transcript of entire speech.
            <p style={{color: "red"}} >
            {datat}
            </p>
            <br></br>
            Corrected text.
            <p style={{color: "green"}} >
            {datac}
            </p>
        </button>
    );
};

export default PlaceholderButton;
