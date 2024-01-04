import React, {useState} from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import Button from './Button'
import './MyCard.css';
import ChecklistIcon from '@mui/icons-material/Checklist';
import DescriptionIcon from '@mui/icons-material/Description';
import PersonAddIcon from '@mui/icons-material/PersonAdd';
import ChecklistModal from './ChecklistModal.tsx'
import {Container, Stack} from "@mui/material";

interface componentProps {
    title: string;
    content: string;
}

const [isChecklistModalOpen, setIsChecklistModalOpen] = useState(false)
const openChecklistModal = () => {
    setIsChecklistModalOpen(true)
}

const closeChecklistModal = () => {
    setIsChecklistModalOpen(false)
}

const MyCard: React.FC<componentProps> = ({title, content}) => {
    return(
        <Card className="vacation-card">
            <CardContent>
                <Typography variant="h5" component="div">
                <header> 
                    {title}
                </header>
                </Typography>

                <Typography variant="body2" color="text.secondary">
                <div>
                    {content}
                </div>
                </Typography>
                <Stack spacing={5} direction="row">
                    <Button 
                        title="Check In" 
                        size="small" 
                        variant="outlined"
                        icon = {<PersonAddIcon color="action" fontSize='large' />}
                    />
                    <Button 
                        title="View Checklist" 
                        size="small" 
                        variant="outlined" 
                        icon={<ChecklistIcon color="action" fontSize='large' />}
                        onClick={ () => openChecklistModal()}

                    /> 
                    {isChecklistModalOpen && 
                        <ChecklistModal
                            onClose={closeChecklistModal}
                            vacationId={1}
                        />
                    }
                    <Button 
                        title="View Itinerary" 
                        size="small" 
                        variant="outlined"
                        icon={<DescriptionIcon color="action" fontSize='large'/>} 
                    />
                </Stack> 
            </CardContent>

        </Card>
    )
}

export default MyCard;
