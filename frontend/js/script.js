document.getElementById('uploadForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent default form submission

    const formData = new FormData();
    const emailText = document.getElementById('emailText').value;
    const emailFile = document.getElementById('emailFile');
    
    if (emailText === "" && emailFile.files.length === 0) {
        console.log("ambas vazias.");
    }

    else {
        formData.append("text", emailText);
        formData.append("file", emailFile.files[0]);
        
        fetch('/verify_email', { // Replace with your actual upload endpoint
        method: 'POST',
        body: formData
        })
        .then(response => response.json())
        .then(data => {
            console.log('Upload successful:', data);
            })
            .catch(error => {
                console.error('Error uploading file:', error);
        });
    }
});