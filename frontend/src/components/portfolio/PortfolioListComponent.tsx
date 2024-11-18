import { useEffect, useContext, useState, FC } from 'react';
import { requestTemplate, BASE_URL } from '../../request/axiosRequest';
import { ListPortfolioContext } from '../../contexts/portfolio/ListPortfolioContext';
import { PortfolioType } from '../../types/portfolio/types';
import '../../styles/portfolio/ListPortfolio.css';
import PortfolioCreateComponent from './PortfolioCreateComponent';
import PortfolioWalletImportComponent from './PortfolioWalletImportComponent';


interface PortfolioListComponentProps {
  onSelectPortfolio: (id: number) => void;
}


const PortfolioListComponent: FC<PortfolioListComponentProps> = ({ onSelectPortfolio }) => {
  const { portfolios, setPortfolios } = useContext(ListPortfolioContext);
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
  const [isImportModalOpen, setIsImportModalOpen] = useState(false);
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
          <img src={`${BASE_URL}uploads/${portfolio.image}`} alt={portfolio.name} className="icon" />
          <div>
            <span className="portfolioName">{portfolio.name}</span>
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
        <div className="menuItem" onClick={() => setIsCreateModalOpen(true)}>
            <span className="createPortfolio">+ Create portfolio</span>
        </div>
        <div className="menuItem" onClick={() => setIsImportModalOpen(true)}>
            <span className="createPortfolio">+ Import wallet</span>
        </div>
        <PortfolioCreateComponent isOpen={isCreateModalOpen} onClose={() => setIsCreateModalOpen(false)} />
        <PortfolioWalletImportComponent isOpen={isImportModalOpen} onClose={() => setIsImportModalOpen(false)} />
    </div>
  );
};

export default PortfolioListComponent;