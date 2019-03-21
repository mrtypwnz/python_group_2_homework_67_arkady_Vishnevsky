import React, {Component} from 'react'
import {HALLS_URL, MOVIES_URL, SHOWS_URL} from "../../api-urls";
import {NavLink} from "react-router-dom";
import axios from 'axios';
import moment from "moment";
import ShowSchedule from "../../components/ShowSchedule/ShowSchedule";

const hall = {
    hall: null,
    shows: null
};

class HallDetail extends Component {
    state = hall;

    componentDidMount() {
        const match = this.props.match;
        axios.get(HALLS_URL + match.params.id)
            .then(response => {
                console.log(response.data);
                return response.data;
            })
            .then(hall => {
                this.setState({hall});
                this.loadShows(hall.id);

            })
            .catch(error => console.log(error));
    }


    loadShows = (hallId) => {
        const startsAfter = moment().format('YYYY-MM-DD HH:mm');
        const startsBefore = moment().add(3, 'days').format('YYYY-MM-DD');
        const query = encodeURI(`hall_id=${hallId}&starts_after=${startsAfter}&starts_before=${startsBefore}`);
        console.log(query);
        axios.get(`${SHOWS_URL}?${query}`).then(response => {
            this.setState(prevState => {
                let newState = {...prevState};
                newState.shows = response.data;
                return newState;
            });
            console.log(response.data, 'data');
        }).catch(error => {
            console.log(error);
            console.log(error.response);
        });
    };

     hallDelete = (hallId) => {
        axios.delete(HALLS_URL + hallId + '/')
            .then(response => {
                console.log(response.data, 'response');
                this.setState(hall);
                this.props.history.replace('/halls/');
            }).catch(error => {
            console.log(error);
        })
    };

    render() {
        if (!this.state.hall) return null;

        const {name, description, id} = this.state.hall;

        return <div className='mt-3'>

            <h1 className='display-4 font-weight-lighter'>{name}</h1>
            <p className='font-weight-normal'>{description}</p>


            <NavLink to={'/halls/' + id + '/edit'} className="btn btn-primary">Edit</NavLink>
            <button type='button' className='btn btn-primary ml-2' onClick={() => this.hallDelete(id)}>Delete</button>

            {this.state.shows ? <ShowSchedule shows={this.state.shows}/> : null}

        </div>;
    }
}


export default HallDetail;