function saveToken(token) {
    localStorage.setItem("token", "token");
}

function getToken() {
    return localStorage.getItem("token");
}

export default {
    saveToken,
    getToken
}