import React from 'react';
import Button from '../components/Button.tsx'
import MyCard from '../components/MyCard';
import Container from '@mui/material/Container';
import './vacationTable.css';

const VacationTable: React.FC = () => {
    return(
        <div className = "container">
            <Container maxWidth="sm">
                <MyCard title="Juneper" content="Biggest Poop" />
            </Container>
        </div>
    )    
}

export default VacationTable