
import LineChart from "./LineChart"

function Metrics() {
 


    return (
        <div>
           
            
       <LineChart></LineChart>
            <div>
                {/* {metricsData.map((metric, index) => (
                    <div key={index}>
                        <p>{metric.name}: {metric.values.join(', ')}</p>
                    </div>
                ))} */}
            </div>
        </div>
    );
}

export default Metrics;
