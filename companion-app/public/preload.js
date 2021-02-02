const chokidar = require('chokidar');
const fs = require('fs');
const path = require('path');
const glob = require('glob');
const electron = require('electron');
const BrowserWindow = electron.remote.BrowserWindow;

let watcher; 


window.initFileWatcher = function(callback) {
    watcher = chokidar.watch('', {
        persistent: true
    });

    watcher.on('change', path => callback(path));
}

window.readFile = function(path) {
    const data = fs.readFileSync(path, 'utf8');
    return data;
}

const getDirectories = function(src, callback) {
    glob(src + '/**/DiscordKeys.lua', callback);
  };

window.walk = function(dir, callback, saveFirst) {
    dir = path.dirname(dir);
    getDirectories(dir, (err, res) => {
        let characters = [];
        res.forEach(path => {
            watcher.add(path);
            saveFirst(path);
            path = path.split("/");
            const server = path[path.length - 4];
            const character = path[path.length - 3];
            characters.push(`${character} - ${server}`)
        });
        callback(characters);
    });
}

let authWindow = new BrowserWindow({
    width: 900,
    height: 800,
    show: false
});

window.openAuthWindow = function(url, callback) {
    authWindow.loadURL(url);
    authWindow.show();

    authWindow.webContents.on('will-navigate', (e, url) => {
        authWindow.close();
        callback(url);
    });
}