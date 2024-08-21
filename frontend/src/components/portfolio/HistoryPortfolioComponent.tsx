import { useContext } from 'react';
import { Line } from "react-chartjs-2";
import { FC } from 'react';
import { ListOperationContext } from './contexts/ListOperationContext';

import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
} from 'chart.js';


const HistoryPortfolioComponent: FC = () => {
    const ListOperation = useContext(ListOperationContext);
    const addDates = ListOperation.operations?.map(item => new Date(item.add_date).toDateString());
    const collectPricesForChart = (): number[] => {
        let total = 0;
        return ListOperation.operations?.map((object) => {
            object.type === 'buy' ?
            total += object.price * object.amount :
            total -= object.price * object.amount;
            return total;
        }) || [];
    };

    ChartJS.register(
        CategoryScale,
        LinearScale,
        PointElement,
        LineElement,
    );

    const options = {
        responsive: false,
        tension: 0.3,
    };

    let labels = addDates

    const data = {
        labels,
        datasets: [
            {
                data: collectPricesForChart(),
                borderColor: "rgb(53, 162, 235)",
                backgroundColor: "rgba(53, 162, 235, 0.3)",
                fill: "origin"
            }
        ]
    };

    return (
        <div id="currstat" className="collapse">
            <div className='mt-3 mb-5'>
                <Line options={options} height={500} width={800} data={data} />
            </div>
        </div >

    )
}

export default HistoryPortfolioComponent;
