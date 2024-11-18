export type PortfolioType = {
    id: number
    name: string
    user_id: number
    image: string
  }


export type InvestmentType = {
    ticker: string
    amount_difference: number
    price_difference: number
    avg_price: number
}


export type PortfolioPrices = {
    portfolioPrice: number
    total_profit: number
}

export type PriceData = {
    ticker: string
    price: number
  }

export type TimeFrameChangesList = {
    ticker: string
    percent: string
  }


export type TimeFrameChanges = {
    "timeframe_1d": Array<TimeFrameChangesList>
    "timeframe_7d": Array<TimeFrameChangesList>
  }


export type PortfolioIdProps = {
    portfolioId: number | null;
  }
