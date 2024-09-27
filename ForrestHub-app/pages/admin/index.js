
if (!forrestHubLib) {
    forrestHubLib = window.forrestHubLib || new ForrestHubLib();
}

forrestHubLib.setAdmin(true);
forrestHubLib.setGameMode(false);

let globalData = {};


forrestHubLib.addEventListenerKey("connect", async () => {
    forrestHubLib.showAlert('success', 'Připojeno k serveru.');
    await loadAndDisplayData();
    forrestHubLib.emit('get_game_status', null);
});


setInterval(loadAndDisplayData, 1000);

async function loadAndDisplayData() {
    try {
        globalData = await forrestHubLib.getAllDatabase();
        displayData();
    } catch (error) {
        forrestHubLib.showAlert('danger', 'Error loading data: ' + error.message);
    }
}

function displayData() {
    const dataList = document.getElementById('data-list');
    dataList.innerHTML = ''; // Clear existing data

    if (Object.keys(globalData).length === 0) {
        dataList.innerHTML = '<li class="list-group-item">Žádná data</li>';
        return;
    }

    for (const [key, value] of Object.entries(globalData)) {
        const li = document.createElement('li');
        li.className = 'list-group-item d-flex justify-content-between align-items-center';
        li.innerHTML = `
            <span><strong>${key}:</strong> <span id="${key}">${JSON.stringify(value)}</span></span>
            <div>
                <button class="btn btn-sm btn-primary" onclick="openEditModal('${key}')">Edit</button>
                <button class="btn btn-sm btn-danger" onclick="deleteData('${key}')">Delete</button>
            </div>
        `;
        dataList.appendChild(li);
    }
}

function openEditModal(key) {
    const value = globalData[key];
    document.getElementById('editKey').value = key;
    const editType = document.getElementById('editType');
    const editValue = document.getElementById('editValue');

    // Clear previous content
    document.getElementById('editValue').value = '';
    document.getElementById('listItems').innerHTML = '';
    document.getElementById('keyValuePairs').innerHTML = '';

    if (Array.isArray(value)) {
        editType.value = 'list';
        updateEditForm();
        value.forEach(item => addListItem(item));
    } else if (typeof value === 'object' && value !== null) {
        editType.value = 'keyvalue';
        updateEditForm();
        Object.entries(value).forEach(([k, v]) => addKeyValuePair(k, v));
    } else {
        editType.value = 'value';
        updateEditForm();
        editValue.value = value;
    }

    const editModal = new bootstrap.Modal(document.getElementById('editModal'));
    editModal.show();
}

function updateEditForm() {
    const type = document.getElementById('editType').value;
    document.getElementById('editValueContainer').classList.toggle('d-none', type !== 'value');
    document.getElementById('editListContainer').classList.toggle('d-none', type !== 'list');
    document.getElementById('editKeyValueContainer').classList.toggle('d-none', type !== 'keyvalue');
}

function addListItem(value = '') {
    const listItems = document.getElementById('listItems');
    const itemDiv = document.createElement('div');
    itemDiv.className = 'input-group mb-2';
    itemDiv.innerHTML = `
        <input type="text" class="form-control" value="${value}">
        <button class="btn btn-outline-danger" type="button" onclick="this.parentElement.remove()">Remove</button>
    `;
    listItems.appendChild(itemDiv);
}

function addKeyValuePair(key = '', value = '') {
    const keyValuePairs = document.getElementById('keyValuePairs');
    const pairDiv = document.createElement('div');
    pairDiv.className = 'input-group mb-2';
    pairDiv.innerHTML = `
        <input type="text" class="form-control" placeholder="Key" value="${key}">
        <input type="text" class="form-control" placeholder="Value" value="${value}">
        <button class="btn btn-outline-danger" type="button" onclick="this.parentElement.remove()">Remove</button>
    `;
    keyValuePairs.appendChild(pairDiv);
}

async function saveData() {
    const key = document.getElementById('editKey').value;
    const type = document.getElementById('editType').value;
    let value;

    if (type === 'value') {
        value = document.getElementById('editValue').value;
    } else if (type === 'list') {
        value = Array.from(document.querySelectorAll('#listItems input')).map(input => input.value);
    } else if (type === 'keyvalue') {
        value = {};
        document.querySelectorAll('#keyValuePairs .input-group').forEach(pair => {
            const [keyInput, valueInput] = pair.querySelectorAll('input');
            value[keyInput.value] = valueInput.value;
        });
    }

    try {
        await forrestHubLib.setKeyBroadcast(key, value);
        globalData[key] = value; // Update local data
        displayData(); // Refresh the display
        forrestHubLib.showAlert('success', `Value for ${key} updated successfully.`);
        bootstrap.Modal.getInstance(document.getElementById('editModal')).hide();
    } catch (error) {
        forrestHubLib.showAlert('danger', `Error updating value: ${error}`);
    }
}

async function deleteData(key) {
    if (confirm(`Opravdu si přeješ smazat data s klíčem: ${key}`)) {
        try {
            await forrestHubLib.deleteKey(key);
            delete globalData[key]; // Remove from local data
            displayData(); // Refresh the display
            forrestHubLib.showAlert('success', `Klíč '${key}' smazán úspěšně`);
        } catch (error) {
            forrestHubLib.showAlert('danger', `Chyba mazání ${key}: ${error}`);
        }
    }
}

forrestHubLib.addEventListenerKey('update_clients', (data) => {
    document.getElementById('connected_clients').innerText = data.count;
});

function sendAdminMessage() {
    const adminMessage = document.getElementById('adminMessage');
    if (adminMessage.value.trim() !== '') {
        forrestHubLib.socket.emit('send_admin_message', adminMessage.value);
        document.getElementById('lastAdminMessage').innerText = adminMessage.value;
        adminMessage.value = '';
        forrestHubLib.showAlert('success', 'Zpráva odeslána.');
    } else {
        forrestHubLib.showAlert('warning', 'Napište nejprve zprávu.');
    }
}

document.getElementById("game_start").addEventListener("click", function () {
    forrestHubLib.emit("set_game_status", forrestHubLib.RUNNING);
});

document.getElementById("game_pause").addEventListener("click", function () {
    forrestHubLib.emit('set_game_status', forrestHubLib.PAUSED);
});

document.getElementById("game_stop").addEventListener("click", function () {
    forrestHubLib.emit('set_game_status', forrestHubLib.STOPPED);
});


document.getElementById("download-button").addEventListener("click", function () {
    window.location.href = "/download-data";
});

document.getElementById("clear-button").addEventListener("click", async function () {
    if (confirm("Are you sure you want to clear all data? This action cannot be undone.")) {
        await forrestHubLib.deleteAllDatabase();
    }
});

document.getElementById("upload-button").addEventListener("click", async function () {
    const fileInput = document.getElementById("uploadFile");
    const file = fileInput.files[0];

    if (file) {
        const formData = new FormData();
        formData.append("file", file);

        try {
            const response = await fetch("/upload-data", {
                method: "POST",
                body: formData
            });
            const data = await response.json();
            if (data.status === "success") {
                forrestHubLib.showAlert('success', "Data successfully uploaded.");
                await loadAndDisplayData(); // Reload and display the new data
            } else {
                forrestHubLib.showAlert('danger', "An error occurred while uploading the data.");
            }
        } catch (error) {
            console.error("Error uploading file:", error);
            forrestHubLib.showAlert('danger', "An error occurred while uploading the file.");
        }
    } else {
        forrestHubLib.showAlert('warning', "Please select a file to upload.");
    }
});
