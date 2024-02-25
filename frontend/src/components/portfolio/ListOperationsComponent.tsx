import {
    useContext,
    useEffect,
    FC
} from 'react';
import { requestTemplate } from '../../request/axiosRequest';
import DeleteOperationComponent from './DeleteOperationComponent';
import { ListOperationContext } from './contexts/ListOperationContext';


const ListOperationsComponent: FC = () => {
    const { operations, setOperations } = useContext(ListOperationContext);


    useEffect(() => {
        requestTemplate.get('api/portfolio/list_all_operation/').then((response) => {
            setOperations(response.data);
        })
    }, []);

    return (
        <div style={{ overflowY: "scroll", maxHeight: "300px" }}>
            <table id="dptable" className="table" style={{ position: 'sticky', top: '0'}}>
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Quantity</th>
                        <th>Buy Price</th>
                        <th>Type operation</th>

                    </tr>
                </thead>
                <tbody>
                    {operations?.map((operation: any, index: number) => (
                        <tr>
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
    );
};

export default ListOperationsComponent;
