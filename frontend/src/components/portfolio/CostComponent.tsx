import CreateOperationComponent from "./CreateOperationComponent";
import { FC, useEffect, useContext } from 'react';
import ListOperationsComponent from "./ListOperationsComponent";
import ListInvestmentsComponent from "./ListInvestmentsComponent";
import { requestTemplate } from "../../request/axiosRequest";
import { PortfolioPriceContext } from "./contexts/OnlinePortfolioPriceContext";
import { SetPortfolioPrice } from "../../request/request";


const CustomCostComponent: FC = () => {
  const { portfolioPrice, setPortfolioPrice } = useContext(PortfolioPriceContext);
  useEffect(() => {
    SetPortfolioPrice({ portfolioPrice, setPortfolioPrice })
  }, []);


  return (
    <div className="container">
      <h2>Total price: {portfolioPrice?.toFixed(2)}$</h2>
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