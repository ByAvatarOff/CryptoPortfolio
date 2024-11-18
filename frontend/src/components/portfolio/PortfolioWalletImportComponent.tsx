import React, {ChangeEvent, FC, useContext, useEffect, useState} from 'react';
import {ModalWindowProps} from '../../types/types';
import '../../styles/portfolio/PortfolioWalletImport.css';
import {requestTemplate} from "../../request/axiosRequest";
import {PortfolioType} from "../../types/portfolio/types";
import {ListPortfolioContext} from "../../contexts/portfolio/ListPortfolioContext";


const PortfolioWalletImportComponent: FC<ModalWindowProps> = ({isOpen, onClose}) => {
    const {portfolios, setPortfolios} = useContext(ListPortfolioContext);
    const [walletFields, setWalletFields] = useState([{address: '', blockchain: ''}]);
    const [data, setData] = useState({
        portfolio_image: null as File | null,
        portfolio_name: "",
        waller_data: walletFields
    });

    if (!isOpen) return null;

    const handleAddField = () => {
        setWalletFields([...walletFields, {address: '', blockchain: ''}]);
    };

    const handleFieldChange = (index: number, field: string, value: string) => {
        const newFields = walletFields.map((f, i) => (i === index ? {...f, [field]: value} : f));
        setWalletFields(newFields);
    };
    const handleImageChange = (event: ChangeEvent<HTMLInputElement>) => {
        if (event.target.files && event.target.files[0]) {
            setData({...data, portfolio_image: event.target.files[0]});
        }
    };

    const handleSubmit = (event: React.FormEvent) => {
        event.preventDefault();
        const formData = new FormData();
        formData.append('web3_data', JSON.stringify(walletFields));
        formData.append('name', data.portfolio_name);
        if (data.portfolio_image) {
            formData.append('image', data.portfolio_image);
        }
        requestTemplate.post('api/web3/create_portfolio/', formData)
            .then(response => {
                const newPortfolio: PortfolioType = response.data;
                setPortfolios((prevPortfolios) => (prevPortfolios ? [...prevPortfolios, newPortfolio] : [newPortfolio]));
                onClose();
            })
            .catch(error => {
                error.response.status === 400 ? alert('Portfolio not created') : alert(error);
            });
    };

    return (
        <div className="wallet-create-modal">
            <div className="wallet-create-modal-content">
                <span className="wallet-create-close-button" onClick={onClose}>&times;</span>
                <form onSubmit={handleSubmit}>
                    <label className="wallet-create-label" htmlFor="image">Portfolio Avatar:</label>
                    <div className="wallet-create-file-input-container">
                        <label htmlFor="image" className="wallet-create-file-input-label">
                            <span className="wallet-create-file-icon">&#128193;</span> Choose File
                        </label>
                        <input
                            type="file"
                            id="image"
                            name="image"
                            onChange={handleImageChange}
                            className="wallet-create-file-input"
                        />
                        {data.portfolio_image &&
                            <div className="wallet-create-file-uploaded-message"><span
                                className="wallet-create-check-icon">✔️</span> File uploaded
                            </div>}
                    </div>
                    {walletFields.map((field, index) => (
                        <div key={index} className="wallet-create-form-group">
                            <label className="wallet-create-label" htmlFor={`address-${index}`}>Wallet Address:</label>
                            <input
                                className="wallet-create-input"
                                type="text"
                                id={`address-${index}`}
                                value={field.address}
                                onChange={(e) => handleFieldChange(index, 'address', e.target.value)}
                            />
                            <label className="wallet-create-label" htmlFor={`blockchain-${index}`}>Blockchain:</label>
                            <select
                                className="wallet-create-select"
                                id={`blockchain-${index}`}
                                value={field.blockchain}
                                onChange={(e) => handleFieldChange(index, 'blockchain', e.target.value)}
                            >
                                <option value="">Select Blockchain</option>
                                <option value="ethereum">Ethereum</option>
                                <option value="bitcoin">Bitcoin</option>
                                <option value="polygon">Polygon</option>
                            </select>
                        </div>
                    ))}
                    <button type="button" className="wallet-create-button" onClick={handleAddField}>+ Add another wallet</button>
                    <button type="submit" className="wallet-create-submit-button">Import</button>
                </form>
            </div>
        </div>
    );
};

export default PortfolioWalletImportComponent;