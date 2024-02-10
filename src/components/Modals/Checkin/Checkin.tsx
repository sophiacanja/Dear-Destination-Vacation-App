import React, { useEffect, useState } from 'react';
import Button from '../../Button/Button.tsx';
import './Checkin.css'
import {Checkbox, FormGroup, Modal, TextField, Typography, FormControlLabel, FormLabel, Stack} from "@mui/material";

type CheckinModalProps = {
    onClose: () => void;
    open: boolean;
    vacationId: string
}

const CheckinModal: React.FC<CheckinModalProps> = ({open, onClose, vacationId}) => {
    const [paymentMethod, setPaymentMethod] = useState<string | null>(null)
    
    const handlePaymentChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setPaymentMethod(event.target.value)
    }

    const handleCheckin = () => {
        console.log("button clicked! implement api call here")
    }
    return(
        <Modal
            open={open}
            onClose={onClose}
            aria-labelledby="checkin-modal"
            aria-describedby="checkin-modal-description"
        >
            <div id="checkin-modal-container"> 
                <Typography id="checkin-modal"variant="h4" component="h2" sx={{mt:2, textDecoration: 'underline'}}>
                    Ready to RSVP? 
                </Typography>  

                <div id="checkin-modal-description">
                    RSVP in advance to ensure you're counted in the activities and the budget!
                </div>
                
                <FormGroup>
                    <div id="checkin-modal-form-entry">
                        <FormLabel component="legend">Name</FormLabel>
                    </div>
                    <TextField required id="outlined-required"/>
                    

                    <div id= "checkin-modal-form-entry">
                        <FormLabel component="legend">Payment Preference</FormLabel>
                    </div>

                    <div id="checkbox-items">
                        <FormControlLabel  
                            control={<Checkbox value="Venmo" checked={paymentMethod === 'Venmo'} onChange={handlePaymentChange} />} 
                            label="Venmo"
                        />

                        <FormControlLabel  
                            control={<Checkbox value="Apple Pay" checked={paymentMethod === 'Apple Pay'} onChange={handlePaymentChange} />} 
                            label="Apple Pay"
                        />      
                        
                        <FormControlLabel  
                            control={<Checkbox value="Zelle" checked={paymentMethod === 'Zelle'} onChange={handlePaymentChange} />} 
                            label="Zelle"
                        />
                    </div>

                    <div id= "checkin-modal-form-entry">
                        <FormLabel component="legend">Payment username/contact</FormLabel>
                    </div>
                    <TextField required id="outlined-required"/>
                    

                    <div id= "checkin-modal-form-entry">
                        <FormLabel component="legend">Add a friendly message to the organizer!</FormLabel>
                    </div>
                    <TextField required id="outlined-required"/>
                   
                    <div id= "checkin-modal-form-entry">
                        <Stack justifyContent="center" spacing={3} direction="row">
                            <Button title="Submit" size="small" variant="contained" onClick={handleCheckin}/>
                            <Button title="Cancel" size="small" variant="outlined" onClick={onClose}/>
                        </Stack>
                    </div>

                    </FormGroup>
                </div>

        </Modal>
    )
}
export default CheckinModal