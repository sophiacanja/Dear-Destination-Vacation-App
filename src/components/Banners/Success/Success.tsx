import React, {useState} from 'react';
import {useNavigate} from "react-router";
import Button from '../../Button/Button';
import './Success.css'

interface SuccessBannerProps {
    message: string;
}

const SuccessBanner: React.FC<SuccessBannerProps> = ({ message }) => {
    const [showBanner, setShowBanner] = useState(true)
  
    return (
        <div className="success-banner">
            {showBanner && 
                <p className='success-message'>{message}</p>
            }
        </div>

    )

}
export default SuccessBanner;