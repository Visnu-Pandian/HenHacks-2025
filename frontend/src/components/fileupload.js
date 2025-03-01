class FileUpload {
    constructor() {
        this.fileInput = document.createElement('input');
        this.fileInput.type = 'file';
        this.fileInput.addEventListener('change', this.handleFileChange.bind(this));
        document.body.appendChild(this.fileInput);
    }

    handleFileChange(event) {
        const files = event.target.files;
        if (files.length > 0) {
            this.saveFileLocally(files[0]);
        }
    }

    async saveFileLocally(file) {
        const reader = new FileReader();
        reader.onload = async (event) => {
            const arrayBuffer = event.target.result;
            const buffer = Buffer.from(arrayBuffer);
            const fs = require('fs');
            const path = require('path');
            const uploadsDir = path.join(__dirname, 'uploads');

            if (!fs.existsSync(uploadsDir)) {
                fs.mkdirSync(uploadsDir);
            }

            const filePath = path.join(uploadsDir, file.name);
            fs.writeFile(filePath, buffer, (err) => {
                if (err) {
                    console.error('Error saving file locally:', err);
                } else {
                    console.log('File saved locally:', filePath);
                }
            });
        };
        reader.readAsArrayBuffer(file);
    }

    async uploadFile(file) {
        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch('/api/upload', {
                method: 'POST',
                body: formData,
            });

            if (response.ok) {
                console.log('File uploaded successfully');
            } else {
                console.error('File upload failed');
            }
        } catch (error) {
            console.error('Error uploading file:', error);
        }
    }
}

export default FileUpload;