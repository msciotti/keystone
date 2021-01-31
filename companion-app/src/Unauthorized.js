import React from 'react';
import { Redirect } from 'react-router-dom';

export default class Home extends React.Component {
    render() {
        const localStorageToken = localStorage.getItem("token");
        return localStorageToken != null ? <Redirect to="/authorized" /> : (
            <button onClick={auth}>
                Authorize
            </button>
        );
    }
}

function auth() {
    window.open("https://discord.com/api/oauth2/authorize?client_id=385208101109760000&redirect_uri=http%3A%2F%2Flocalhost%3A3000%2Fredirect&response_type=code&scope=identify");
  }