import { requestTemplate } from "./axiosRequest";


export const SetListInvestmentsHook = (context: any) => {
    requestTemplate.get('api/portfolio/all_investments/').then((response) => {
        context.setInvestments(response.data);
    });
}


export const SetPortfolioPrice = (context: any) => {
    requestTemplate.get('api/portfolio/porfolio_operation_sum/')
      .then(response => {
        const jsonArray = JSON.parse(response.data)
        requestTemplate.get('api/portfolio/all_time_profit/')
        .then(responseProfit => {
          context.setPrices({
            portfolioPrice: jsonArray.reduce((sum: number, current: any) => sum + current.price, 0),
            total_profit: responseProfit.data
          })
        })
      })
}