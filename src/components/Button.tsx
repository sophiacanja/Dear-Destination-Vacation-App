import React, { FC } from 'react';

interface ButtonProps {
    title: string; 
    onClick?: () => void; 
}

const Button: FC<ButtonProps>=({title, onClick}) => {
    return(
        <button onClick={onClick}>
            {title}
        </button>
    )
}

export default Button;