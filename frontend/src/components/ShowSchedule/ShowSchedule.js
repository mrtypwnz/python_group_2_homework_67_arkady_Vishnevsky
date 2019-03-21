import React, {Fragment} from 'react'
import moment from "moment";

const formatDate = (dateString) => {
    return moment(dateString).format('YYYY-MM-DD')
};

const ShowSchedule = props => {
    return <div className="mt-4">
        <h2 className='display-4 font-weight-lighter text-center'>Расписание сеансов</h2>
        {props.shows.map(show => {
            return <Fragment>
                <div className='border-dark border-bottom radius'>
                    <p className='font-weight-bold'>Фильм: <span className='font-weight-lighter'>{show.movie_name}</span></p>
                    <p className='font-weight-bold'>Зал: <span className='font-weight-lighter'>{show.hall_name}</span></p>
                    <p>Цена: <span className="badge badge-info category-badge mt-0">{show.ticket_price}</span></p>
                    <p className='font-weight-lighter'>Начало: <span className='font-weight-bold'>{formatDate(show.starts_at)}</span>,
                        Конец: <span className='font-weight-bold'>{formatDate(show.ends_at)}</span></p>
                </div>
            </Fragment>
        })}
    </div>
};


export default ShowSchedule
