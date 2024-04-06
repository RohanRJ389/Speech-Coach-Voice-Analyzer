import { Chart, LinearScale } from 'chart.js/auto';
import { useEffect, useRef, useState } from 'react';
import jsonDataFile from './metrics.json';

// Register linear scale
Chart.register(LinearScale);



function Metrics() {
    const [jsonData, setJsonData] = useState({});
    const [metricsData, setMetricsData] = useState(
        [
            { name: 'Intensity', values: [0, 0, 0, 0, 0] },
            { name: 'Speech Rate', values: [0, 0, 0, 0, 0] },
            { name: 'Disfluency Rate', values: [0, 0, 0, 0, 0] },
            { name: 'Pitch Variation', values: [0, 0, 0, 0, 0] }
        ]
    );
    function fetchJSONData() {
        setJsonData(JSON.parse(JSON.stringify(jsonDataFile)))

        setMetricsData(prev => {


            let arr = prev[0]["values"]
            arr.shift()
            arr.push(parseFloat(jsonData["intensity"]) * 100)
            prev[0]["values"] = arr

            arr = prev[1]["values"]
            arr.shift()
            arr.push(parseFloat(jsonData["speech_rate"]) * 100)
            prev[1]["values"] = arr

            arr = prev[2]["values"]
            arr.shift()
            arr.push(parseFloat(jsonData["disfluency_rate"]) * 100)
            prev[2]["values"] = arr

            arr = prev[3]["values"]
            arr.shift()
            arr.push(parseFloat(jsonData["pitch_variation"]) * 100)
            prev[3]["values"] = arr


            return prev
        })

    }
    useEffect(() => {
        let intrvl = setInterval(fetchJSONData, 2000);

        return () => {
            clearInterval(intrvl)
        }
    })



    const chartRef = useRef(null);


    useEffect(() => {

        let graphintrvl = setInterval(() => {


            let ctx = document.getElementById('myChart').getContext('2d');
            let labels = Array.from({ length: metricsData[0].values.length }, (_, i) => i + 1); // Generate labels from 1 to n
            let datasets = [];

            // Calculate the average incrementally for each point across all metrics
            for (let i = 0; i < labels.length; i++) {
                let sum = 0;
                metricsData.forEach(metric => {
                    sum += metric.values[i];
                });
                const average = sum / 4;
                datasets.push(average.toFixed(2));
                console.log(datasets)
            }

            // Check if a chart instance already exists and destroy it
            if (chartRef.current) {
                chartRef.current.destroy();
            }

            // Create new chart instance
            chartRef.current = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Average Metrics',
                        data: datasets,
                        fill: false,
                        borderColor: 'rgba(75, 192, 192, 1)',
                        tension: 0.1
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            })

        }, 1000)

        return () => {
            clearInterval(graphintrvl)
        }

    }, [])

    return (
        <div>
            {/* Chart Placeholder */}
            <h2>{jsonData["tip"]}</h2>
            <canvas id="myChart" width="500" height="500"></canvas>
            <div>
                {metricsData.map((metric, index) => (
                    <div key={index}>
                        <p>{metric.name}: {metric.values.join(', ')}</p>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default Metrics;
