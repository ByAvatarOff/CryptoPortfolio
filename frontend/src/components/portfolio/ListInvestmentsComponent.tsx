import { useContext, useState } from 'react';
import { Chart, ArcElement } from 'chart.js'
import { FC } from 'react';
import { ListInvestmentsContext } from './contexts/ListInvestmentsContext';
import { WSPrices } from './types';
import ChartDoughnutComponent from './ChartDoughnutComponent';

interface PriceData {
    ticker: string;
    price: number;
  }

const ListInvestmentsComponent: FC = () => {
    const [prices, setPrices] = useState<PriceData[]>([]);

    const access = localStorage.getItem('access')
    const socket = new WebSocket(`ws://127.0.0.1:8000/api/binance/ws/${access}`);
    socket.onmessage = function (event) {
        let data = JSON.parse(event.data)
        setPrices(prevPrices => {
            const index = prevPrices.findIndex(price => price.ticker === data.ticker);
            if (index !== -1) {
              const updatedPrices = [...prevPrices];
              updatedPrices[index].price = data.price;
              return updatedPrices;
            } else {
              return [...prevPrices, data];
            }
        });
    };
    socket.onerror = function (event) {
        socket.close()
    };

    socket.onclose = function (event) {
        socket.close()
    };

    const { investments, setInvestments } = useContext(ListInvestmentsContext);
    Chart.register(ArcElement);

    return (
        <div id="portsummary" className="collapse">
            <br />
            <table id="pstable" className="table">
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Amount</th>
                        <th>Average price with sells</th>
                        <th>Money spent</th>
                        <th>Current Price</th>
                        <th>24h Changed</th>
                        <th>7d Changed</th>
                        <th>30d Changed</th>
                    </tr>
                </thead>
                <tbody>
                    {investments?.map((investment, index) => (
                        <tr>
                            <td><span key={index}>{investment.ticker}</span></td>
                            <td><span key={index}>{investment.amount_difference}</span></td>
                            <td><span key={index}>{investment.avg_price}</span></td>
                            <td><span key={index}>{investment.price_difference}</span></td>
                            <td><span key={index}>{(prices[index]?.price)?.toFixed(4)}</span></td>
                        </tr>
                    ))}

                </tbody>
            </table>
            <ChartDoughnutComponent />
        </div >
    )
}

export default ListInvestmentsComponent;
