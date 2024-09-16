import { Routes, Route } from 'react-router-dom';

import { Layout } from './components/auth/Layout';
import LoginComponent from './components/auth/LoginComponent';
import { LoginButtonContextProvider } from './contexts/auth/LoginButtonContext';
import MainComponent from './components/MainComponent'
import { ListOperationContextProvider } from './contexts/operation/ListOperationContext';
import { ListInvestmentsContextProvider } from './contexts/operation/ListInvestmentsContext';
import { PortfolioPriceContextProvider } from './contexts/operation/OnlinePortfolioPriceContext';
import { ListPortfolioContextProvider } from './contexts/portfolio/ListPortfolioContext';


const App = () => {
  return (
    <ListPortfolioContextProvider>
      <LoginButtonContextProvider>
        <ListOperationContextProvider>
          <ListInvestmentsContextProvider>
            <PortfolioPriceContextProvider>
              <Routes>
                <Route path="/" element={<Layout />}>
                  <Route path="login" element={<LoginComponent />} />
                  <Route path="/" element={<MainComponent />} />
                </Route>
              </Routes>
            </PortfolioPriceContextProvider>
          </ListInvestmentsContextProvider>
        </ListOperationContextProvider>
      </LoginButtonContextProvider>
    </ListPortfolioContextProvider>
  );
}

export default App;
