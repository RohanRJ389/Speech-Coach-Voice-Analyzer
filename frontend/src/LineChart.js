import { useEffect, useState } from 'react';
import { Line } from 'react-chartjs-2';
import { Chart, LinearScale } from 'chart.js/auto';
import jsonDataFile from './metrics.json';


Chart.register(LinearScale);

const LineChart = () => {

  const [jsonData, setJsonData] = useState({});
  const [metricsData, setMetricsData] = useState(
      [0, 0, 0, 0, 0, 0,0,0,0,0, 0, 0,0,0,0,0]
  );
  function fetchJSONData() {
      setJsonData(JSON.parse(JSON.stringify(jsonDataFile)))

      setMetricsData(prev => {

          prev.shift()
          prev.push(parseFloat(jsonData["master_score"]))

          return prev
      })

  }
  useEffect(() => {
      let intrvl = setInterval(fetchJSONData, 2000);

      return () => {
          clearInterval(intrvl)
      }
  })


  const data = {
    labels: ['.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.'],
    datasets: [
      {
        label: 'Master score',
        data: metricsData,
        fill: false,
        borderColor: 'rgba(75, 192, 192, 0.6)',
        tension: 1,
      }
    ],
  };

  const options = {
    scales: {
      y: {
        beginAtZero: true,
      },
    },
  };

  return (
    <div>
      <h2>{jsonData["tip"]}</h2>
      
      <Line data={data} options={options} />
    </div>
  );
};

export default LineChart;