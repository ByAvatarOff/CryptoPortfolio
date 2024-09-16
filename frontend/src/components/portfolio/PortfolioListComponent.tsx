import { useEffect, useContext, useState, FC } from 'react';
import { requestTemplate } from '../../request/axiosRequest';
import { ListPortfolioContext } from '../../contexts/portfolio/ListPortfolioContext';
import { PortfolioType } from '../../types/portfolio/types';
import '../../styles/portfolio/ListPortfolio.css';
import PortfolioCreateComponent from './PortfolioCreateComponent';


interface PortfolioListComponentProps {
  onSelectPortfolio: (id: number) => void;
}


const PortfolioListComponent: FC<PortfolioListComponentProps> = ({ onSelectPortfolio }) => {
  const { portfolios, setPortfolios } = useContext(ListPortfolioContext);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedPortfolioId, setSelectedPortfolioId] = useState<number | null>(null);

  useEffect(() => {
    requestTemplate.get<PortfolioType[]>('api/portfolio/')
      .then((response) => {
        if (response.data) {
          setPortfolios(response.data);
          setSelectedPortfolioId(response.data[0].id);
          onSelectPortfolio(response.data[0].id);
        }
      })
      .catch((error) => {
        console.error("Error occured with get list portfolio", error);
      });
  }, [setPortfolios]);

  const getRandomImage = () => {
    const randomId = Math.floor(Math.random() * 1000);
    return `https://loremflickr.com/40/40?random=${randomId}`;
  };

  const handleDelete = (id: number) => {
    requestTemplate.delete(`api/portfolio/${id}/`)
      .then(() => {
        setPortfolios((prevPortfolios = []) => (prevPortfolios ?? []).filter(portfolio => portfolio.id !== id));
      })
      .catch((error) => {
        console.error("Ошибка при удалении портфеля:", error);
      });
  };

  const handleSelect = (id: number) => {
    setSelectedPortfolioId(id);
    onSelectPortfolio(id);
  };

  return (
    <div className="sidebar">
      {portfolios?.map((portfolio) => (
        <div
          key={portfolio.id}
          className={`menuItem ${selectedPortfolioId === portfolio.id ? 'selected' : ''}`}
          onClick={() => handleSelect(portfolio.id)}
        >
          <img src={getRandomImage()} alt="Random" className="icon" />
          <div>
            <span className="portfolioName">{portfolio.name}</span>
            <span className="portfolioValue">${(Math.random() * 10000).toFixed(2)}</span>
          </div>
          <span
            className="deleteIcon"
            onClick={(e) => {
              e.stopPropagation();
              handleDelete(portfolio.id);
            }}
            role="button"
            aria-label="delete portfolio"
          >
            🗑️
          </span>
        </div>
      ))}
      <div className="menuItem" onClick={() => setIsModalOpen(true)}>
        <span className="createPortfolio">+ Create portfolio</span>
      </div>
      <PortfolioCreateComponent isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} />
    </div>
  );
};

export default PortfolioListComponent;