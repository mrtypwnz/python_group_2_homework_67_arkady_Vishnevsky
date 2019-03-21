import React, {Component} from 'react';


class Logout extends Component {
    componentDidMount() {
        localStorage.removeItem('auth-token');
        this.props.history.replace('/');
    };

    render() { return <h2>Выход</h2>; }
}


export default Logout;
