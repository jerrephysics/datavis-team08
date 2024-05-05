import Papa from 'papaparse'

export const load = async ({ fetch }) => {
    const responseFlights = await fetch('http://vda-lab.gitlab.io/datavis-technologies/assets/flights_part.json')
    const dataFlights = await responseFlights.json()

    const elements = await fetch('http://localhost:5173/regions.json')
    const markers = await elements.json()

    const companyRegionsData = await fetch('https://raw.githubusercontent.com/JannesPeeters/DEAD/main/data/regions.csv')
    let csvCompanyRegions = await companyRegionsData.text()
    let parsedCsvCompanyRegions = Papa.parse(csvCompanyRegions, {header: true})

    const companyOrdersData = await fetch('https://raw.githubusercontent.com/JannesPeeters/DEAD/main/data/orders.csv')
    let csvCompanyOrders = await companyOrdersData.text()
    let parsedCsvCompanyOrders = Papa.parse(csvCompanyOrders, {header: true})
    console.log(parsedCsvCompanyRegions);
    console.log(parsedCsvCompanyOrders);
  
    return {
      flights: dataFlights,
      regions: markers,
      deadregions: parsedCsvCompanyRegions.data,
      deadorders: parsedCsvCompanyOrders.data
    }
  }

  export const ssr = false