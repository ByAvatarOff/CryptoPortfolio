import { FC, useEffect, useContext, useState } from 'react';
import { PortfolioPriceContext } from "./contexts/OnlinePortfolioPriceContext";
import { SetPortfolioPrice } from "../../request/request";
import { PortfolioPrices } from "./types";


const SelectPeriodprofitComponent: FC = () => {
    const { prices, setPrices } = useContext(PortfolioPriceContext);
    useEffect(() => {
        SetPortfolioPrice({ prices, setPrices })
    }, []);

    const AllTimeProfitColor = (prices: PortfolioPrices | undefined) => {
        let total_profit = prices?.total_profit ? prices.total_profit : 0
        return total_profit > 0 ? 'green' : 'red'
    }

    const ButtonPeriodHandler = (event: React.MouseEvent<HTMLElement>) => {
        SetPortfolioPrice({ prices, setPrices }, (event.target as HTMLInputElement).value)
    }

    return (
        <div className="container">

            <div className="container">
                <h2>Total price: {prices?.portfolioPrice?.toFixed(2)}$</h2>
            </div>
            <div className="container">
                <button value="1m" onClick={ButtonPeriodHandler}>All</button>
                <button value="1h" className='mx-2' onClick={ButtonPeriodHandler}>1h</button>
                <button value="1d" onClick={ButtonPeriodHandler}>1d</button>
                <button value="7d" className='mx-2' onClick={ButtonPeriodHandler}>7d</button>
            </div>

            <div className="container mx-3 my-3" style={{ backgroundColor: "#F5FFFA", width: '13%' }}>
                <span style={{ fontSize: "20px" }}>Your profit: </span><br />
                <span style={{ fontSize: "20px", color: AllTimeProfitColor(prices) }}>{prices?.total_profit?.toFixed(2)}$</span>
            </div>

        </div>

    )
}

export default SelectPeriodprofitComponent;