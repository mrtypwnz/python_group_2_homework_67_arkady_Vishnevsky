import React, {Component} from 'react'
import axios from "axios";
import {HALLS_URL} from "../../api-urls";


class HallForm extends Component {
    constructor(props) {
        super(props);

        const newHall = {
            name: "",
            description: "",
        };

        this.state = {
            submitEnabled: true,
            hall: newHall,
        };
        if (this.props.hall) {
            this.state.hall = this.props.hall
        }
    }

    componentDidMount() {
        axios.get(HALLS_URL)
            .then(response => {
                const hall = response.data;
                console.log(hall);
                this.setState(prevState => {
                    let newState = {...prevState};
                    newState.hall = this.props.hall;
                    return newState;
                });
            })
            .catch(error => {
                console.log(error);
                console.log(error.response);
                console.log(this.state.hall);
            });
    }

    enableSubmit = () => {
        this.setState(prevState => {
            let newState = {...prevState};
            newState.submitEnabled = true;
            return newState;
        });
    };

    disableSubmit = () => {
        this.setState(prevState => {
            let newState = {...prevState};
            newState.submitEnabled = false;
            return newState;
        });
    };



    updateMovieState = (fieldName, value) => {
        this.setState(prevState => {
            let newState = {...prevState};
            let hall = {...prevState.hall};
            hall[fieldName] = value;
            console.log(fieldName);
            newState.hall = hall;
            return newState;
        });
    };

    inputChanged = (event) => {
        const value = event.target.value;
        const fieldName = event.target.name;
        this.updateMovieState(fieldName, value);
    };


    submitForm = (event) => {
        if (this.state.submitEnabled) {
            event.preventDefault();
            this.disableSubmit();
            this.props.onSubmit(this.state.hall)
                .then(this.enableSubmit);
        }
    };

    render() {
        if (this.state.hall) {
            const {name, description} = this.state.hall;
            const {submitEnabled} = this.state;
            return <div>
                <form onSubmit={this.submitForm}>
                    <div className="form-group">
                        <label className="font-weight-bold">Название</label>
                        <input type="text" className="form-control" name="name" value={name}
                               onChange={this.inputChanged}/>
                    </div>
                    <div className="form-group">
                        <label>Описание</label>
                        <input type="text" className="form-control" name="description" value={description}
                               onChange={this.inputChanged}/>
                    </div>
                    <button disabled={!submitEnabled} type="submit"
                            className="btn btn-primary">Сохранить
                    </button>
                </form>
            </div>;
        } else {
            return <div>
                <form onSubmit={this.submitForm}>
                    <div className="form-group">
                        <label className="font-weight-bold">Название</label>
                        <input type="text" className="form-control" name="name" value={null}
                               onChange={this.inputChanged}/>
                    </div>
                    <div className="form-group">
                        <label>Описание</label>
                        <input type="text" className="form-control" name="description" value={null}
                               onChange={this.inputChanged}/>
                    </div>
                    <button type="submit"
                            className="btn btn-primary">Сохранить
                    </button>
                </form>
            </div>;
        }
    }
}


export default HallForm;