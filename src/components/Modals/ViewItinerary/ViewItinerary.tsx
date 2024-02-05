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
    Activities : string; 
    Message : string;
    Restaurants: string;
    VacationId : number;
}

const ViewItineraryModal: React.FC<ItineraryModalProps> = ({open, onClose, vacationId }) => {
    const [data, setData] = useState<ItineraryDataInterface | null>(null);
    const [messageArr, setMessageArr] = useState([])

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
            console.log("response data", responseData)
            setData(responseData)
            
        }
    })

    .catch((err) => {
        console.error(err.message)
    })
}, [vacationId])

useEffect(() => {
    console.log("USE EFFECT Updated Itinerary Data:", data);
    if (data){
        const message = formatMessage(data[0].Message)
        
        setMessageArr(data[0].Message)
    }
    }, [data]);

const formatMessage = (message: string): string => {
    let formattedMessage = "" 
    for(let i = 0; i < message.length ; i++){
        if (message[i] == "'" || message[i] == "}" || message[i] == "{"){
            formattedMessage = message.replace(message[i], "")
        }
    }
    console.log("formatted message function ", formattedMessage)
    return formattedMessage
}

    return (
        <Modal
            open={open}
            onClose={onClose}
            aria-labelledby="itinerary-modal"
            aria-describedby="itinerary-modal-description"
        >
            <div id="itinerary-modal-container">
                <Typography id="checklist-modal" variant="h3" component="h2" sx={{mt:2}}>
                    Trip Itinerary:
                </Typography>

                <Typography id="checklist-modal" variant="h4" component="h2" sx={{mt:2}}>
                    Group Comments:
                </Typography>

                {/* {messageArr && (
          <Typography variant="h6" component="h2" sx={{ mt: 2 }}>
            {messageArr.map((item) => <div> {item} </div>)}
          </Typography>
        )} */}

                <Button title="Close" onClick={onClose} size="small" variant='contained'/>
            </div>
        </Modal>
        
    )
}
export default ViewItineraryModal;