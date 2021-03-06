/*
 * Name: SystemMetricsTable.js
 *
 * Purpose: Renders the System Metrics Table for the Query page tabs
 * 
 * Usage: Query.js
 */

// Module imports here
import {useState, useEffect, useMemo} from 'react'

// Component imports here
import MetricsTable from '../../metrics-table/MetricsTable';

// Column data for the Table
import { AppMetricsColumnData } from './AppMetricsColumnData'

/*
 * This is the main component for the System Metrics Table tab
*/
export const AppMetricsTable = (props) => {
  
  /*
  * useMemo() hook ensures the data inst recreated on every render
  * otherwise react-table woulf think that it is receving new data on every render
  * it would attempt to calculate a lot of logic every time - affecting performance
  */
  const appMetricsColumns = useMemo(() => AppMetricsColumnData, [])
  
  // Variable to store the data from the API call
  const [appMetrics, setMetrics] = useState([])
  
  // Hook used to render the client machines returned from API call
  useEffect(() => {
    const getMetrics = async () => {
      const data = await fetchMetrics()
      setMetrics(data.application_metrics)
    }
    getMetrics()
  }, [])

  // Function to fetch client machines from DB
  const fetchMetrics = async () => {
    const resp = await fetch('/metrics/getallappmetrics')
    const data = await resp.json()
    if(resp.ok) {
      return data;
    } else {
      throw Error(`Request rejected with status ${resp.status}`);
    }
  }

  return (
    <div>
      <MetricsTable data={appMetrics} columns={appMetricsColumns} machineName={props.machineName}/>
    </div>
  )
}