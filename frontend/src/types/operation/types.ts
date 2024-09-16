export type CreateOperationType = {
    ticker: string
    amount: number
    price: number
    type: string
    portfolio_id: number
}


export type OperationType = {
    id: number
    ticker: string
    amount: number
    price: number
    add_date: string
    type: string
    portfolio_id: number
}

export type OperationPropsType = {
    operation_id: number
}