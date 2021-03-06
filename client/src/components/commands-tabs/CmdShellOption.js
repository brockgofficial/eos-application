/*
 * Name: CmdShellOption.js
 * Purpose: Renders a simple select component that makes up part of the 'Command Page' 
 * 
 * Usage: Child of Command.js 
 *        User selects shell option and gives the selection to command.js to include when sending the command details
 *        to the backend
 */

// Module imports here
import React from 'react';
import {useState } from 'react';

// Component imports here
import InputLabel from "@material-ui/core/InputLabel";
import MenuItem from "@material-ui/core/MenuItem";
import FormControl from '@material-ui/core/FormControl';
import Select from "@material-ui/core/Select";
import FormLabel from "@material-ui/core/FormLabel";


export default function CmdShellOption(props) {
    const [value, setValue] = useState('')

    const handleChange = (event) => {
        props.changeShellOption(event.target.value)
        setValue(event.target.value)
    }

    return (
    <div style={{display: "flex", flexDirection: 'column'}}>
        <div style={{flex: 2}}>
        </div>
        <FormLabel>Command Shell Option</FormLabel>
        <FormControl style={{display: "flex", flex: 2, marginTop: "20px"}}>
            <Select
                labelId="Command Shell Options"
                id="Command Shell Options"
                value={value}
                onChange={handleChange}
                variant="outlined"
                defaultValue="cmd"
            >
                <MenuItem value={'cmd'}>CMD</MenuItem>
                <MenuItem value={'powershell'}>Powershell</MenuItem>
                <MenuItem value={'wsl'}>WSL</MenuItem>
            </Select>
        </FormControl> 
    </div>
    );
}