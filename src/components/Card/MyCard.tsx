import React, {useState} from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import Button from '../Button/Button.tsx'
import './MyCard.css';
import ChecklistIcon from '@mui/icons-material/Checklist';
import DescriptionIcon from '@mui/icons-material/Description';
import PersonAddIcon from '@mui/icons-material/PersonAdd';

import ChecklistModal from '../Modals/ViewChecklist/ViewChecklist.tsx'
import ItineraryModal from '../Modals/ViewItinerary/ViewItinerary.tsx'
import CheckinModal from '../Modals/Checkin/Checkin.tsx'
import {Container, Stack} from "@mui/material";

interface componentProps {
    title: string;
    content: string;
    vacationId: string;
}


const MyCard: React.FC<componentProps> = ({title, content, vacationId}) => {
    const [isChecklistModalOpen, setIsChecklistModalOpen] = useState(false)
    const [isItineraryModalOpen, setIsItineraryModalOpen] = useState(false)
    const [isCheckinModalOpen, setIsCheckinModalOpen] = useState(false)

    const closeItineraryModal = () => {
        setIsItineraryModalOpen(false)
    }

    const openItineraryModal = () => {
        setIsItineraryModalOpen(true)
    }

    const closeChecklistModal = () => {
        setIsChecklistModalOpen(false)
    }

    const openChecklistModal = () => {
        setIsChecklistModalOpen(true)
    }

    const openCheckinModal = () => {
        setIsCheckinModalOpen(true)
    }

    const closeCheckinModal = () => {
        setIsCheckinModalOpen(false)
    }

    return(
        <div className="vacation-card">
        <Card>
            <CardContent>
                <Typography variant="h5" component="div">
                <header> 
                    {title}
                </header>
                </Typography>

                <Typography variant="body2" color="text.secondary" fontSize="large">
                <div id= "card-content">
                    {content}
                </div>
                </Typography>
                <Stack spacing={5} direction="row">
                    <Button 
                        title="Check In" 
                        size="small" 
                        variant="outlined"
                        icon = {<PersonAddIcon color="action" fontSize='large' />}
                        onClick={() => openCheckinModal()}
                    />
                    {isCheckinModalOpen && 
                        <CheckinModal
                            open={isCheckinModalOpen}
                            onClose={() => closeCheckinModal()}
                            vacationId = {vacationId}
                        />

                    }
                    <Button 
                        title="View Checklist" 
                        size="small" 
                        variant="outlined" 
                        icon={<ChecklistIcon color="action" fontSize='large' />}
                        onClick={ () => openChecklistModal()}

                    /> 
                    {isChecklistModalOpen && 
                        <ChecklistModal
                            open={isChecklistModalOpen}
                            onClose={closeChecklistModal}
                            vacationLocation={title}
                            vacationId={vacationId}
                        />
                    }
                    <Button 
                        title="View Itinerary" 
                        size="small" 
                        variant="outlined"
                        icon={<DescriptionIcon color="action" fontSize='large'/>} 
                        onClick={ () => openItineraryModal()}
                    />
                    {isItineraryModalOpen && 
                        <ItineraryModal
                            open={isItineraryModalOpen}
                            onClose={closeItineraryModal}
                            vacationId={vacationId}
                        />
                    }
                </Stack> 
            </CardContent>

        </Card>
        </div>
    )
}

export default MyCard;
