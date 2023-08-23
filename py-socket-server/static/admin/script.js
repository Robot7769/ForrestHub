const adminClient = new SocketClient();

function editData(key) {
    let newValue = prompt("Edit the value:", document.getElementById(key).innerText);
    if (newValue != null) {
        adminClient.edit(key, newValue);
        document.getElementById(key).innerText = newValue;
    }
}

function deleteData(key) {
    if (confirm('Are you sure you want to delete this?')) {
        adminClient.delete(key);
        location.reload();
    }
}


// Update the connected devices count when the event is received
adminClient.addEventListener('update_clients', (data) => {
    document.getElementById('connected_clients').innerText = data.count;
});

function sendAdminMessage() {
    const adminMessage = document.getElementById('adminMessage')
    adminClient.socket.emit('send_admin_message', adminMessage.value);
    document.getElementById('lastAdminMessage').innerText = adminMessage.value;
    adminMessage.value = '';
}


document.getElementById("download-button").addEventListener("click", function() {
    window.location.href = "/download_data";
});

document.getElementById("clear-button").addEventListener("click", function() {
    if (window.confirm("Are you sure you want to clear all data?")) {
        // Add AJAX call here to Flask endpoint that clears the data
        fetch('/clear_data')
            .then(response => response.json())
            .then(data => {
                if (data.status === "success") {
                    alert("Data successfully cleared.");
                    // You can also add code here to update the UI to reflect the cleared data
                } else {
                    alert("An error occurred while clearing the data.");
                }
            });
    }
});

document.getElementById("upload-button").addEventListener("click", function() {
    const fileInput = document.getElementById("uploadFile");
    const file = fileInput.files[0];

    if (file) {
        const formData = new FormData();
        formData.append("file", file);

        fetch("/upload_data", {
            method: "POST",
            body: formData
        }).then(response => response.json())
            .then(data => {
                if (data.status === "success") {
                    alert("Data successfully uploaded.");
                    // Update the UI here if needed
                } else {
                    alert("An error occurred while uploading the data.");
                }
            }).catch(error => {
            console.error("Error uploading file:", error);
        });
    } else {
        alert("Please select a file to upload.");
    }
});


