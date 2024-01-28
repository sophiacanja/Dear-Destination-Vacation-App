import React, { useEffect, useState } from 'react';
import Button from '../../Button/Button.tsx';
import './ViewChecklist.css'
import {Modal, Typography, Box} from "@mui/material";
import { json } from 'stream/consumers';
import { isTemplateElement } from '@babel/types';

// https://vf24p8yepd.execute-api.us-west-1.amazonaws.com/dev/get-checklist 
type ChecklistModalProps = {
    onClose: () => void;
    open: boolean;
    vacationId: string;
    vacationLocation: string; 
}


const ChecklistModal: React.FC<ChecklistModalProps> = ({open, onClose, vacationLocation, vacationId}) => {
    const [checklistArr, setChecklistArr] = useState([])

    var headersAPI: any = {
        "vacation_id" : vacationId
    }
    // console.log('Vacation id: ', vacationId)
    useEffect(() => {
        fetch(`https://vf24p8yepd.execute-api.us-west-1.amazonaws.com/dev/get-checklist`, {
            method: 'GET',
            headers: headersAPI
        })
        .then((response) => response.json()) 
        .then((data) => {
            if (data && data.length > 0 ){
                const tempChecklistArr = data.map((item) => {
                    return item.Item
                    // console.log(item.Item)
                })
            // console.log("Temp checklist", tempChecklistArr)
            setChecklistArr(tempChecklistArr)
            console.log("Updated Checklist Items:", checklistArr);  
            }
                
        })
                 
        .catch((err) => {
            console.error(err.message)
        })

    }, [vacationId])

useEffect(() => {
    console.log("USE EFFECT Updated Checklist Items:", checklistArr);
    }, [checklistArr]);

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
                    
                <Typography id="checklist-modal" variant="h6" component="h2">
                    {checklistArr.map((item) => <div> {item} </div>)}
                </Typography>
           
                <Button title="Close" onClick={onClose} size="small" variant='contained'/>
            </div>
        </Modal>
    )
}

export default ChecklistModal;