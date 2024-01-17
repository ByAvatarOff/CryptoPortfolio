import { requestTemplate } from '../../request/axiosRequest';
import { useContext } from 'react';
import { ListOperationContext } from './contexts/ListOperationContext';
import { DeleteOperationPropsType } from './types';
import { ListInvestmentsContext } from "./contexts/ListInvestmentsContext";
import { SetListInvestmentsHook, SetPortfolioPrice } from '../../request/request';
import { PortfolioPriceContext } from "./contexts/OnlinePortfolioPriceContext";


const DeleteOperationComponent = (props: DeleteOperationPropsType) => {
    const { investments, setInvestments } = useContext(ListInvestmentsContext);
    const { operations, setOperations } = useContext(ListOperationContext);
    const { portfolioPrice, setPortfolioPrice } = useContext(PortfolioPriceContext);

    const DeleteRecordHandler = () => {
        let endpoint = `api/portfolio/delete_operation/${props.operation_id}/`;
        requestTemplate.delete(endpoint).then((response) => {
            setOperations(response.data)
            SetListInvestmentsHook({ investments, setInvestments })
            SetPortfolioPrice({ portfolioPrice, setPortfolioPrice })
        });;

    }
    return (
        <button type="button" onClick={DeleteRecordHandler} className="btn btn-danger delete-row">Delete Row</button>
    );
};

export default DeleteOperationComponent;