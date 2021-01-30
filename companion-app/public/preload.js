const chokidar = require('chokidar');
const fs = require('fs');
const path = require('path');
const glob = require('glob');
let watcher; 


window.initFileWatcher = function(callback) {
    watcher = chokidar.watch('', {
        persistent: true
    });

    watcher.on('change', callback);
}

window.readFile = function(path) {
    const data = fs.readFileSync(path, 'utf8');
    return data;
}

const getDirectories = function(src, callback) {
    glob(src + '/**/DiscordKeys.lua', callback);
  };

window.walk = function(dir, callback) {
    dir = path.dirname(dir);
    getDirectories(dir, (err, res) => {
        let characters = [];
        res.forEach(path => {
            watcher.add(path);
            path = path.split("/");
            const server = path[path.length - 4];
            const character = path[path.length - 3];
            characters.push(`${character} - ${server}`)
        });
        callback(characters);
    });
}