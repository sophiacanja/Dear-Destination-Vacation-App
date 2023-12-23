import React from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import Button from './Button'
import './MyCard.css';

interface componentProps {
    title: string;
    content: string;
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
            <Button title="Check In" size="small"/> <t></t>
            <Button title="View Checklist" size="small"/> <t></t>
            <Button title="View Itinerary" size="small"/> 
            </CardContent>

        </Card>
    )
}

export default MyCard;
