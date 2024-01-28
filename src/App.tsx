import React from 'react';
import Header from './pages/Header/header.tsx';
import './App.css';
import VacationTable from './pages/VacationTable/vacationTable.tsx';
import Grid from '@mui/material/Grid';
import Calendar from './components/Calendar/Calendar.tsx';


function App() {
  return (
    <div className="App">
      <Header></Header>
      <div id="table-calendar-container">
        <div className = "split-container-left"> 
        <div id="scroll-container">
            <VacationTable></VacationTable>
        </div>
        </div>

        <div className = "split-container-right"> 
            <Calendar></Calendar>
            <div id="signature-title">
              Yours Truly, <br></br> Sophia Canja
            </div>
        </div>
      </div>
    </div>
  );
}

export default App;
