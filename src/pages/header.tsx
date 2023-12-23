import React from 'react';
import Button from '../components/Button.tsx'

const handleButtonClick = () => {
    console.log("button clicked");
  }

const Header: React.FC = () => {
    return(
        <div>
            <header id="site-title"> Vacation App </header>
            <p>
                This application helps you and your friends organize upcoming trips! <br></br>It is a one-stop shop to find out vacation details, itineraries, and attendees in order to avoid confusion and miscommunication when planning big trips!
            </p>
            <Button title="Plan New Vacation" variant = "contained" onClick={handleButtonClick}/>
      </div>
    )
} 

export default Header;