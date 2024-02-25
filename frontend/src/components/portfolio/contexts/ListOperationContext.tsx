import {
  createContext,
  useState,
  Dispatch,
  SetStateAction,
  ReactNode
} from 'react';
import { OperationsType } from '../types';


type ListOperationStateType = {
  operations: OperationsType | undefined
  setOperations: Dispatch<SetStateAction<OperationsType | undefined>>
};

type ListOperationProviderProps = {
  children: ReactNode
}

const defaultState = {
  operations: [{}],
  setOperations: (operations: OperationsType) => { }
} as ListOperationStateType

export const ListOperationContext = createContext<ListOperationStateType>(defaultState);

export const ListOperationContextProvider = ({ children }: ListOperationProviderProps) => {

  const [operations, setOperations] = useState<OperationsType | undefined>([{
    id: 0,
    ticker: '',
    amount: 0,
    price: 0,
    add_date: '',
    type: '',
    user_id: 0,
  }]);

  return (
    <ListOperationContext.Provider value={{ operations, setOperations }}>
      {children}
    </ListOperationContext.Provider>
  );
};
