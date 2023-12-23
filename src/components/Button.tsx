import React, { FC } from 'react';
import ButtonMUI from '@mui/material/Button';
import './Button.css';

interface ButtonProps {
    title: string; 
    onClick?: () => void; 
    size?: 'small' | 'medium' | 'large';
    variant?: 'contained' | 'outlined'
}

const Button: FC<ButtonProps>=({title, onClick, size, variant}) => {
    return(
        <ButtonMUI size={size} variant={variant} href="#outlined-buttons" onClick={onClick}>
        {title}
      </ButtonMUI>
    )
}

export default Button;