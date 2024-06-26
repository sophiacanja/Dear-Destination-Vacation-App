import React from 'react';
import './header.css'

const Header: React.FC = () => {
    return(
        <div id="header-container">
            <header id="site-title"> Dear Destination, </header>
            <div id="site-description">
                Welcome! This is an application helps you and your friends organize upcoming trips! <br></br>This is a one-stop shop to find out vacation details, itineraries, and attendees in order to avoid confusion and miscommunication when planning big trips!
            </div>  
      </div>
    )
} 

export default Header;