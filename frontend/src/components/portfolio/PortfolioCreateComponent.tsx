import React, {FC, useState, useContext, FormEvent, ChangeEvent} from 'react';
import '../../styles/portfolio/PortfolioCreate.css';
import {requestTemplate} from "../../request/axiosRequest";
import {ListPortfolioContext} from '../../contexts/portfolio/ListPortfolioContext';
import {PortfolioType} from '../../types/portfolio/types';
import {ModalWindowProps} from '../../types/types';


const PortfolioCreateComponent: FC<ModalWindowProps> = ({isOpen, onClose}) => {
    const {portfolios, setPortfolios} = useContext(ListPortfolioContext);
    const [data, setData] = useState({
        portfolio_name: "",
        image: null as File | null,
    });

    if (!isOpen) return null;

    const handleNameChange = (event: FormEvent<HTMLInputElement>) => {
        setData({...data, portfolio_name: (event.target as HTMLInputElement).value});
    };

    const handleImageChange = (event: ChangeEvent<HTMLInputElement>) => {
        if (event.target.files && event.target.files[0]) {
            setData({...data, image: event.target.files[0]});
        }
    };

    const handleSubmit = async (event: React.FormEvent) => {
        event.preventDefault();
        const formData = new FormData();
        formData.append('name', data.portfolio_name);
        if (data.image) {
            formData.append('image', data.image);
        }
        requestTemplate.post('api/portfolio/', formData)
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
        <div className="portfolio-create-modal">
            <div className="portfolio-create-button-modal-content">
                <span className="portfolio-create-close-button" onClick={onClose}>&times;</span>
                <form onSubmit={handleSubmit}>
                    <div className="portfolio-create-form-group">
                        <label className="portfolio-create-label" htmlFor="image">Portfolio Avatar:</label>
                        <div className="portfolio-create-file-input-container">
                            <label htmlFor="image" className="portfolio-create-file-input-label">
                                <span className="portfolio-create-file-icon">&#128193;</span> Choose File
                            </label>
                            <input
                                type="file"
                                id="image"
                                name="image"
                                onChange={handleImageChange}
                                className="portfolio-create-file-input"
                            />
                            {data.image &&
                                <div className="portfolio-create-file-uploaded-message"><span
                                    className="portfolio-create-check-icon">✔️</span> File uploaded
                                </div>}
                        </div>
                        <label className="portfolio-create-label" htmlFor="portfolio_name">Portfolio Name:</label>
                        <input
                            className="portfolio-create-text-input"
                            type="text"
                            id="portfolio_name"
                            name="portfolio_name"
                            value={data.portfolio_name}
                            onChange={handleNameChange}
                        />
                    </div>
                    <button type="submit" className="portfolio-create-button">Create</button>
                </form>
            </div>
        </div>
    );
};


export default PortfolioCreateComponent;