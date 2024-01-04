import React from 'react';
import Header from './pages/header';
import logo from './logo.svg';
import './App.css';
import VacationTable from './pages/vacationTable';
import Grid from '@mui/material/Grid';
import Calendar from './components/Calendar.tsx';


function App() {
  return (
    <div className="App">
      <Header></Header>
      <div className="table-calendar-container">
        <Grid container spacing={0} columnSpacing={{ xs: 0}}> 
          <Grid item xs={6} >
            <VacationTable></VacationTable>
          </Grid>
          <Grid item xs={6} style={{ margin: '0', marginTop: '10px' }}>
            <Calendar></Calendar>
          </Grid>
        </Grid>
      </div>
    </div>
  );
}

export default App;
