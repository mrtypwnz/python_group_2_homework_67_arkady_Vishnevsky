import React from 'react';
import Hall from "../UI/Hall/Hall";


const HallCard = props => {

    const {name, id} = props.hall;

    const link = {
        text: 'Read more',
        url: '/halls/' + id
    };

    return <Hall header={name} link={link} className='w-100'/>;
};


export default HallCard;