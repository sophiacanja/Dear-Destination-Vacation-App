import React from 'react';
import Header from './pages/header';
import './App.css';
import VacationTable from './pages/vacationTable';
import Grid from '@mui/material/Grid';
import Calendar from './components/Calendar.tsx';


function App() {
  return (
    <div className="App">
      <Header></Header>
      <div id="table-calendar-container">
        <div className = "split-container-left"> 
            <VacationTable></VacationTable>
        </div>

        <div className = "split-container-right"> 
            <Calendar></Calendar>
        </div>
      </div>
    </div>
  );
}

export default App;
