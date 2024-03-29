import React, { useEffect, useState } from 'react';
import Button from '../../Button/Button.tsx';
import SuccessBanner from '../../Banners/Success/Success.tsx';
import './AddVacation.css';
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
}

const AddVacationModal: React.FC<AddVacationModalProps> = ({open, onClose}) => {
    const [startDate, setStartDate] = React.useState<Dayjs | null>(dayjs('2023-01-17'));
    const [endDate, setEndDate] = React.useState<Dayjs | null>(dayjs('2023-01-18'));
    const [inputLocation, setLocation] = React.useState("Enter Location");
    const [showSuccessBanner, setShowSuccessBanner] = useState(false);
    const [isSubmitting, setIsSubmitting] = useState(false);

    // TODO: IMPLEMENT REFRESH AFTER ADDING THE VACATION
    const refresh = () => window.location.reload()

    var bodyAPI: any ={
        "location" : inputLocation,
        "departure_date" : startDate?.toISOString()
    }


const handleAddVacation = () => {
    setIsSubmitting(true)
    fetch(`https://zjb2711d56.execute-api.us-west-1.amazonaws.com/dev/post-vacation`, {
        method:'POST',
        body: JSON.stringify(bodyAPI)
    })
    .then((response) => {
        if(response.ok){
            console.log("POST request successful")
            setShowSuccessBanner(true)
        }else{
            throw response;
        }
    })
    .catch((err) => {
        console.error("Error making POST request ", err.message)
    })
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
                <Typography variant="h4" component="div" sx={{textDecoration:'underline'}}>
                    <header> 
                        Create a New Vacation!
                    </header>
                </Typography>
            </div>

            <Stack spacing={3}>
                <TextField 
                    id="outlined-controlled"
                    label="Vacation location"
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
                    <Button title="Add Vacation" onClick={handleAddVacation} size="small" variant='contained' disabled={isSubmitting} /> 
                    <Button title="Cancel" onClick={onClose} size="small" variant='outlined' disabled={isSubmitting} />
                </Stack>
                {showSuccessBanner && (
                    <div> 
                        <SuccessBanner message="Successfully added vacation!"/>
                        <Button title="Close" onClick={onClose} size="small" variant="contained"/>
                    </div>
                )}
                
            </Stack>
          
        </div>
        </Modal>

    )
}


export default AddVacationModal;