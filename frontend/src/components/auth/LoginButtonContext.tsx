import {
  createContext,
  useState,
  Dispatch,
  SetStateAction,
  ReactNode
} from 'react';


type ContextType = {
  loginButton: boolean
  setLoginButton: Dispatch<SetStateAction<boolean>>
};

type ButtonProviderProps = {
  children: ReactNode
}

const defaultState = {
  loginButton: false,
  setLoginButton: (loginButton: boolean) => { }
} as ContextType

export const LoginButtonContext = createContext<ContextType>(defaultState);

export const LoginButtonContextProvider = ({ children }: ButtonProviderProps) => {
  let access: string | null = localStorage.getItem('access')
  const [loginButton, setLoginButton] = useState<boolean>(Boolean(access));

  return (
    <LoginButtonContext.Provider value={{ loginButton, setLoginButton }}>
      {children}
    </LoginButtonContext.Provider>
  );
};