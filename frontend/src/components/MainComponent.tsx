import { FC, useState, useEffect } from 'react';
import ListOperationsComponent from "./operations/ListOperationsComponent";
import ListInvestmentsComponent from "./investment/ListInvestmentsComponent";
import PortfolioListComponent from "./portfolio/PortfolioListComponent";
import '../styles/MainComponent.css';


const MainComponent: FC = () => {
  const [selectedTab, setSelectedTab] = useState<string>('operations');
  const [selectedPortfolioId, setSelectedPortfolioId] = useState<number | null>(null);
  const [dynamicText, setDynamicText] = useState<string>('Loading...');

  let content;
  switch (selectedTab) {
    case 'operations':
      content = <ListOperationsComponent portfolioId={selectedPortfolioId} />;
      break;
    case 'investments':
      content = <ListInvestmentsComponent portfolioId={selectedPortfolioId}  />;
      break;
    case 'createOperation':
      content = <ListInvestmentsComponent portfolioId={selectedPortfolioId}  />;
      break;
    default:
      content = <ListOperationsComponent portfolioId={selectedPortfolioId} />;
  }

  return (
    <div className="mainContent">
      <div className="header">
        <h1>{dynamicText}</h1>
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
          <div className={`tab ${selectedTab === 'createOperation' ? 'active' : ''}`} onClick={() => setSelectedTab('createOperation')}>
            <h3>Create Operation</h3>
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