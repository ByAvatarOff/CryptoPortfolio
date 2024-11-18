import {requestTemplate} from "../../request/axiosRequest";
import React, {FormEvent, FC, useContext, useState, useEffect} from 'react';
import {ListOperationContext} from "../../contexts/operation/ListOperationContext";
import {CreateOperationType, OperationType} from "../../types/operation/types";
import '../../styles/operation/CreateOperation.css';
import Select from 'react-select';


interface PortfolioCreateComponentProps {
    portfolioId: number | null;
    isOpen: boolean;
    onClose: () => void;
}


const CreateOperationComponent: FC<PortfolioCreateComponentProps> = ({portfolioId, isOpen, onClose}) => {
    const {operations, setOperations} = useContext(ListOperationContext);
    const [listTickers, setListTickers] = useState<Array<string>>([]);
    const [filteredTickers, setFilteredTickers] = useState<Array<string>>([]);
    const [operationData, setOperationData] = useState<CreateOperationType>({
        ticker: "",
        amount: 0,
        price: 0,
        type: "",
        portfolio_id: 0,
    });

    useEffect(() => {
        requestTemplate.get('api/binance/list_all_tickers/')
            .then((response) => {
                const initialTickers = response.data.slice(0, 10); // Показать первые 10 тикеров по умолчанию
                setListTickers(response.data);
                setFilteredTickers(initialTickers);
            })
            .catch(error => console.log(error));
    }, []);

    if (!isOpen) return null;

    const handleTickerChange = (event: FormEvent<HTMLInputElement>) => {
        const value = (event.target as HTMLInputElement).value;
        setOperationData({...operationData, ticker: value});

        // Фильтрация списка тикеров по введенному значению
        const filtered = listTickers.filter((ticker) =>
            ticker.toLowerCase().includes(value.toLowerCase())
        ).slice(0, 10); // Ограничение вывода до 10 вариантов
        setFilteredTickers(filtered);
    };

    const handleAmountChange = (event: FormEvent<HTMLInputElement>) => {
        setOperationData({...operationData, 'amount': Number((event.target as HTMLInputElement).value)});
    };

    const handlePriceChange = (event: FormEvent<HTMLInputElement>) => {
        setOperationData({...operationData, 'price': Number((event.target as HTMLInputElement).value)});
    };

    const handleTypeChange = (event: FormEvent<HTMLSelectElement>) => {
        setOperationData({...operationData, 'type': (event.target as HTMLSelectElement).value});
    };

    const submitHandler = (event: FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        let data_obj: CreateOperationType = {
            ticker: operationData.ticker,
            amount: operationData.amount,
            price: operationData.price,
            type: operationData.type,
            portfolio_id: portfolioId!
        }
        requestTemplate.post('api/portfolio/operation/', data_obj)
            .then(response => {
                const newOperation: OperationType = response.data;
                setOperations((prevOperations) => (prevOperations ? [...prevOperations, newOperation] : [newOperation]));
                onClose();
            })
            .catch(error => {
                error.response.status === 400 ? alert('You cant to sell more than buy') : alert(error)
            });
    };

    return (
        <div className="create-operation-modal">
            <div className="create-operation-modal-content">
                <span className="create-operation-close-button" onClick={onClose}>&times;</span>
                <form onSubmit={submitHandler}>
                    <div className="create-operation-form-group">
                        <label className="create-operation-label" htmlFor="ticker">Ticker</label>
                        <input
                            className="create-operation-form-control"
                            list="tickers"
                            type="text"
                            id="ticker"
                            name="ticker"
                            value={operationData.ticker}
                            placeholder="Start type ticker name..."
                            onChange={handleTickerChange}
                        />
                        <datalist id="tickers">
                            {filteredTickers.map((ticker, index) => (
                                <option key={index} value={ticker}/>
                            ))}
                        </datalist>
                    </div>
                    <div className="create-operation-form-group">
                        <label className="create-operation-label" htmlFor="amount">Amount</label>
                        <input
                            className="create-operation-form-control"
                            type="number"
                            id="amount"
                            name="amount"
                            value={operationData.amount}
                            onChange={handleAmountChange}
                        />
                    </div>
                    <div className="create-operation-form-group">
                        <label className="create-operation-label" htmlFor="price">Price</label>
                        <input
                            className="create-operation-form-control"
                            type="number"
                            id="price"
                            name="price"
                            value={operationData.price}
                            onChange={handlePriceChange}
                        />
                    </div>
                    <div className="create-operation-form-group">
                        <label className="create-operation-label" htmlFor="type">Type Operation</label>
                        <select
                            className="create-operation-select"
                            defaultValue="BUY"
                            onChange={handleTypeChange}
                        >
                            <option value="BUY">Choose type</option>
                            <option value="BUY">Buy</option>
                            <option value="SELL">Sell</option>
                        </select>
                    </div>
                    <div className="create-operation-form-group">
                        <button type="submit" className="create-operation-submit-button">
                            Add transaction
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default CreateOperationComponent;
