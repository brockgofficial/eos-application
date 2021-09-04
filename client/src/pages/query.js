import {useState, useEffect} from 'react'

import { DataGrid } from "@material-ui/data-grid";
import '../styles/query.css';


const Query = (props) => {
    const [messages, setMessages] = useState({description: "default desc", content: []})
  
    useEffect(() => {
      const getMessages = async () => {
        const messagesFromServer = await fetchMessages()
        setMessages(messagesFromServer)
      }
  
      getMessages()
    }, [])
  
    // Fetch device data from DB
    const fetchMessages = async () => {
      const resp = await fetch('/getmetrics')
      const data = await resp.json()
      if(resp.ok) {
        //console.log(data.content[4].message)
        return data;
      } else {
        throw Error(`Request rejected with status ${resp.status}`);
      }
    }

    // Columns for device grid
    const columns = [
        { 
            field: "machine_name",
            headerName: "Machine Name",
            width: 200,
            headerAlign: 'center',
            align: 'center',
        },
        { 
            field: "time",
            headerName: "Time", 
            width: 220,
            headerAlign: 'center', 
            align: 'center',
        },
        { 
            field: "app_name",
            headerName: "Application", 
            width: 200,
            headerAlign: 'center', 
            align: 'center',
        },
        { 
            field: "app_cpu",
            headerName: "CPU (%)", 
            width: 140,
            headerAlign: 'center', 
            align: 'center',
        },
        { 
            field: "app_ram",
            headerName: "RAM (%)", 
            width: 140,
            headerAlign: 'center', 
            align: 'center',
        }
    ]
    return (
      <div className="query">
        <div className="queryTitle">
          <h1>Query Page</h1>
        </div>
        <div className="queryForm">
          
        </div>
        <div className="machineList">
          <DataGrid
              className="deviceList"
              rows={messages.content}
              disableColumnMenu
              disableSelectionOnClick
              pageSize={10}
              rowsPerPageOptions={[10, 25, 50]}
              columns={columns}
          />
        </div>
      </div>
    )
}

export { Query }