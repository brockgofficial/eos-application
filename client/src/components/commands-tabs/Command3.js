/*
 * Name: command3.js
 * Purpose: Renders Simple component that makes up the 'Command Page' custom command tab (Tab 3)
 * 
 * Usage: Child of Command.js 
 *        Receives Custom command input and sends through to command.js through props
 */



import React from 'react';
import { useState} from 'react';
import { TextField } from '@material-ui/core';
import styled from 'styled-components';

const CmdThreeContainer = styled.div`
  display: flex;
  flex-direction: column;
  justify-items: center;
`;

const CustomInputWrapper = styled.div`
  width: 100%;
  padding-top: 20px;
`;

const CustomCmdTitle = styled.div`
  padding-top: 15px;  
  width: 100%;
  font-size: 20px;
`;

export default function Command3(props){
  const [value, setValue] = useState();
  const [customCmd, setCustomCmd] = useState('');

  const handleChange = (event) => {
    event.preventDefault();
    props.changeCmd(event.target.value)
    setCustomCmd(event.target.value)
  }
  
  return (
  <CmdThreeContainer>
    <CustomCmdTitle>
      Enter Custom Command to run.
    </CustomCmdTitle>
    <CustomInputWrapper>
      <TextField
        id="customCmd"
        name="customCmd"
        multiline
        style={{paddingTop: "10px"}}
        minRows={4}
        placeholder="eg. ls "
        variant="outlined"
        required
        margin="normal"
        fullWidth
        value={value}
        onChange={handleChange}
      >
      </TextField>
    </CustomInputWrapper>
  </CmdThreeContainer>
  )
}


