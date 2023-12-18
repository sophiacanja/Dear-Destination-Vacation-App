import React from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';

interface componentProps {
    title: string;
    content: string;
}

const MyCard: React.FC<componentProps> = ({title, content}) => {
    return(
        <Card>
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
            </CardContent>

        </Card>
    )
}

export default MyCard;
