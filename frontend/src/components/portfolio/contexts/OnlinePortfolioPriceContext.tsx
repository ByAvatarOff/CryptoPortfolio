import {
  createContext,
  useState,
  Dispatch,
  SetStateAction,
  ReactNode
} from 'react';


type PortfolioPriceStateType = {
  portfolioPrice: number | undefined
  setPortfolioPrice: Dispatch<SetStateAction<number | undefined>>
};

type PortfolioPriceProviderProps = {
  children: ReactNode
}

const defaultState = {
  portfolioPrice: 0,
  setPortfolioPrice: (portfolioPrice: number) => { }
} as PortfolioPriceStateType

export const PortfolioPriceContext = createContext<PortfolioPriceStateType>(defaultState);

export const PortfolioPriceContextProvider = ({ children }: PortfolioPriceProviderProps) => {

  const [portfolioPrice, setPortfolioPrice] = useState<number | undefined>(0);

  return (
    <PortfolioPriceContext.Provider value={{ portfolioPrice, setPortfolioPrice }}>
      {children}
    </PortfolioPriceContext.Provider>
  );
};