import {
  createContext,
  useState,
  Dispatch,
  SetStateAction,
  ReactNode
} from 'react';

import { PortfolioPrices } from '../types';


type PortfolioPriceStateType = {
  prices: PortfolioPrices | undefined
  setPrices: Dispatch<SetStateAction<PortfolioPrices | undefined>>
};

type PortfolioPriceProviderProps = {
  children: ReactNode
}

const defaultState = {
  prices: {},
  setPrices: (prices: PortfolioPrices) => { }
} as PortfolioPriceStateType

export const PortfolioPriceContext = createContext<PortfolioPriceStateType>(defaultState);

export const PortfolioPriceContextProvider = ({ children }: PortfolioPriceProviderProps) => {

  const [prices, setPrices] = useState<PortfolioPrices | undefined>({
    portfolioPrice: 0,
    total_profit: 0
  });

  return (
    <PortfolioPriceContext.Provider value={{ prices, setPrices }}>
      {children}
    </PortfolioPriceContext.Provider>
  );
};
