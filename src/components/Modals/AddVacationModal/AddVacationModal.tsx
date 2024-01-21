import React, { useEffect, useState } from 'react';
import Button from '../../Button/Button.tsx';
import './AddVacationModal.css'
import {Modal, Typography, Box} from "@mui/material";

type AddVacationModalProps = {
    onClose: () => void; 
    open: boolean;
    location: string;
    departureDate: Date; 
}

const AddVacationModal: React.FC<AddVacationModalProps> = ({open, onClose, location, departureDate}) => {
    var headersAPI: any ={
        "location" : location,
        "departure_date" : departureDate
    }
    return(
        <Modal
            open={open}
            onClose={onClose}
            aria-labelledby="add-vacation-modal"
            aria-describedby="add-vacation-modal-description"
        >
            <div> hello world {location}
            <Button title="Check In" onClick={onClose} size="small" variant='contained'/>
            <Button title="Cancel" onClick={onClose} size="small" variant='outlined'/>

            </div>
        </Modal>

    )
}


export default AddVacationModal;