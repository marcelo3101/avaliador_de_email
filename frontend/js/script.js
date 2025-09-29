document.getElementById('uploadForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent default form submission


    const formData = new FormData();
    const emailText = document.getElementById('emailText').value;
    const emailFile = document.getElementById('emailFile');
    const overlay = document.getElementById("loadingOverlay");
    
    if (emailText === "" && emailFile.files.length === 0) {
        console.log("ambas vazias.");
    }

    else {
        formData.append("text", emailText);
        formData.append("file", emailFile.files[0]);
        
        // Display overlay
        overlay.style.display = "flex";

        fetch('/verify_email', { // Replace with your actual upload endpoint
        method: 'POST',
        body: formData
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById("emailClassification").textContent = data.classification;
            document.getElementById("aiSuggestion").textContent = data.response_suggestion;
            document.getElementById("templateSuggestion").textContent = data.template_suggestion;

            // Clear email file input


            overlay.style.display = "none";
            document.getElementById("results").hidden = false;  // Display results
        })
        .catch(error => {
            console.error('Error uploading file:', error);
        });
    }
});

// Copy to clipboard
function copyText(elementId) {
    const text = document.getElementById(elementId).innerText;
    navigator.clipboard.writeText(text).then(() => {
      alert("Texto copiado!");
    });
  }

  // Mailto
  function mailtoText(elementId) {
    const text = encodeURIComponent(document.getElementById(elementId).innerText);
    window.location.href = `mailto:?body=${text}`;
  }