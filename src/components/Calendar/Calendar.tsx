import React, {useState} from 'react';
import dayjs from 'dayjs';
import { DateCalendar } from '@mui/x-date-pickers/DateCalendar';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import Button from '../Button/Button.tsx'
import './Calendar.css'
import AddVacationModal from '../Modals/AddVacationModal/AddVacationModal.tsx';


const Calendar: React.FC = () => {
    const [isAddVacationModalOpen, setIsAddVacationModalOpen] = useState(false)
    const closeAddvacationModal = () => {
        console.log("Closing modal")
        setIsAddVacationModalOpen(false)
    }

    const openAddVacationModal = () => {
        console.log("Opening modal");
        setIsAddVacationModalOpen(true)
      }

    return(
        <div id='calendar-container'>
            <LocalizationProvider dateAdapter={AdapterDayjs}>
                <DateCalendar defaultValue={dayjs('2024-01-10')} readOnly/>
            </LocalizationProvider>
            <Button 
                title="Plan New Vacation" 
                variant = "contained" 
                onClick={() => openAddVacationModal()}
            />
            {isAddVacationModalOpen && 
                <AddVacationModal
                    open={isAddVacationModalOpen}
                    onClose={closeAddvacationModal}
                    location='Test'
                    departureDate={ new Date()}
                />
            }
        </div>
    ) 
}

export default Calendar;