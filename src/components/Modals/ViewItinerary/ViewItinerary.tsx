import React, { useEffect, useState } from 'react';
import Button from '../../Button/Button.tsx';
import './ViewItinerary.css'
import {Modal, Typography, Box} from "@mui/material";


type ItineraryModalProps = {
    onClose: () => void;
    open: boolean;
    vacationId: string
}

interface ItineraryDataInterface{
    activities : string; 
    messages : string;
    restaurants: string;
    vacationId : number;
}

const ViewItineraryModal: React.FC<ItineraryModalProps> = ({open, onClose, vacationId }) => {
    const [data, setData] = useState<ItineraryDataInterface[]>([])

var headersAPI: any = {
    "vacation_id" : vacationId
}
console.log("vacation id headers ", vacationId)
useEffect(() => {
    fetch(`https://ddewbg59ti.execute-api.us-west-1.amazonaws.com/dev/get-itinerary`, {
        method: 'GET',
        headers: headersAPI
    })
    .then((response) => response.json())
    .then((responseData) => {
        if(responseData && responseData.length > 0 ) {
            console.log(responseData)
            setData(responseData[0])
        }
    })

    .catch((err) => {
        console.error(err.message)
    })
}, [vacationId])

useEffect(() => {
    console.log("USE EFFECT Updated Itinerary Data:", data);
    }, [data]);

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