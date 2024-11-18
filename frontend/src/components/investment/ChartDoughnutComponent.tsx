import { useEffect, useContext } from 'react';
import { Doughnut } from "react-chartjs-2";
import { Chart, ArcElement } from 'chart.js'
import { FC } from 'react';
import { ListInvestmentsContext } from '../../contexts/operation/ListInvestmentsContext';
import { PortfolioIdProps } from '../../types/portfolio/types';
import { InvestmentType } from '../../types/portfolio/types';
import { requestTemplate } from '../../request/axiosRequest';
import '../../styles/investment/ChartDoughnut.css';


const ChartDoughnutComponent: FC<PortfolioIdProps> = ({ portfolioId }) => {
    const { investments, setInvestments } = useContext(ListInvestmentsContext);
    Chart.register(ArcElement);

    const tickerPersent = (investment: InvestmentType, investments: InvestmentType[]) => {
        let ticker_price: number = investment.amount_difference * investment.avg_price;
        let sum_prices: number = investments.reduce((sum: number, current: any) => sum + current.price_difference, 0);
        return ((ticker_price / sum_prices) * 100).toFixed(2);
    };

    useEffect(() => {
        if (investments!) {
            requestTemplate.get(`api/investment/list_tickers_stat/${portfolioId}`).then((response) => {
                setInvestments(response.data);
            }).catch((error) => {
                console.error("Error occurred with get list tickers stat", error);
            });
        }
    }, [setInvestments, portfolioId]);

    const backgroundColors = ['#FF6384', '#36A2EB', '#FFCE56'];
    const investmentsWithColors = investments?.map((investment, index) => ({
        ...investment,
        color: backgroundColors[index % backgroundColors.length]
    }));

    return (
        <div className="container">
            <div className="row">
                <div className="col-sm">
                    <Doughnut data={{
                        labels: investmentsWithColors?.map((obj) => obj.ticker),
                        datasets: [{
                            data: investmentsWithColors?.map((obj) => obj.price_difference),
                            backgroundColor: investmentsWithColors?.map((obj) => obj.color),
                            hoverBackgroundColor: investmentsWithColors?.map((obj) => obj.color)
                        }]
                    }} options={{ responsive: false }} height={500} width={500} />
                </div>
                <div className="col-md-auto align-self-center mx-5 mb-5">
                    <ul>
                        {investmentsWithColors?.map((investment, index) => (
                                <div className="ticker-title">
                                    <div className="ticker-name" style={{ backgroundColor: investment.color }}></div>
                                    <h4>{investment.ticker}: {tickerPersent(investment, investmentsWithColors)}%</h4>
                                </div>
                        ))}
                    </ul>
                </div>
            </div>
        </div>
    );
};



export default ChartDoughnutComponent;
