import React from 'react';
import Button from './components/Button'
import MyCard from './components/MyCard';
// Example: src/index.tsx or src/App.tsx
// import '@emotion/react';

import logo from './logo.svg';
import './App.css';

const handleButtonClick = () => {
  console.log("button clicked");
}

function App() {
  return (
    <div className="App">
      <header> Hello world</header>
      <Button title="Poop" onClick={handleButtonClick}/>
      <div>
      <MyCard title="Juneper" content="Biggest Poop" />
      </div>
    </div>
  );
}

export default App;
