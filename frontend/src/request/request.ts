import { requestTemplate } from "./axiosRequest";


export const SetListInvestmentsHook = (context: any) => {
    requestTemplate.get('api/investment/all_investments/').then((response) => {
        context.setInvestments(response.data);
    });
}


export const SetPortfolioPrice = (context: any, period = '1m') => {
    requestTemplate.get('api/investment/porfolio_operation_sum/')
      .then(response => {
        requestTemplate.get(`api/investment/all_time_profit/${period}/`)
        .then(responseProfit => {
          context.setPrices({
            portfolioPrice: response.data.reduce((sum: number, current: any) => sum + current.price, 0),
            total_profit: responseProfit.data.profit
          })
        })
      })
}
