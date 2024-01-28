import React, { useEffect, useState } from 'react';
import Button from '../../Button/Button.tsx';
import './ViewChecklist.css'
import {Modal, Typography, Box} from "@mui/material";


type ItineraryModalProps = {
    onClose: () => void;
    open: boolean;
    vacationId: string
}

const ViewItineraryModal: React.FC<ItineraryModalProps> = ({open, onClose, vacationId }) => {

    return (
        <div> VIEW ITINERARY MODAL </div>
    )
}
export default ViewItineraryModal;