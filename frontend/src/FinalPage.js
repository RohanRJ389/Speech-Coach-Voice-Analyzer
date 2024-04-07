// Charts.js
import React, { useEffect, useState } from 'react';
import LineChart from './LineChartFinal';
import DoughnutChart from './DoughnutChart';
import PlaceholderButton from './PlaceHolderButton.js';
import html2canvas from 'html2canvas';
import jsPDF from 'jspdf';
import jsonDataFile from './metrics.json';

let jsonData = JSON.parse(JSON.stringify(jsonDataFile))


const Charts = () => {

    const [exporting, setExporting] = useState(false);

    const exportPDF = () => {
        setExporting(true);
        const input = document.getElementById('charts-content');
        html2canvas(input)
            .then((canvas) => {
                const pdf = new jsPDF('p', 'mm', 'a4');
                pdf.addImage(canvas.toDataURL('image/png'), 'PNG', 0, 0, 210, 297);
                pdf.save('charts.pdf');
                setExporting(false);
            });
    };


    const [finalmasterScore, setfinalmasterScore] = useState(30)

    
    const scorefetcher =  async ()=>{
        const response = await fetch("http://127.0.0.1:5000/finalScore");
        const dt = await response.text();
        setfinalmasterScore(parseFloat(dt))
    }

    useEffect(() => {
      scorefetcher()
    
    
    }, [])
    

  

    return (
        <div id="charts-content" style={{ backgroundColor: "honeydew" }}>
            <div style={{ display: "flex", flexDirection: "row",justifyContent : "space-between" }} >
            <h5 style={{color : "black" , margin : 50}} >Name : Sathvik Malgikar</h5>
            <h5 style={{color : "black" , margin : 50}} >Date : 7th April 2024</h5>

            </div>
            <div style={{ display: "flex", flexDirection: "row",justifyContent : "space-evenly" }}>
                
                <div style={{ color: "black" }} >
                    <br></br>
                    <br></br>
                    <br></br>
           Intensity : {jsonData["intensity"]*100}% <br></br>
           Pitch Variation : {jsonData["pitch_variation"]*100}%<br></br>
           Fluency Rate : {jsonData["fluency_rate"]*100}%<br></br>
                    Speech Rate : {jsonData["speech_rate"] * 100} WPM

                    <h4>Remarks :   </h4>     
              <h7>   {  jsonData["tip"]}</h7>
                     
            </div>
                <div>

                <h2 style={{ color: "black" }} >Line Chart</h2>
            <LineChart />

                </div>
                <div>

            <h2 style={{color:"black"}} >Doughnut Chart</h2>
            <DoughnutChart />
                </div>
            </div>
            <h4 style={{ color: "black" }} >Your final master score has been { finalmasterScore * 100}% </h4>
            <PlaceholderButton />
            
            {!exporting && <button onClick={exportPDF}>Export to PDF</button>}
        </div>
    );
};

export default Charts;





