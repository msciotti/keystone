import React from 'react';
import { Redirect } from 'react-router-dom';

export default class AuthRedirect extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            isPending: true
        };
    }
    async componentDidMount() {
        const code = new URLSearchParams(this.props.location.search).get("code")
        const body = {
            "code": code
        };

        const res = await fetch("", {
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
        return this.state.isPending ? (<p>Authorizing...</p>) : (<Redirect to="/authorized" />);
    }
}