import { useContext } from 'react';
import { Line } from "react-chartjs-2";
import { FC } from 'react';
import { ListOperationContext } from '../../contexts/operation/ListOperationContext';
import { PortfolioIdProps } from '../../types/portfolio/types';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
} from 'chart.js';


const HistoryPortfolioComponent: FC<PortfolioIdProps> = ({ portfolioId }) => {
    const ListOperation = useContext(ListOperationContext);
    const addDates = ListOperation.operations?.map(item => new Date(item.add_date).toDateString());
    const collectPricesForChart = (): number[] => {
        let total = 0;
        return ListOperation.operations?.map((object) => {
            object.type === 'BUY' ?
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
        <div className='mt-5 mb-5'>
            <Line options={options} height={500} width={800} data={data} />
        </div>

    )
}

export default HistoryPortfolioComponent;
