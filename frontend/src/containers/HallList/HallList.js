import React, {Component} from 'react'
import {HALLS_URL} from "../../api-urls";
import HallCard from '../../components/HallCard/HallCard'
import axios from 'axios';

class HallsList extends Component {
    state = {
        halls: []
    };

    componentDidMount() {
        axios.get(HALLS_URL).then(response => {
            console.log(response.data);
            return response.data;
        }).then(halls => this.setState({halls}))
            .catch(error => console.log(error));
    }

    render() {
        return (
            <div className='row'>
                {this.state.halls.map(hall => {
                    return <div className='col-xs-12 col-sm-6 col-lg-4 mt-3 m-4' key={hall.id}>
                        <HallCard hall={hall}/>
                    </div>
                })}
            </div>
        );
    }
}

export default HallsList;