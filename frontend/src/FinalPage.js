// Charts.js
import React from 'react';
import LineChart from './LineChartFinal';
import DoughnutChart from './DoughnutChart';
import PlaceholderButton from './PlaceHolderButton';

const Charts = () => {
    return (
        <div style={{backgroundColor:"honeydew"}}>
            <h2>Line Chart</h2>
            <LineChart />
            <h2>Doughnut Chart</h2>
            <DoughnutChart />
            <PlaceholderButton/>
        </div>
    );
};

export default Charts;
