import { useEffect, useContext } from 'react';
import { Doughnut } from "react-chartjs-2";
import { Chart, ArcElement } from 'chart.js'
import { FC } from 'react';
import { ListInvestmentsContext } from './contexts/ListInvestmentsContext';
import { SetListInvestmentsHook } from '../../request/request';
import { ListInvestments, Investment } from './types';


const ChartDoughnutComponent: FC = () => {

    const { investments, setInvestments } = useContext(ListInvestmentsContext);
    Chart.register(ArcElement);

    useEffect(() => {
        SetListInvestmentsHook({ investments, setInvestments })
    }, []);

    const tickerPersent = (investment: Investment, investments: ListInvestments) => {
        let ticker_price: number = investment.amount_difference * investment.avg_price;
        let sum_prices: number = investments.reduce((sum: number, current: any) => sum + current.price_difference, 0)
        return ((ticker_price / sum_prices) * 100).toFixed(2)
    }

    return (
        <div className="container">
            <div className="row">
                <div className="col-sm">
                    <Doughnut data={{
                        labels: [investments?.map((obj) => {
                            return obj.ticker
                        })],
                        datasets: [{
                            data: investments?.map((obj) => {
                                return obj.price_difference
                            }),

                            backgroundColor: [
                                '#FF6384',
                                '#36A2EB',
                                '#FFCE56'
                            ],
                            hoverBackgroundColor: [
                                '#FF6384',
                                '#36A2EB',
                                '#FFCE56'
                            ]
                        }]
                    }}
                        options={{ responsive: false }} height={500} width={500} />
                </div>
                <div className="col-md-auto align-self-center mx-5 mb-5" style={{ backgroundColor: "#F5FFFA" }}>
                    <ul>
                        {investments?.map((investment, index) => (
                            <li><h4 key={index}>{investment.ticker}: {tickerPersent(investment, investments)}%</h4></li>
                        ))}
                    </ul>
                </div>
            </div>
        </div>
    )
}

export default ChartDoughnutComponent;
