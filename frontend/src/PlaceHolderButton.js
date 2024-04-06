import React from 'react';

const PlaceholderButton = () => {
    const handleClick = () => {
        alert('Placeholder text');
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
                marginTop:'20px',
                marginBottom:'20px'
            }}
            onClick={handleClick}
        >
            Grammatical Feedback
        </button>
    );
};

export default PlaceholderButton;
