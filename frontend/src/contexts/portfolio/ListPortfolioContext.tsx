import { createContext, useState, Dispatch, SetStateAction, ReactNode, FC } from 'react';
import { PortfolioType } from '../../types/portfolio/types';

type ListPortfolioStateType = {
  portfolios: PortfolioType[] | undefined;
  setPortfolios: Dispatch<SetStateAction<PortfolioType[] | undefined>>;
};

type ListPortfolioProviderProps = {
  children: ReactNode;
};

const defaultState = {
  portfolios: [],
  setPortfolios: (portfolios: PortfolioType[]) => {}
} as ListPortfolioStateType;

export const ListPortfolioContext = createContext<ListPortfolioStateType>(defaultState);

export const ListPortfolioContextProvider: FC<ListPortfolioProviderProps> = ({ children }) => {
  const [portfolios, setPortfolios] = useState<PortfolioType[] | undefined>([]);

  return (
    <ListPortfolioContext.Provider value={{ portfolios, setPortfolios }}>
      {children}
    </ListPortfolioContext.Provider>
  );
};