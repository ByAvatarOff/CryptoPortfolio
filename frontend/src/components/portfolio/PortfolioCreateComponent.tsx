import React, { FC, useState, useContext } from 'react';
import '../../styles/portfolio/PortfolioCreateComponent.css';
import { requestTemplate } from "../../request/axiosRequest";
import { ListPortfolioContext } from '../../contexts/portfolio/ListPortfolioContext';
import { PortfolioType } from '../../types/portfolio/types';


interface PortfolioCreateComponentProps {
  isOpen: boolean;
  onClose: () => void;
}

const PortfolioCreateComponent: FC<PortfolioCreateComponentProps> = ({ isOpen, onClose }) => {
  const { portfolios, setPortfolios } = useContext(ListPortfolioContext);
  const [name, setName] = useState('');

  if (!isOpen) return null;

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    requestTemplate.post('api/portfolio/', { "name": name })
      .then(response => {
        const newPortfolio: PortfolioType = response.data;
        setPortfolios((prevPortfolios) => (prevPortfolios ? [...prevPortfolios, newPortfolio] : [newPortfolio]));
        onClose();
      })
      .catch(error => {
        error.response.status === 400 ? alert('Portfolio not create') : alert(error)
      });
  };

  return (
    <div className="modal">
      <div className="modalContent">
        <span className="closeButton" onClick={onClose}>&times;</span>
        <form onSubmit={handleSubmit}>
          <div className="formGroup">
            <label htmlFor="name">Portfolio Name:</label>
            <input
              type="text"
              id="name"
              name="name"
              value={name}
              onChange={(e) => setName(e.target.value)}
            />
          </div>
          <button type="submit" className="submitButton">Create</button>
        </form>
      </div>
    </div>

  );
};

export default PortfolioCreateComponent;