import React from 'react';
import dayjs from 'dayjs';
import { DateCalendar } from '@mui/x-date-pickers/DateCalendar';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import Button from '../components/Button.tsx'
import './Calendar.css'

const handleButtonClick = () => {
    console.log("button clicked");
  }

const Calendar: React.FC = () => {
    return(
        <div id='calendar-container'>
            <LocalizationProvider dateAdapter={AdapterDayjs}>
                <DateCalendar defaultValue={dayjs('2024-01-10')} readOnly/>
            </LocalizationProvider>
            <Button title="Plan New Vacation" variant = "contained" onClick={handleButtonClick}/>
        </div>
    ) 
}

export default Calendar;