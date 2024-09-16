import {
  useContext,
  useEffect,
  FC,
  useState,
} from 'react';
import { requestTemplate } from '../../request/axiosRequest';
import DeleteOperationComponent from './DeleteOperationComponent';
import CreateOperationComponent from './CreateOperationComponent';
import { ListOperationContext } from '../../contexts/operation/ListOperationContext';
import { PortfolioIdProps } from '../../types/portfolio/types';
import '../../styles/operation/ListOperations.css';
import { OperationType } from '../../types/operation/types';



const ListOperationsComponent: FC<PortfolioIdProps> = ({ portfolioId }) => {
  const { operations, setOperations } = useContext(ListOperationContext);
  const [isModalOperationOpen, setIsModalOperationOpen] = useState(false);

  useEffect(() => {
    requestTemplate.get(`api/portfolio/operation/${portfolioId}/`)
      .then((response) => {
        setOperations(response.data);
      })
      .catch((error) => {
        console.error("Ошибка при получении операций:", error);
      });
  }, [portfolioId, setOperations]);

  return (
    <div>
      <div className="table-wrapper">
        <div className="add-button" onClick={() => setIsModalOperationOpen(true)}>
          + Add transaction
        </div>
        <CreateOperationComponent portfolioId={portfolioId} isOpen={isModalOperationOpen} onClose={() => setIsModalOperationOpen(false)} />
        <table id="dptable" className="table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Quantity</th>
              <th>Buy Price</th>
              <th>Type operation</th>
            </tr>
          </thead>
          <tbody>
            {operations?.map((operation: OperationType, index: number) => (
              <tr key={index}>
                <td><span id={`${operation.id}_${operation.ticker}`}>{operation.ticker}</span></td>
                <td><span id={`${operation.id}_${operation.amount}`}>{operation.amount}</span></td>
                <td><span id={`${operation.id}_${operation.price}`}>{operation.price}</span></td>
                <td><span id={`${operation.id}_${operation.type}`}>{operation.type}</span></td>
                <DeleteOperationComponent operation_id={operation.id} />
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default ListOperationsComponent;