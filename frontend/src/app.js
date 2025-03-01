const FileUpload = require('./components/FileUpload');

document.addEventListener('DOMContentLoaded', () => {
    const fileUpload = new FileUpload();
    fileUpload.init();
});