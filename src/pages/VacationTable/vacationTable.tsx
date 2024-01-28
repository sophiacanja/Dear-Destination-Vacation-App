import React, {useEffect, useState} from 'react';
import Button from '../../components/Button/Button.tsx'
import MyCard from '../../components/Card/MyCard.tsx';
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
    // this use effect calls the get api endpoint, turns the response body into a json obj, the data is stored in variable vacations 
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
        <div id = "vacation-table-container">
            <header id="sub-title"> My Upcoming Trips!</header>
            <Container maxWidth="sm">
                { vacations.map((vacation) => (
                    <div id="vacation-table">
                        <MyCard 
                            title={vacation.Location} 
                            content={`Departure Date: ${vacation.DepartureDate}`}
                            vacationId={vacation.VacationId}
                        />
                    </div>
                ))}
            </Container>
        </div>
    )    
}

export default VacationTable