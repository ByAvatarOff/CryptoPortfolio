import CreateOperationComponent from "./CreateOperationComponent";
import { FC, useEffect, useContext } from 'react';
import ListOperationsComponent from "./ListOperationsComponent";
import ListInvestmentsComponent from "./ListInvestmentsComponent";
import { requestTemplate } from "../../request/axiosRequest";
import { PortfolioPriceContext } from "./contexts/OnlinePortfolioPriceContext";
import { SetPortfolioPrice } from "../../request/request";
import { PortfolioPrices } from "./types";



const CustomCostComponent: FC = () => {
  const { prices, setPrices } = useContext(PortfolioPriceContext);
  useEffect(() => {
    SetPortfolioPrice({ prices, setPrices })
  }, []);

  const AllTimeProfitColor = (prices: PortfolioPrices | undefined) => {
    let total_profit = prices?.total_profit ? prices.total_profit : 0
    if (total_profit > 0) {
      return 'green'
    }
    return 'red'
  }


  return (
    <div className="container">
      <div className="">
        <div className="container">
          <h2>Total price: {prices?.portfolioPrice?.toFixed(2)}$</h2>
        </div>
        <div className="container mx-3 my-3" style={{ backgroundColor: "#F5FFFA", width: '13%' }}>
          <span style={{ fontSize: "20px" }}>Your profit: </span><br />
          <span style={{ fontSize: "20px", color: AllTimeProfitColor(prices) }}>{prices?.total_profit?.toFixed(2)}$</span>
        </div>
      </div>

      <div className="row">
        <button type="button" id="addTickers" className="btn btn-success" data-toggle="collapse" data-target="#defport">Add coin to portfolio</button>
      </div>
      <br />
      <CreateOperationComponent />
      <ListOperationsComponent />

      <div className="row">
        <button type="button" className="btn btn-success psdata" data-toggle="collapse"
          data-target="#portsummary">Investments Summary</button>
      </div>
      <ListInvestmentsComponent />

      <br />

      {/* <div className="row">
                <button type="button" className="btn btn-success csdata" data-toggle="collapse"
                    data-target="#currstat">Investments Status</button>
            </div> */}
      {/* <InvestmentStatusComponent /> */}

    </div>

  )
}

export default CustomCostComponent;