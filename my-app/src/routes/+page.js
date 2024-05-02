export const load = async ({ fetch }) => {
    const responseFlights = await fetch('http://vda-lab.gitlab.io/datavis-technologies/assets/flights_part.json')
    const dataFlights = await responseFlights.json()
  
    return {
      flights: dataFlights
    }
  }