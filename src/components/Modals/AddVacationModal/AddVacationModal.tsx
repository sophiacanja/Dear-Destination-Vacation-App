import React, { useEffect, useState } from 'react';
import Button from '../../Button/Button.tsx';
import './AddVacationModal.css'
import {Modal, Typography, Box} from "@mui/material";
import TextField from '@mui/material/TextField';
import {Stack} from "@mui/material";

import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import dayjs, { Dayjs } from 'dayjs';


type AddVacationModalProps = {
    onClose: () => void; 
    open: boolean;
    location: string;
    departureDate: Date; 
}

const AddVacationModal: React.FC<AddVacationModalProps> = ({open, onClose}) => {
    const [startDate, setStartDate] = React.useState<Dayjs | null>(dayjs('2023-01-17'));
    const [endDate, setEndDate] = React.useState<Dayjs | null>(dayjs('2023-01-18'));
    const [inputLocation, setLocation] = React.useState("Enter Location");

    var headersAPI: any ={
        "location" : inputLocation,
        "departure_date" : startDate
    }
    return(
        <Modal
            open={open}
            onClose={onClose}
            aria-labelledby="add-vacation-modal"
            aria-describedby="add-vacation-modal-description"
        >
        <div id="add-vacation-modal-container">
            <div id="modal-header">
                <Typography variant="h5" component="div">
                    <header> 
                        Create a New Vacation!
                    </header>
                </Typography>
            </div>

            <Stack spacing={3}>
                <TextField 
                  id="outlined-controlled"
                  label="Enter your vacation's location"
                  value={inputLocation}
                  onChange={(event: React.ChangeEvent<HTMLInputElement>) => {
                    setLocation(event.target.value);
                  }}
                />

                <LocalizationProvider dateAdapter={AdapterDayjs}>  
                    <DatePicker
                        label="Start of Vacation"
                        value={startDate}
                        onChange={(newValue) => setStartDate(newValue)}
                    />

                    <DatePicker
                        label="End of Vacation"
                        value={endDate}
                        onChange={(newValue) => setEndDate(newValue)}
                    />  
                </LocalizationProvider>
            
                <Stack justifyContent="center" spacing={3} direction="row">
                    <Button title="Add Vacation" onClick={onClose} size="small" variant='contained' /> 
                    <Button title="Cancel" onClick={onClose} size="small" variant='outlined' />
                </Stack>
            </Stack>
          
        </div>
        </Modal>

    )
}


export default AddVacationModal;