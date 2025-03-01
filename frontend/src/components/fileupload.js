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
            this.uploadFile(files[0]);
        }
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