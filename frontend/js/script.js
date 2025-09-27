document.getElementById('uploadForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent default form submission

    const formData = new FormData();
    const emailText = document.getElementById('emailText');
    const emailFile = document.getElementById('emailFile')
    
    if (emailText === '' && emailFile.files.length === 0) {
        console.log("ambas vazias.");
    }

    else {
        formData.append(emailText);
        formData.append(emailFile);
        
        fetch('/verify_email', { // Replace with your actual upload endpoint
        method: 'POST',
        body: formData
        })
        .then(response => response.json())
        .then(data => {
            console.log('Upload successful:', data);
            alert('File uploaded successfully!');
            })
            .catch(error => {
                console.error('Error uploading file:', error);
                alert('Error uploading file.');
        });
    }
});