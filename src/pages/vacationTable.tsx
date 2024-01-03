import React, {useEffect, useState} from 'react';
import Button from '../components/Button.tsx'
import MyCard from '../components/MyCard';
import Container from '@mui/material/Container';
import './vacationTable.css';

// invoke url for get:  https://qtlldz9f9l.execute-api.us-west-1.amazonaws.com/dev/get-vacation

interface Vacation {
    VacationId : string
    Location : string
    DepartureDate: string
}

const VacationTable: React.FC = () => {
    const [vacations, setVacations] = useState<Vacation[]>([]);

    const APIHeaders = {
        "Content-Type" : "application/json"
    }
    useEffect(()=>{
        fetch('https://qtlldz9f9l.execute-api.us-west-1.amazonaws.com/dev/get-vacation', {
            method: 'GET',
            headers: APIHeaders
        })
        .then((response) => response.json())
        .then((data) => {
            console.log(data)
            const parsedData = JSON.parse(data.body)
            setVacations(parsedData)
        })
        .catch((err) => {
            console.error(err.message)
        })
    }, [])

    return(
        <div className = "container">
            <Container maxWidth="sm">
                { vacations.map((vacation) => (
                        <MyCard 
                            title={vacation.Location} 
                            content={`Departure Date: ${vacation.DepartureDate}`}
                    />
                ))}
            </Container>
        </div>
    )    
}

export default VacationTable