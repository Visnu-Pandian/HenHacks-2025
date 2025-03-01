const fs = require('fs');
const path = require('path');

const inputDirectory = path.join(__dirname, '../../input');

const fileHandler = {
    saveFile: (fileName, fileData) => {
        return new Promise((resolve, reject) => {
            const filePath = path.join(inputDirectory, fileName);
            fs.writeFile(filePath, fileData, (err) => {
                if (err) {
                    return reject(err);
                }
                resolve(filePath);
            });
        });
    }
};

module.exports = fileHandler;