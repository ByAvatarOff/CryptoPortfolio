import { useContext, useState, useEffect } from 'react';
import { FC } from 'react';
import { requestTemplate } from '../../request/axiosRequest';
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
    }, [setInvestments, portfolioId]);

    useEffect(() => {
        requestTemplate.get(`api/binance/ticker_price_changed/${portfolioId}`).then((response) => {
            setPriceChange(response.data.data)
        })
            .catch((error) => {
                console.error("Error occured with get tickers prices", error);
            });
    }, [portfolioId]);

    useEffect(() => {
        const access = localStorage.getItem('access');
        const socket = new WebSocket(`ws://127.0.0.1:8000/api/binance/ws/${portfolioId}/${access}`);

        socket.onmessage = function (event) {
            let data = JSON.parse(event.data);
            setPrices(prevPrices => {
                const index = findTickerPriceInPrices(prevPrices, data.ticker);
                if (index === -1) {
                    return [...prevPrices, data];
                }
                const updatedPrices = [...prevPrices];
                updatedPrices[index] = data;
                return updatedPrices;
            });
        };

        socket.onerror = function (event) {
            socket.close();
        };

        socket.onclose = function (event) {
            socket.close();
        };

        return () => {
            socket.close();
        };
    }, [portfolioId]);

    const findTickerPriceInPrices = (list_prices: PriceData[], ticker: string) => {
        return list_prices.findIndex(price => price.ticker === ticker);
    };

    const findTickerPriceInChanges = (list_changes: TimeFrameChangesList[], ticker: string) => {
        return list_changes.findIndex(change => change.ticker === ticker);
    };

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
                        <tr key={index}>
                            <td>{investment.ticker}</td>
                            <td>{investment.amount_difference}</td>
                            <td>{investment.avg_price}</td>
                            <td>{investment.price_difference}</td>
                            <td>{prices[findTickerPriceInPrices(prices, investment.ticker)]?.price}</td>
                            <td>{priceChange.timeframe_1d[findTickerPriceInChanges(priceChange.timeframe_1d, investment.ticker)]?.percent}</td>
                            <td>{priceChange.timeframe_7d[findTickerPriceInChanges(priceChange.timeframe_7d, investment.ticker)]?.percent}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default ListInvestmentsComponent;