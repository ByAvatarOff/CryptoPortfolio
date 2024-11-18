import { FC, useState, useEffect } from 'react';
import ListOperationsComponent from "./operations/ListOperationsComponent";
import ListInvestmentsComponent from "./investment/ListInvestmentsComponent";
import PortfolioListComponent from "./portfolio/PortfolioListComponent";
import '../styles/MainComponent.css';
import { requestTemplate } from '../request/axiosRequest';
import ChartDoughnutComponent from './investment/ChartDoughnutComponent';
import HistoryPortfolioComponent from './investment/HistoryPortfolioComponent';


const MainComponent: FC = () => {
  const [selectedTab, setSelectedTab] = useState<string>('operations');
  const [selectedPortfolioId, setSelectedPortfolioId] = useState<number | null>(null);
  const [dynamicText, setDynamicText] = useState<string>('Loading...');
  const [timeFrame, setTimeFrame] = useState<string>('1h');

  useEffect(() => {
    if (selectedPortfolioId !== null) {
      requestTemplate.get(`api/investment/all_time_profit/${selectedPortfolioId}/${timeFrame}/`).then((response) => {
        setDynamicText(response.data.profit);
      }).catch(error => console.log(error));
    }
  }, [selectedPortfolioId, timeFrame]);

  const handleTimeFrameChange = (frame: string) => {
    setTimeFrame(frame);
  };

  let content;
  switch (selectedTab) {
    case 'operations':
      content = [<ListOperationsComponent portfolioId={selectedPortfolioId} />];
      break;
    case 'investments':
      content = [<ListInvestmentsComponent portfolioId={selectedPortfolioId} />];
      break;
    case 'charts':
      content = [
        <ChartDoughnutComponent portfolioId={selectedPortfolioId} />,
        <HistoryPortfolioComponent portfolioId={selectedPortfolioId} />
      ];
      break;
    default:
      content = [<ListOperationsComponent portfolioId={selectedPortfolioId} />];
  }

  return (
    <div className="mainContent">
      <div className="header">
        <div className="profitSection">
          <h2>All Time Profit: </h2>
          <h2>{dynamicText}$</h2>
        </div>
        <div className="timeFrameButtons">
          <button className={timeFrame === '1h' ? 'active' : ''} onClick={() => handleTimeFrameChange('1h')}>1h</button>
          <button className={timeFrame === '1d' ? 'active' : ''} onClick={() => handleTimeFrameChange('1d')}>1d</button>
          <button className={timeFrame === '7d' ? 'active' : ''} onClick={() => handleTimeFrameChange('7d')}>7d</button>
        </div>
      </div>
      <div>
        <PortfolioListComponent onSelectPortfolio={setSelectedPortfolioId} />
        <div className="tabs">
          <div className={`tab ${selectedTab === 'operations' ? 'active' : ''}`} onClick={() => setSelectedTab('operations')}>
            <h3>Operations</h3>
          </div>
          <div className={`tab ${selectedTab === 'investments' ? 'active' : ''}`} onClick={() => setSelectedTab('investments')}>
            <h3>Investments</h3>
          </div>
          <div className={`tab ${selectedTab === 'charts' ? 'active' : ''}`} onClick={() => setSelectedTab('charts')}>
            <h3>Charts</h3>
          </div>
        </div>
      </div>
      <div className="operationsContent">
        {content}
      </div>
    </div>
  );
};

export default MainComponent;