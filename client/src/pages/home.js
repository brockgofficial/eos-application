import React from 'react';
import 'animate.css' ;
import '../styles/home.css';


//Main homepage view/component
const Home = (props) => {

 function clickMe(){
     alert('You clicked me');
 } 


    return (
        <div>
            <h1>HOMEPAGE</h1>
            <p>[TO DO]</p>
            <p>Another paragraph</p>
            <div>
                <button onClick={clickMe}>
                    don't click
                </button>
            </div>
        </div>
)}

export { Home }