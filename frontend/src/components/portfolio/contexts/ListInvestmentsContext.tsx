import {
  createContext,
  useState,
  Dispatch,
  SetStateAction,
  ReactNode
} from 'react';
import { ListInvestments } from '../types';


type ListInvestmentsStateType = {
  investments: ListInvestments | undefined
  setInvestments: Dispatch<SetStateAction<ListInvestments | undefined>>
};

type ListInvestmentsProviderProps = {
  children: ReactNode
}

const defaultState = {
  investments: [{}],
  setInvestments: (investments: ListInvestments) => { }
} as ListInvestmentsStateType

export const ListInvestmentsContext = createContext<ListInvestmentsStateType>(defaultState);

export const ListInvestmentsContextProvider = ({ children }: ListInvestmentsProviderProps) => {

  const [investments, setInvestments] = useState<ListInvestments | undefined>([{
    ticker: '',
    amount_difference: 0,
    price_difference: 0,
    avg_price: 0
  }]);

  return (
    <ListInvestmentsContext.Provider value={{ investments, setInvestments }}>
      {children}
    </ListInvestmentsContext.Provider>
  );
};