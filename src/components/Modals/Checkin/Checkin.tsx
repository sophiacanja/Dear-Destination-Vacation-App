import React, { useEffect, useState } from 'react';
import Button from '../../Button/Button.tsx';
import './Checkin.css';
import SuccessBanner from '../../Banners/Success/Success.tsx';
import {Checkbox, FormGroup, Modal, TextField, Typography, FormControlLabel, FormLabel, Stack, InputLabel} from "@mui/material";

type CheckinModalProps = {
    onClose: () => void;
    open: boolean;
    vacationId: string
}

const CheckinModal: React.FC<CheckinModalProps> = ({open, onClose, vacationId}) => {
    const [paymentMethod, setPaymentMethod] = useState<string | null>(null)
    const [name, setName] = useState("")
    const [paymentInfo, setPaymentInfo] = useState("")
    const [message, setMessage] = useState("")
    const [showSuccessBanner, setShowSuccessBanner] = useState(false)
    const [isSubmitting, setIsSubmitting] = useState(false)
    
    const handlePaymentChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setPaymentMethod(event.target.value)
    }

    var bodyAPI: any ={
        "VacationId" : vacationId,
        "AttendeeName" : name,
        "PaymentType" : paymentMethod,
        "PaymentInfo" : paymentInfo, 
        "Message" : message
    }

    const handleCheckin = () => {
        setIsSubmitting(true)
        console.log("button clicked! implement api call here")
        fetch(`https://sxlte22z2k.execute-api.us-west-1.amazonaws.com/dev/put-checkin`, {
        method:'POST',
        body: JSON.stringify(bodyAPI)
    })
        .then((response) => {
            if(response.ok){
                console.log("success banner is set to true")
                setShowSuccessBanner(true)
            }else {
                throw response;
            }
        
        })
        .catch((err) => {
            console.error("Error making POST request ", err.message)
        })
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
                        <InputLabel htmlFor="name">Name</InputLabel>
                        <TextField required id="name" value={name} onChange={(e) => setName(e.target.value)} />

                    </div>

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
                        <InputLabel htmlFor="payment-info">Payment username/contact</InputLabel>
                        <TextField required id="payment-info" value={paymentInfo} onChange={(e) => setPaymentInfo(e.target.value)} />
                    </div>
                    

                    <div id= "checkin-modal-form-entry">
                        <InputLabel htmlFor="message">Add a friendly message to the organizer!</InputLabel>
                        <TextField required id="message" value={message} onChange={(e) => setMessage(e.target.value)} />
                    </div>

                   
                    <div id= "checkin-modal-form-entry">
                        <Stack justifyContent="center" spacing={3} direction="row">
                            <Button title="Submit" size="small" variant="contained" onClick={handleCheckin} disabled={isSubmitting}/>
                            <Button title="Cancel" size="small" variant="outlined" onClick={onClose} disabled={isSubmitting}/>
                        </Stack>
                    </div>

                    </FormGroup>
                    {showSuccessBanner && (
                        <div className='success-message'>
                            <SuccessBanner message="Successfully checked in!"/>
                            <Button title="Close" size="small" variant="contained" onClick={onClose}/>
                        </div>
                    )}
                    
                </div>
                

        </Modal>
    )
}
export default CheckinModal