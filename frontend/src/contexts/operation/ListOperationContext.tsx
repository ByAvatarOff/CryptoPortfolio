import { createContext, useState, Dispatch, SetStateAction, ReactNode } from 'react';
import { OperationType } from '../../types/operation/types';


type ListOperationStateType = {
  operations: OperationType[] | undefined
  setOperations: Dispatch<SetStateAction<OperationType[] | undefined>>
};

type ListOperationProviderProps = {
  children: ReactNode
}

const defaultState = {
  operations: [],
  setOperations: (operations: OperationType[]) => { }
} as ListOperationStateType

export const ListOperationContext = createContext<ListOperationStateType>(defaultState);

export const ListOperationContextProvider = ({ children }: ListOperationProviderProps) => {
  const [operations, setOperations] = useState<OperationType[] | undefined>([]);

  return (
    <ListOperationContext.Provider value={{ operations, setOperations }}>
      {children}
    </ListOperationContext.Provider>
  );
};
