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

function getVacations(): Promise<Vacation[]>{
    const headers: Headers = new Headers()
    headers.set('Content-Type', 'application/json')
    headers.set('Accept', 'application/json')

    const request: RequestInfo = new Request('https://qtlldz9f9l.execute-api.us-west-1.amazonaws.com/dev/get-vacation',{
        method: 'GET',
        headers: headers
    })

    return fetch(request)
        .then((res) => {
            if (!res.ok) {
            throw new Error(`HTTP error! Status: ${res.status}`);
            }
            return res.json();
        })
        .then((res) => {
            console.log(res);
            return res as Vacation[];
        })
        .catch((error) => {
            console.error('Error during fetch:', error);
            throw error; // rethrow the error to be caught by the caller
        });
}

const VacationTable: React.FC = () => {
    const [vacations, setVacations] = useState<Vacation[]>([]);

    useEffect(()=>{
        const fetchData = async () => {
            try {
                const data = await getVacations();
                if (Array.isArray(data)) {
                    setVacations(data);
                }
                else {
                    console.error("invalid data format:", data);
                }
            } catch (error){
                console.error('Error fetching data:', error);
            }
        };
        fetchData();
    }, [])

    return(
        <div className = "container">
            <Container maxWidth="sm">
                {vacations.map((vacation) => (
                    <MyCard 
                        title={vacation.Location} 
                        content="hello"
                        // content={`Departure Date: ${vacation.DepartureDate}`}
                    />
                ))}
            </Container>
        </div>
    )    
}

export default VacationTable