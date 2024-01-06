import React, { useEffect, useState } from 'react';
import Button from './Button.tsx';
import './ChecklistModal.css'
import {Modal, Typography, Box} from "@mui/material";
import { json } from 'stream/consumers';

// https://vf24p8yepd.execute-api.us-west-1.amazonaws.com/dev/get-checklist 
type ChecklistModalProps = {
    onClose: () => void;
    open: boolean;
    vacationId: string;
    vacationLocation: string; 
}

interface ChecklistInfo {
    ChecklistId: string,
    Item: string,
    VacationId: string
}

const ChecklistModal: React.FC<ChecklistModalProps> = ({open, onClose, vacationLocation, vacationId}) => {
    const [checklistItems, setChecklistItems] = useState<ChecklistInfo>({
        ChecklistId: "",
        Item: "",
        VacationId: ""
    });

    var headersAPI: any = {
        "vacation_id" : vacationId
    }

    // console.log("Vacation id " + vacationId)
    // console.log(headersAPI)
    useEffect(() => {
        fetch(`https://vf24p8yepd.execute-api.us-west-1.amazonaws.com/dev/get-checklist`, {
            method: 'GET',
            headers: headersAPI
        })
        .then((response) => response.json()) 
        .then((data) => {
            if(data[0] !== undefined){
                setChecklistItems({Item : data[0].item, ChecklistId : data[0].ChecklistId, VacationId:data[0].VacationId})
                console.log(checklistItems)
                console.log(data)
            }
            
            else {
                console.log("DATA RESPONSE IS UNDEF")
                console.log(data)
            }
            
        })
        .catch((err) => {
            console.error(err.message)
        })

    }, [vacationId])

    return(
        <Modal
            open={open}
            onClose={onClose}
            aria-labelledby="checklist-modal"
            aria-describedby="checklist-modal-description"
        >
            <div id="checklist-modal-container">
                <Typography id="checklist-modal" variant="h4" component="h2" sx={{mt:2}}>
                Trip Checklist: {vacationLocation} 
                </Typography>
           
                <Button title="Close" onClick={onClose} size="small" variant='contained'/>
            </div>
        </Modal>
    )
}

export default ChecklistModal;