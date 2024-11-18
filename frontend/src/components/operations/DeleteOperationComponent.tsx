import { requestTemplate } from '../../request/axiosRequest';
import { useContext, FC } from 'react';
import { ListOperationContext } from '../../contexts/operation/ListOperationContext';
import { OperationPropsType } from '../../types/operation/types';
import { OperationType } from '../../types/operation/types';


const DeleteOperationComponent: FC<OperationPropsType> = ({ operation_id }) => {
  const { operations, setOperations } = useContext(ListOperationContext);

  const deleteRecordHandler = (operation_id: number) => {
    let endpoint = `api/portfolio/operation/${operation_id}/`;
    requestTemplate.delete(endpoint).then(() => {
      setOperations((prevOperations = []) => (prevOperations ?? []).filter(operation => operation.id !== operation_id));
    })
    .catch((error) => {
      console.error("Ошибка при удалении транзакции:", error);
    });
  }

  return (
    <span
      className="deleteIcon"
      onClick={(e) => {
        e.stopPropagation();
        deleteRecordHandler(operation_id);
      }}
      role="button"
      aria-label="delete portfolio"
    >
      🗑️
    </span>
  );
};

export default DeleteOperationComponent;
