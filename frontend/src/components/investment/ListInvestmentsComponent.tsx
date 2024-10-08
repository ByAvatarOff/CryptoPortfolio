import { useContext, useState, useEffect } from 'react';
import { Chart, ArcElement } from 'chart.js'
import { FC } from 'react';
import { requestTemplate } from '../../request/axiosRequest';
import ChartDoughnutComponent from './ChartDoughnutComponent';
import { PriceData, TimeFrameChanges, TimeFrameChangesList } from '../../types/portfolio/types';
import { ListInvestmentsContext } from '../../contexts/operation/ListInvestmentsContext';
import { PortfolioIdProps } from '../../types/portfolio/types';


const ListInvestmentsComponent: FC<PortfolioIdProps> = ({ portfolioId }) => {
    const [prices, setPrices] = useState<PriceData[]>([]);
    const [priceChange, setPriceChange] = useState<TimeFrameChanges>({ "timeframe_1d": [], "timeframe_7d": [] });
    const { investments, setInvestments } = useContext(ListInvestmentsContext);

    useEffect(() => {
        requestTemplate.get(`api/investment/list_tickers_stat/${portfolioId}`).then((response) => {
            setInvestments(response.data);
        })
            .catch((error) => {
                console.error("Error occured with get list tickers stat", error);
            });
    }, [setInvestments]);

    useEffect(() => {
        requestTemplate.get(`api/binance/ticker_price_changed/${portfolioId}`).then((response) => {
            setPriceChange(response.data.data)
        })
        .catch((error) => {
            console.error("Error occured with get tickers prices", error);
        });
    }, []);

    const access = localStorage.getItem('access')

    const socket = new WebSocket(`ws://127.0.0.1:8000/api/binance/ws/${access}`);
    socket.onmessage = function (event) {
        let data = JSON.parse(event.data)
        setPrices(prevPrices => {
            const index = findTickerPrice(prevPrices, data.ticker)
            if (index === 0) {
                return [...prevPrices, data];
            }
            const updatedPrices = [...prevPrices];
            updatedPrices[index].price = data.price;
            return updatedPrices;

        });
    };
    socket.onerror = function (event) {
        socket.close()
    };

    socket.onclose = function (event) {
        socket.close()
    };
    
    // Chart.register(ArcElement);

    const findTickerPrice = (list_prices: PriceData[] | TimeFrameChangesList[], ticker: string) => {
        if (list_prices.length === 0) return 0
        const index = list_prices.findIndex(price => price.ticker === ticker);
        if (index === -1) {
            return 0
        }
        return index
    }

    return (
        <div>
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
                    </tr>
                </thead>
                <tbody>
                    {investments?.map((investment, index) => (
                        <tr>
                            <td><span key={index}>{investment.ticker}</span></td>
                            <td><span key={index}>{investment.amount_difference}</span></td>
                            <td><span key={index}>{investment.avg_price}</span></td>
                            <td><span key={index}>{investment.price_difference}</span></td>
                            <td><span key={index}>{(prices[findTickerPrice(prices, investment.ticker)]?.price)}</span></td>
                            <td><span key={index}>{(priceChange.timeframe_1d[findTickerPrice(priceChange.timeframe_1d, investment.ticker)]?.percent)}</span></td>
                            <td><span key={index}>{(priceChange.timeframe_7d[findTickerPrice(priceChange.timeframe_7d, investment.ticker)]?.percent)}</span></td>
                        </tr>
                    ))}

                </tbody>
            </table>
            {/* <ChartDoughnutComponent /> */}
        </div >
    )
}

export default ListInvestmentsComponent;
