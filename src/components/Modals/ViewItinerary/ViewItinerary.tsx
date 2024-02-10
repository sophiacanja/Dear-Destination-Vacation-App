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
    Activities : []; 
    Message : string;
    Restaurants: string;
    VacationId : number;
}

const ViewItineraryModal: React.FC<ItineraryModalProps> = ({open, onClose, vacationId }) => {
    const [data, setData] = useState<ItineraryDataInterface | null>(null);
    const [messageArr, setMessageArr] = useState<string[]>(["No messages at this time"])
    const [activitiesArr, setActivitiesArr] = useState<string[]>(["No activities listed at this time"])
    const [restaurantsArr, setRestaurantsArr] = useState<string[]>(["No restaurants listed at this time"])

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
            setMessageArr(formatData(responseData[0].Message))
            setActivitiesArr(formatData(responseData[0].Activities))
            setRestaurantsArr(formatData(responseData[0].Restaurants))
        }
    })

    .catch((err) => {
        console.error(err.message)
    })
}, [vacationId])

useEffect(() => {
    console.log("Updated Itinerary Data:", data);
    console.log("Messages Returned:", messageArr)
    }, [data]);

// helper function that takes in a dictionary casted to a string and returns an array of each key, val pair
const formatData = (message: string): string[] => {
    const formattedMessage = message.replace(/[{}'"]/g, '');
    const messageList: string[] = formattedMessage.split(',').map(item => item.trim())
    console.log("formatted list  ", messageList)
    return messageList
}

    return (
        <Modal
            open={open}
            onClose={onClose}
            aria-labelledby="itinerary-modal"
            aria-describedby="itinerary-modal-description"
        >
            <div id="itinerary-modal-container">
                <Typography id="checklist-modal" variant="h4" component="h2" sx={{mt:2, textDecoration:'underline'}}>
                    Trip Itinerary:
                </Typography>

                <Typography id="checklist-modal" variant="h5" component="h2" sx={{mt:2}} fontWeight={"bold"}>
                    Group Comments:
                </Typography>

                 {messageArr  && (
                    <Typography variant="h6" component="h2" sx={{ mt: 2 }}>
                        {messageArr.map((item) => <div> {item} </div>)}
                    </Typography>
                )} 

                <Typography id="checklist-modal" variant="h5" component="h2" sx={{mt:2}} fontWeight={"bold"}>
                    Activities:
                </Typography>

                {activitiesArr && (
                    <Typography variant="h6" component="h2" sx={{ mt: 2 }}>
                        {activitiesArr.map((item) => <div> {item} </div>)}
                    </Typography>
                )}

                <Typography id="checklist-modal" variant="h5" component="h2" sx={{mt:2}} fontWeight={"bold"}>
                    Restaurants:
                </Typography>

                {restaurantsArr && (
                    <Typography variant="h6" component="h2" sx={{ mt: 2 }}>
                        {restaurantsArr.map((item) => <div> {item} </div>)}
                    </Typography>
                )}

                <Button title="Close" onClick={onClose} size="small" variant='contained'/>
            </div>
        </Modal>
        
    )
}
export default ViewItineraryModal;