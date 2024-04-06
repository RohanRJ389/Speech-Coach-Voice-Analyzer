import { Chart, LinearScale } from 'chart.js/auto';
import { useEffect, useRef ,useState} from 'react';
import jsonDataFile from './metrics.json';

// Register linear scale
Chart.register(LinearScale);



function Metrics() {
    const [jsonData, setJsonData] = useState({});
    function fetchJSONData() {
        setJsonData(JSON.parse(JSON.stringify(jsonDataFile))) 
    
    }
    useEffect(() => {
        let intrvl = setInterval(fetchJSONData, 2000);

        return () => {
            clearInterval(intrvl)
        }
    })

    const metricsData = [
        { name: 'Intensity', values: [10, 20, 30, 40, 50] },
        { name: 'Speech Rate', values: [50, 30, 60, 40, 70] },
        { name: 'Disfluency Rate', values: [5, 10, 15, 2, 25] },
        { name: 'Pitch Variation', values: [40, 50, 70, 20, 90] }
    ];

    const chartRef = useRef(null);

    useEffect(() => {
        const ctx = document.getElementById('myChart').getContext('2d');
        const labels = Array.from({ length: metricsData[0].values.length }, (_, i) => i + 1); // Generate labels from 1 to n
        const datasets = [];

        // Calculate the average incrementally for each point across all metrics
        for (let i = 0; i < labels.length; i++) {
            let sum = 0;
            metricsData.forEach(metric => {
                sum += metric.values[i];
            });
            const average = sum / 4;
            datasets.push(average.toFixed(2));
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
        });
    }, []);

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
