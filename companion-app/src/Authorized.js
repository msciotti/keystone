import React from 'react';
import { Redirect } from 'react-router-dom';


export default class AuthorizedHome extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            token: null,
            currentUser: null,
            characters: localStorage.getItem("characters"),
            wowPath: localStorage.getItem("wowPath"),
            disableSelectPath: false
        }
        this.handleDirectorySelect = this.handleDirectorySelect.bind(this);
        this.handleFileChange = this.handleFileChange.bind(this);
        this.handleGetSyncedCharacters = this.handleGetSyncedCharacters.bind(this);
        window.initFileWatcher(this.handleFileChange);
    }

    async componentDidMount() {
        let { token, currentUser, characters, wowPath } = this.state;

        if (token == null) {
            token = this.getToken();
        }

        if (currentUser == null) {
            currentUser = await this.getCurrentUser(token);
        }

        if (characters == null) {
            characters = localStorage.getItem("characters");
        }

        if (wowPath != null) {
            window.walk(wowPath, this.handleGetSyncedCharacters);
        }

        this.setState({
            token: token,
            currentUser: currentUser,
            disableSelectPath: !!wowPath,
            characters: characters
        });
    }

    handleDirectorySelect(event) {
        const path = event.target.files[0].path;
        window.walk(path, this.handleGetSyncedCharacters);

        localStorage.setItem("wowPath", path);
        this.setState({
            wowPath: path,
            disableSelectPath: true
        });
    }

    handleGetSyncedCharacters(characters) {
        localStorage.setItem("characters", JSON.stringify(characters));
        this.setState({
            characters: characters
        });
    }

    handleFileChange(path) {
        const {currentUser} = this.state;

        const url = "https://keystone.masonsciotti.com/update-keystones";

        const fileData = window.readFile(path);
        const characterName = path.split("\\")[8];

        const body = {
            "key_data": fileData,
            "character": characterName,
            "user_id": currentUser.id,
            "username":`${currentUser.username}#${currentUser.discriminator}`
        };

        fetch(url, {
            method: "POST",
            body: JSON.stringify(body),
            headers: {
                "Content-Type": "application/json"
            }
        }).then(res => res.json());
    }

    render() {
        let {currentUser, disableSelectPath} = this.state;        

        return ( currentUser == null ? <p>Loading</p> :
            (
                <div>
                    <p>Logged in as: {`${currentUser.username}#${currentUser.discriminator}`}</p>
                    {disableSelectPath ? 
                        <p>Already tracking your characters</p> :
                        <div>
                            <p>Select your World of Warcraft executable</p>
                            <input type="file" onChange={this.handleDirectorySelect} disabled={disableSelectPath} />
                        </div>
                    }
                </div>
            )
        )
    }

    getToken() {
        const localStorageToken = localStorage.getItem("token");
        const tokenObject = JSON.parse(localStorageToken);

        if (tokenObject == null) {
            <Redirect to="/" />
        }

        return tokenObject;
    }

    async getCurrentUser(token) {
        if (token != null) {
            const res = await fetch("https://discord.com/api/v8/users/@me", {
                method: "GET",
                headers: {
                    "Authorization": `Bearer ${token.access_token}`
                }
            });

            return await res.json();
        }
    }
}