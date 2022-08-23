import React, { useState } from 'react';
import {createRoot} from 'react-dom/client'
import '../assets/tailwind.css'
import styled from 'styled-components';
import { motion } from "framer-motion";
import 'bootstrap/dist/css/bootstrap.min.css';
import '../assets/ToggleSwitch.css'

const types = ['Sign In', "Sign Out"];

var toggleOn = false;
var toggleCounter = 0;

const Button = styled.button`
background-color: white;
color: #000000;


outline: 0;
font-size: 20px;
padding: 5px 20px;
margin: 10px 5px;

border-radius: 100px;
border: 2px;
border-weight: 2px;
border-style: solid;
border-color: black;


cursor: pointer;
box-shadow: 0px 2px 2px lightgray;

&:hover {
    background-color: #000000;
    color: #FFFFFF
}
&:disabled {
    color: grey;
    opacity: 0.7;
    cursor:default;
}
`;

const ButtonToggle = styled(Button)`
  opacity: 1;
  ${({ active }) =>
    active &&
    `
    opacity: 0.6;
  `}
`;

const ButtonGroup = styled.div`
  display: flex;
  margin-left: 20px;
`;

const Paragraph = styled.div`
  font-size: 15px;
  text-align: center;
  font-family: Georgia, Verdana, Geneva, Tahoma, sans-serif;
`



const ToggleSwitch = ( {id, label},  ) => {
    return(
        <div className="container">
        {label}{" "}
        <div className="toggle-switch">
            <input type="checkbox" className="checkbox" 
                name={label} id={label} />
            <label className="label" htmlFor={label}>
            <span className="inner" />
            <span className="switch" />
            </label>
        </div>
    </div>
    );
};

const handleClick=(e)=>{
  console.log(e);
}


function toggleClick() {
  toggleCounter ++;
  if (toggleCounter % 2){
    toggleOn = !toggleOn;
  }
}



const test = (
    <>
    <h1 className="header">Quick Fill</h1>
    <Paragraph>Use ctrl+q to auto-fill your text!</Paragraph>
    
    <ButtonGroup onClick={toggleClick}>
    <ToggleSwitch id ="cb" label="Activate Quick Fill:" />
    </ButtonGroup>
    
    <ButtonGroup onClick={handleClick}>
        <Button variant="primary" value="Sign In"  >Sign In</Button>
        <Button variant="primary" value="Sign Out" >Sign Out</Button>
        
    </ButtonGroup>
    </>   
)

const container = document.createElement('div')
document.body.appendChild(container)
const root = createRoot(container)
root.render(test)

