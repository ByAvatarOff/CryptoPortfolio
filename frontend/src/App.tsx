import { Routes, Route } from 'react-router-dom';

import { Layout } from './components/auth/Layout';
import LoginComponent from './components/auth/LoginComponent';
import { LoginButtonContextProvider } from './components/auth/LoginButtonContext';
import CustomCostComponent from './components/portfolio/CostComponent'
import { ListOperationContextProvider } from './components/portfolio/contexts/ListOperationContext';
import { ListInvestmentsContextProvider } from './components/portfolio/contexts/ListInvestmentsContext';
import { PortfolioPriceContextProvider } from './components/portfolio/contexts/OnlinePortfolioPriceContext';


const App = () => {
  return (
    <LoginButtonContextProvider>
      <ListOperationContextProvider>
        <ListInvestmentsContextProvider>
          <PortfolioPriceContextProvider>
            <Routes>
              <Route path="/" element={<Layout />}>
                <Route path="login" element={<LoginComponent />} />
                <Route path="/" element={<CustomCostComponent />} />
              </Route>
            </Routes>
          </PortfolioPriceContextProvider>
        </ListInvestmentsContextProvider>
      </ListOperationContextProvider>
    </LoginButtonContextProvider>

  );
}

export default App;