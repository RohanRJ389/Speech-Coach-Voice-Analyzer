// DoughnutChart.js
import React, { useEffect, useRef } from 'react';
import Chart from 'chart.js/auto';

const DoughnutChart = () => {
    const chartRef = useRef(null);

    useEffect(() => {
        const ctx = chartRef.current.getContext('2d');

        // Data for the doughnut chart
        const data = {
            labels: ['Simile', 'Normal text', 'Metaphor' , "Questions"],
            datasets: [{
                data: [12, 19, 3 ,6],
                backgroundColor: [
                    'rgba(255, 99, 132, 0.8)',
                    'rgba(54, 162, 235, 0.8)',
                    'rgba(255, 206, 86, 0.8)',
                    'rgba(75, 192, 192, 0.8)',
                    'rgba(153, 102, 255, 0.8)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)'
                ],
                borderWidth: 1
            }]
        };

        // Configuration for the chart
        const config = {
            type: 'doughnut',
            data: data,
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    title: {
                        display: true,
                        text: 'Doughnut Chart Example'
                    }
                }
            }
        };

        // Initialize the chart
        const chart = new Chart(ctx, config);

        return () => {
            // Clean up: Destroy the chart instance when component unmounts
            chart.destroy();
        };
    }, []);

    return (
        <div
            style={{
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
                width: '100%',
                height: '400px'
            }}
        >
            <canvas ref={chartRef}></canvas>
        </div>
    );
};

export default DoughnutChart;
