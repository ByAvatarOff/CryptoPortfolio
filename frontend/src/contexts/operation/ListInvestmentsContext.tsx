import { createContext, useState, Dispatch, SetStateAction, ReactNode, FC } from 'react';
import { InvestmentType } from '../../types/portfolio/types';


type ListInvestmentsStateType = {
  investments: InvestmentType[] | undefined
  setInvestments: Dispatch<SetStateAction<InvestmentType[] | undefined>>
};

type ListInvestmentsProviderProps = {
  children: ReactNode
}

const defaultState = {
  investments: [],
  setInvestments: (investments: InvestmentType[]) => { }
} as ListInvestmentsStateType

export const ListInvestmentsContext = createContext<ListInvestmentsStateType>(defaultState);

export const ListInvestmentsContextProvider: FC<ListInvestmentsProviderProps> = ({ children }) => {
  const [investments, setInvestments] = useState<InvestmentType[] | undefined>([]);

  return (
    <ListInvestmentsContext.Provider value={{ investments, setInvestments }}>
      {children}
    </ListInvestmentsContext.Provider>
  );
};
