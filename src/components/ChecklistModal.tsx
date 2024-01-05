import React from 'react';
import Button from './Button.tsx';
import './ChecklistModal.css'
import {Modal, Typography, Box} from "@mui/material";

// https://vf24p8yepd.execute-api.us-west-1.amazonaws.com/dev/get-checklist 
type ChecklistModalProps = {
    onClose: () => void
    open: boolean
    vacationId: number 
}

const style = {
    position: 'absolute' as 'absolute',
    top: '50%',
    left: '50%',
    transform: 'translate(-50%, -50%)',
    width: 400,
    bgcolor: 'background.paper',
    border: '2px solid #000',
    boxShadow: 24,
    borderRadius: 5,
    p: 4,
  };

const ChecklistModal: React.FC<ChecklistModalProps> = ({open, onClose, vacationLocation}) => {
    return(
        <Modal
            open={open}
            onClose={onClose}
            aria-labelledby="checklist-modal"
            aria-describedby="checklist-modal-description"
        >
            <div id="checklist-modal-container">
                <Typography id="checklist-modal" variant="h4" component="h2" sx={{mt:2}}>
                Checklist for {vacationLocation}
                </Typography>
           
                <Button title="Close" onClick={onClose} size="small" variant='contained'/>
            </div>
        </Modal>
    )
}

export default ChecklistModal;