import React from 'react';
import Header from './pages/header';
import logo from './logo.svg';
import './App.css';
import VacationTable from './pages/vacationTable';


function App() {
  return (
    <div className="App">
      <Header></Header>
      <VacationTable></VacationTable>
    </div>
  );
}

export default App;
