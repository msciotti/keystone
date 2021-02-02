import React from 'react';
import { Redirect } from 'react-router-dom';

export default class AuthRedirect extends React.Component {
    constructor(props) {
        super(props);
        console.log(props);
        const { code } = props;
        this.state = {
            isPending: true,
            code: code
        };
    }
    async componentDidMount() {
        const code = this.props.location.state.code;
        const body = {
            "code": code
        };

        const res = await fetch("https://keystone.masonsciotti.com/token", {
            method: "POST",
            body: JSON.stringify(body),
            headers: {
                "Content-Type": "application/json"
            }
        });

        const token = await res.json();
        localStorage.setItem("token", JSON.stringify(token));
        this.setState({
            isPending: false
        })
    }

    render() {
        const {isPending} = this.state;
        return isPending ? (<p>Authorizing...</p>) : (<Redirect to="/authorized" />);
    }
}