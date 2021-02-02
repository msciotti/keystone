import React from 'react';
import { Redirect } from 'react-router-dom';

export default class Home extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            code: null
        };

        this.handleRedirect = this.handleRedirect.bind(this);
        this.auth = this.auth.bind(this);
    }

    render() {
        const {code} = this.state;
        const localStorageToken = localStorage.getItem("token");

        if (localStorageToken != null) {
            return <Redirect to="/authorized" />
        }


        if (code != null) {
            return <Redirect to={{
                pathname: "/redirect",
                state: { code: code }
            }} />;
        }

        return (
            <button onClick={this.auth}>
                Authorize
            </button>
        );
    }
    
    handleRedirect(url) {
        const code = url.split("code=")[1];
        this.setState({
            code: code
        });
    }

    auth() {
        const authUrl = "https://discord.com/api/oauth2/authorize?client_id=385208101109760000&redirect_uri=https%3A%2F%2Fkeystone.masonsciotti.com%2Fcallback&response_type=code&scope=identify";
        window.openAuthWindow(authUrl, this.handleRedirect);
    }
}
