import React, { useEffect, useState } from 'react';
import Button from '../../Button/Button.tsx';
import './ViewItinerary.css'
import {Modal, Typography, Box} from "@mui/material";


type ItineraryModalProps = {
    onClose: () => void;
    open: boolean;
    vacationId: string
}

const ViewItineraryModal: React.FC<ItineraryModalProps> = ({open, onClose, vacationId }) => {

var headersAPI: any = {
    "Content-Type" : "application/json",
    "vacation_id" : vacationId
}

useEffect(() => {
    fetch(`https://ddewbg59ti.execute-api.us-west-1.amazonaws.com/dev`, {
        method: 'GET',
        headers: headersAPI
    })
    .then((response) => response.json())
    .then((data) => {
        console.log(data)
    })

    .catch((err) => {
        console.error(err.message)
    })
}, [vacationId])

    return (
        <Modal
            open={open}
            onClose={onClose}
            aria-labelledby="itinerary-modal"
            aria-describedby="itinerary-modal-description"
        >
            <div id="itinerary-modal-container">
                <Typography id="checklist-modal" variant="h4" component="h2" sx={{mt:2}}>
                    Trip Itinerary
                </Typography>
            </div>
        </Modal>
        
    )
}
export default ViewItineraryModal;