import React, { FC, ReactNode } from 'react';
import ButtonMUI from '@mui/material/Button';
import './Button.css';
import { start } from 'repl';

interface ButtonProps {
    title: string; 
    onClick?: () => void; 
    size?: 'small' | 'medium' | 'large';
    variant?: 'contained' | 'outlined';
    icon?: ReactNode;
    disabled?: boolean;
}

const Button: FC<ButtonProps>=({title, onClick, size, variant, icon, disabled}) => {
    return(
        <ButtonMUI size={size} variant={variant} onClick={onClick} startIcon={icon} disabled={disabled}>
        {title}
      </ButtonMUI>
    )
}

export default Button;