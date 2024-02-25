import { requestTemplate } from "../../request/axiosRequest";
import { FormEvent, FC, useContext, useState, useEffect, MouseEvent } from 'react';
import { ListOperationContext } from "./contexts/ListOperationContext";
import { OperationType } from "./types";
import { SetListInvestmentsHook, SetPortfolioPrice } from "../../request/request";
import { ListInvestmentsContext } from "./contexts/ListInvestmentsContext";
import { PortfolioPriceContext } from "./contexts/OnlinePortfolioPriceContext";



const CreateOperationComponent: FC = () => {
    const { investments, setInvestments } = useContext(ListInvestmentsContext);
    const { operations, setOperations } = useContext(ListOperationContext);
    const { prices, setPrices } = useContext(PortfolioPriceContext);
    const [listTickers, setListTickers] = useState<Array<string>>();
    const [operationData, setOperationData] = useState<OperationType>({
        'ticker': '',
        'amount': 0,
        'price': 0,
        'type': '',
        'user_id': 0
    });

    useEffect(() => {
        requestTemplate.get('api/binance/list_all_tickers/').then((response) => {
            setListTickers(response.data);
        });
    }, []);


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
        let data_obj: OperationType = {
            'ticker': operationData.ticker,
            'amount': operationData.amount,
            'price': operationData.price,
            'type': operationData.type,
            'user_id': 0
        }
        requestTemplate.post('api/portfolio/create_operation/', data_obj)
            .then(response => {
                setOperations(response.data)
                SetListInvestmentsHook({ investments, setInvestments })
                SetPortfolioPrice({ prices, setPrices })

            })
            .catch(error => {
                error.response.status === 400 ? alert('You cant to sell more than buy') : alert(error)
            });
    };


    return (
        <div id="defport" className="collapse">
            <div className="container" style={{ backgroundColor: "#F5FFFA" }}>
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
