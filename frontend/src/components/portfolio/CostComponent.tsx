import CreateOperationComponent from "./CreateOperationComponent";
import { FC } from 'react';
import ListOperationsComponent from "./ListOperationsComponent";
import ListInvestmentsComponent from "./ListInvestmentsComponent";
import SelectPeriodprofitComponent from "./SelectPeriodProfitComponent";
import HistoryPortfolioComponent from "./HistoryPortfolioComponent";



const CustomCostComponent: FC = () => {
  return (
    <div className="container">
      <SelectPeriodprofitComponent />

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

      <div className="row">
        <button type="button" className="btn btn-success csdata" data-toggle="collapse"
          data-target="#currstat">Balance history</button>
      </div>
      <HistoryPortfolioComponent />

    </div>

  )
}

export default CustomCostComponent;
