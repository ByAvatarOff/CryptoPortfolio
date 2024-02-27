export type OperationsType = [{
    id: number
    ticker: string
    amount: number
    price: number
    add_date: string
    type: string
    user_id: number
}]

export type OperationType = {
    ticker: string
    amount: number
    price: number
    type: string
    user_id: number
}


export type DeleteOperationPropsType = {
    operation_id: number
}


export type Investment = {
    ticker: string
    amount_difference: number
    price_difference: number
    avg_price: number
}

export type ListInvestments = [Investment]


export type PortfolioPrices = {
    portfolioPrice: number
    total_profit: number
}

export type WSPrices = [{
    ticker: string,
    price: number
}]
