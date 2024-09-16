import { requestTemplate } from '../../request/axiosRequest';
import { useContext, FC } from 'react';
import { ListOperationContext } from '../../contexts/operation/ListOperationContext';
import { OperationPropsType } from '../../types/operation/types';
import { ListInvestmentsContext } from "../../contexts/operation/ListInvestmentsContext";
import { SetListInvestmentsHook, SetPortfolioPrice } from '../../request/request';
import { PortfolioPriceContext } from "../../contexts/operation/OnlinePortfolioPriceContext";


const DeleteOperationComponent: FC<OperationPropsType> = ({ operation_id }) => {
    const { investments, setInvestments } = useContext(ListInvestmentsContext);
    const { operations, setOperations } = useContext(ListOperationContext);
    const { prices, setPrices } = useContext(PortfolioPriceContext);

    const DeleteRecordHandler = (operation_id: number) => {
        let endpoint = `api/portfolio/delete_operation/${operation_id}/`;
        requestTemplate.delete(endpoint).then((response) => {
            setOperations(response.data)
            SetListInvestmentsHook({ investments, setInvestments })
            SetPortfolioPrice({ prices, setPrices })
        });
    }

    return (
        <span
        className="deleteIcon"
        onClick={(e) => {
          e.stopPropagation();
          DeleteRecordHandler(operation_id);
        }}
        role="button"
        aria-label="delete portfolio"
      >
        🗑️
      </span>
    );
};

export default DeleteOperationComponent;
