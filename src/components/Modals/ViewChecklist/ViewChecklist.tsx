import React, { useEffect, useState } from 'react';
import Button from '../../Button/Button.tsx';
import './ViewChecklist.css'
import {Modal, Typography, Box} from "@mui/material";

// https://vf24p8yepd.execute-api.us-west-1.amazonaws.com/dev/get-checklist 
type ChecklistModalProps = {
    onClose: () => void;
    open: boolean;
    vacationId: string;
    vacationLocation: string; 
}


const ChecklistModal: React.FC<ChecklistModalProps> = ({open, onClose, vacationLocation, vacationId}) => {
    const [checklistArr, setChecklistArr] = useState([])
    const [dataPresent, setDataPresent] = useState(false)

    var headersAPI: any = {
        "vacation_id" : vacationId
    }
    useEffect(() => {
        fetch(`https://vf24p8yepd.execute-api.us-west-1.amazonaws.com/dev/get-checklist`, {
            method: 'GET',
            headers: headersAPI
        })
        .then((response) => response.json()) 
        .then((data) => {
            if (data && data.length > 0 ){
                setDataPresent(true)
                const tempChecklistArr = data.map((item) => {
                    return item.Item
                })
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
                <Typography id="checklist-modal" variant="h4" component="h2" sx={{mt:2, textDecoration:'underline'}}>
                Trip Checklist: {vacationLocation} 
                </Typography>
                    
                <Typography id="checklist-modal" variant="h6" component="h2">
                    {checklistArr.map((item) => <div> {item} </div>)}
                </Typography>

                {!dataPresent && (
                    <Typography id="checklist-modal" variant="h6" component="h2">
                        No checklist provided by the organizer yet! 
                    </Typography>
                )}
           
                <Button title="Close" onClick={onClose} size="small" variant='contained'/>
            </div>
        </Modal>
    )
}

export default ChecklistModal;