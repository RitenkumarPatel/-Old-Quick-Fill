import React, { useState } from 'react';
import {createRoot} from 'react-dom/client'
import "./styling.css"
import styled from 'styled-components';



import './ToggleSwitch.css'
 
const types = ['Sign In', "Sign Out"];
 
var toggleOn = false;
var toggleCounter = 0;
var xhr = new XMLHttpRequest()
 
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
  font-family: Helvetica, Verdana, Arial;
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
 
const signIn=(e)=>{
  console.log("sign in")
   /*eslint-disable no-undef */
  chrome.runtime.sendMessage({message: 'login'}, function (response){
    if(response=='success') window.close();
  });
}
 
const signOut=(e)=>{
  console.log("sign out");
 /*eslint-disable no-undef */
 chrome.runtime.sendMessage({message: 'logout'}, function(response){
  if(response=='success') window.close();
 });
 
  
}
 
function toggleClick() {
  toggleCounter ++;
  if (toggleCounter % 2){
    toggleOn = !toggleOn;
  }
}
 
 
 
const test = (
    <>
   
    <img className="logo" src="icon_48.png" ></img>
    <h1></h1>
 
    <Paragraph>Use ctrl+q to auto-fill your text!</Paragraph>
   
    <ButtonGroup onClick={toggleClick}>
    <ToggleSwitch id ="cb" label="Activate Quick Fill:" />
    </ButtonGroup>
   
    <ButtonGroup >
        <Button variant="primary" value="Sign In"  onClick={signIn}>Sign In</Button>
        <Button variant="primary" value="Sign Out" onClick={signOut}>Sign Out</Button>
       
    </ButtonGroup>
    </>  
)
 
const container = document.createElement('div')
document.body.appendChild(container)
const root = createRoot(container)
root.render(test)
 

function App() {}

 export default App;

