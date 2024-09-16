import { requestTemplate } from "../../request/axiosRequest";
import { FormEvent, FC, useContext, useState, useEffect, MouseEvent } from 'react';
import { ListOperationContext } from "../../contexts/operation/ListOperationContext";
import { CreateOperationType } from "../../types/operation/types";
import { SetListInvestmentsHook, SetPortfolioPrice } from "../../request/request";
import { PortfolioPriceContext } from "../../contexts/operation/OnlinePortfolioPriceContext";
import { PortfolioIdProps } from '../../types/portfolio/types';
import '../../styles/operation/CreateOperation.css';


interface PortfolioCreateComponentProps {
    portfolioId: number | null;
    isOpen: boolean;
    onClose: () => void;
  }


const CreateOperationComponent: FC<PortfolioCreateComponentProps> = ({ portfolioId, isOpen, onClose }) => {
    const { operations, setOperations } = useContext(ListOperationContext);
    const { prices, setPrices } = useContext(PortfolioPriceContext);
    const [listTickers, setListTickers] = useState<Array<string>>();
    const [operationData, setOperationData] = useState<CreateOperationType>({
        ticker: "",
        amount: 0,
        price: 0,
        type: "",
        portfolio_id: 0,
    });

    if (!isOpen) return null;

    // useEffect(() => {
    //     requestTemplate.get('api/binance/list_all_tickers/').then((response) => {
    //         setListTickers(response.data)
    //     }).catch(error => console.log(error));
    // }, []);


    const handleTickerChange = (event: FormEvent<HTMLInputElement>) => {
        setOperationData({ ...operationData, 'ticker': (event.target as HTMLInputElement).value });
    };
    const handleAmountChange = (event: FormEvent<HTMLInputElement>) => {
        setOperationData({ ...operationData, 'amount': Number((event.target as HTMLInputElement).value) });
    };
    const handlePriceChange = (event: FormEvent<HTMLInputElement>) => {
        setOperationData({ ...operationData, 'price': Number((event.target as HTMLInputElement).value) });
    };
    const handleTypeChange = (event: FormEvent<HTMLSelectElement>) => {
        setOperationData({ ...operationData, 'type': (event.target as HTMLSelectElement).value });
    };

    const submitHandler = (event: FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        let data_obj: CreateOperationType = {
            'ticker': operationData.ticker,
            'amount': operationData.amount,
            'price': operationData.price,
            'type': operationData.type,
            'portfolio_id': 0
        }
        requestTemplate.post('api/portfolio/create_operation/', data_obj)
            .then(response => {
                setOperations(response.data)
                SetPortfolioPrice({ prices, setPrices })

            })
            .catch(error => {
                error.response.status === 400 ? alert('You cant to sell more than buy') : alert(error)
            });
    };

    return (
        <div className="modal">
        <div className="modalContent">
          <span className="closeButton" onClick={onClose}>&times;</span>
                <form onSubmit={submitHandler}>
                    <div className="row">
                        <div className="form-group col-sm-2">
                            <input className="form-control" list="tickers" type="text" id="ticker" value={operationData.ticker} placeholder="Ticker" onChange={handleTickerChange} />
                            <datalist id="tickers">
                                {listTickers?.map((ticker: string, index: number) => (
                                    <option value={ticker} />
                                ))}
                            </datalist>
                        </div>
                        <div className="form-group col-sm-2">
                            <input className="form-control" type="number" id="amount" value={operationData.amount} placeholder="Amount" onChange={handleAmountChange} />
                        </div>
                        <div className="form-group col-sm-2">
                            <input className="form-control" type="number" id="price" value={operationData.price} placeholder="Price(USD)" onChange={handlePriceChange} />
                        </div>
                        <div className="form-group col-sm-2">
                            <select className="form-control" defaultValue="Buy" onChange={handleTypeChange}>
                                <option value="buy">Choose type</option>
                                <option value="buy">Buy</option>
                                <option value="sell">Sell</option>
                            </select>
                        </div>
                        <div className="form-group col-sm-2">
                            <button type="submit" className="btn btn-dark add-row form-control">Add Row</button>
                        </div>
                    </div>
                </form>
            </div>
        </div>
    )
}

export default CreateOperationComponent;
