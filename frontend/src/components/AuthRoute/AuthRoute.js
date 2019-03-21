import React from 'react'
import {Redirect, Route} from 'react-router'


// const AuthRoute = (props) => {
//     const {Component, path, ...other} = props;
//
//     if(localStorage.getItem('auth-token')) {
//         return <Route path={path} {...other}><Component/></Route>
//     } else {
//         return <Redirect to={{
//             pathname: "/login",
//             state: {next: path}
//         }}/>
//     }
// };


const AuthRoute = (props) => {
    if(localStorage.getItem('auth-token')) {
        return <Route {...props} />
    } else {
        return <Redirect to={{
            pathname: "/login",
            state: {next: props.location}
        }}/>
    }
};

export default AuthRoute;
