/**
 * ForrestHubLib - Library for communication with the server
 */

class ForrestHubLib {
    VERSION = '1.4.0';

    // RUNNING = 1;
    RUNNING = "running";
    PAUSED = "paused";
    STOPPED = "stopped";

    /**
     * @type {string}
     */
    project = "";

    constructor(isAdmin = false, url = `http://${window.location.hostname}:${window.location.port}`) {
        this.project = window.location.pathname.split('/')[1];
        this.isGamePage = true;
        this.isAdmin = isAdmin;


        if (typeof io === 'undefined') {
            throw new Error('Socket.io is not loaded.');
        }
        this.socket = io.connect(url);

        this.addEventListenerKey('connect', () => {
            console.log('Connected to the server!');
            this.socket.emit('get_game_status', null);
            this.removeOverlay();
        });

        this.addEventListenerKey('disconnect', () => {
            console.log('Disconnected from the server.');
            this.showOverlay('Byl jsi odpojen od serveru. <br/>Hra nejspíš skončila nebo nastala neočekávaná chyba.', null, "danger", true);
        });

        this.addEventListenerKey('admin_messages', (message) => {
            this.showOverlay(message, 5000, 'warning'); // Show for 5 seconds
        });

        this.addEventListenerKey('game_status', (status) => {
            if (status === this.RUNNING) {
                this.removeOverlay();
                if (this.isGamePage) {
                    this.showAlert('success', 'Hra spuštěna', 5000);
                }
            } else if (status === this.PAUSED) {
                this.showOverlay('Hra je pozastavena', null, 'info');
            } else if (status === this.STOPPED) {
                this.showOverlay('Hra byla ukončena', null, 'danger');
            } else {
                this.showOverlay('Neznámý stav hry', null, 'warning');
            }
            this.updateGameStatusUI(status);
        });
    }

    /**
     * Set if user is admin
     * @param isAdmin {boolean} - true if user is admin
     */
    setAdmin(isAdmin) {
        this.isAdmin = isAdmin;
    }

    /**
     * Set if user is on game page
     * @param isGameMode {boolean} - true if user is on game page
     */
    setGameMode(isGameMode) {
        this.isGamePage = isGameMode;
    }

    /**
     * Set project name (for database)
     * @param project {string} - project name
     */
    setProject(project) {
        this.project = project;
    }

    /**
     * Add event listener for key
     * @param eventKey
     * @param callback
     */
    addEventListenerKey(eventKey, callback) {
        this.socket.on(eventKey, (data) => {
            callback(data);
        });
    }

    /**
     * Emit event with data and return response
     * @param event - event name
     * @param data - data to send
     * @returns {Promise<unknown>}
     */
    emitWithResponse(event, data) {
        return new Promise((resolve, reject) => {
            this.emit(event, data, (response) => {
                if (response && response.status === 'ok') {
                    resolve(response);
                } else {
                    let message = `Chyba při zpracování události: ${event}`;
                    if (response && response.message) {
                        message = response.message;
                    }
                    console.error(message);
                    this.showOverlay(message, null);
                    reject(new Error(message));
                }
            });
        });
    }

    /**
     * Emit event with data and optional callback
     * @param event
     * @param data
     * @param callback
     */
    emit(event, data=null, callback = null) {
        if (callback) {
            this.socket.emit(event, data, callback);
        } else {
            this.socket.emit(event, data);
        }
    }

    /**
     * Set key with value and return response
     * @param key {string} - key name
     * @param value {any} - value to set
     */
    async setKey(key, value) {
        const {project} = this;
        await this.emitWithResponse('set_key', { project, key, value });
    }

    /**
     * Get key value
     * @param key {string} - key name
     * @param defaultValue {any} - default value if key does not exist
     * @returns {Promise<*>}
     */
    async getKey(key, defaultValue = null) {
        const {project} = this;
        const response = await this.emitWithResponse('get_key', { project, key, defaultValue });
        return response.data;
    }

    /**
     * Check if key exists
     * @param key {string} - key name
     * @returns {Promise<boolean>} - true if key exists
     */
    async hasKey(key) {
        const {project} = this;
        const response = await this.emitWithResponse('has_key', { project, key });
        return !!response?.exists;
    }

    /**
     * Delete key
     * @param key {string} - key name
     * @returns {Promise<void>}
     */
    async deleteKey(key) {
        const {project} = this;
        await this.emitWithResponse('delete_key', { project, key });
    }

    /////////////////////////// DATABASE ///////////////////////////

    /**
     * Set database value
     * @returns {Promise<{}>}
     */
    async getAllDatabase() {
        const db = await this.emitWithResponse('get_all_db');
        return db.data || {};
    }

    /**
     * Set database value
     * @returns {Promise<void>}
     */
    async deleteAllDatabase() {
        await this.emitWithResponse('delete_all_db');
    }

    /////////////////////////// DATABASE ARRAY ///////////////////////////

    /**
     * Add record to array
     * each record will have got unique id (recordId)
     * Store format: {y3XX50fxYK: <value>, 0U_dTy3IKg: <value>, ...}
     * @param arrayName {string} - array name
     * @param value {any} - initial value
     * @returns {Promise<void>}
     */
    async arrayAddRecord(arrayName, value) {
        const {project} = this;
        await this.emitWithResponse('array_add_record', {project , arrayName, value });
    }

    /**
     * Remove record from array by recordId
     * Store format: {y3XX50fxYK: <value>, 0U_dTy3IKg: <value>, ...}
     * @param arrayName {string} - array name
     * @param recordId {string} - record id
     * @returns {Promise<void>}
     */
    async arrayRemoveRecord(arrayName, recordId) {
        const {project} = this;
        await this.emitWithResponse('array_remove_record', { project, arrayName, recordId });
    }

    /**
     * Update record in array by recordId
     * @param arrayName {string} - array name
     * @param recordId {string} - record id
     * @param value {any} - new value
     * @returns {Promise<void>}
     */
    async arrayUpdateRecord(arrayName, recordId, value) {
        const {project} = this;
        await this.emitWithResponse('array_update_record', { project, arrayName, recordId, value });
    }

    /**
     * Get all records from array by arrayName
     * @param arrayName {string} - array name
     * @returns {Promise<*>} - record map {recordId: value, ...}
     */
    async arrayGetAllRecords(arrayName) {
        const {project} = this;
        const response = await this.emitWithResponse('array_get_all_records', { project, arrayName });
        return response.data;
    }

    /**
     * Get record from array by recordId
     * @param arrayName {string} - array name
     * @param recordId {string} - record id
     * @returns {Promise<*>} - record value
     */
    async arrayGetRecordId(arrayName, recordId) {
        const {project} = this;
        const response = await this.emitWithResponse('array_get_record_id', { project, arrayName, recordId });
        return response.data;
    }

    /**
     * Clear all records from array
     * @param arrayName {string} - array name
     * @returns {Promise<void>}
     */
    async arrayClearRecords(arrayName) {
        const {project} = this;
        await this.emitWithResponse('array_clear_records', { project, arrayName });
    }

    /**
     * List all projects stored in the database
     * @returns {Promise<*>}
     */
    async arrayListProjects() {
        const {project} = this;
        const response = await this.emitWithResponse('array_list_projects', {});
        return response.data;
    }


    updateGameStatusUI(status) {
        let statusText = "";
        switch (status) {
            case this.RUNNING:
                statusText = "Běží";
                break;
            case this.PAUSED:
                statusText = "Pozastavena";
                break;
            case this.STOPPED:
                statusText = "Ukončena";
                break;
            default:
                statusText = "?";
        }
        document.querySelectorAll(".game_status").forEach((element) => {
            element.innerText = statusText;
        });
    }

    showAlert(type, message, duration = 5000) {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
        alertDiv.style.position = 'fixed';
        alertDiv.style.top = '0';
        alertDiv.style.left = '50%';
        alertDiv.style.transform = 'translateX(-50%)';
        alertDiv.style.width = '100%';
        alertDiv.style.zIndex = '9999';
        alertDiv.role = 'alert';
        alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
        document.querySelector('.container').insertAdjacentElement('afterbegin', alertDiv);
        setTimeout(() => alertDiv.remove(), duration);
    }

    showOverlay(text, duration = null, status = 'info', forceShow = false) {
        if (this.isAdmin && !forceShow) {
            this.showAlert('info', `Zpráva: ${text}`, 5000);
            return;
        }

        let overlay = document.createElement('div');
        let message = document.createElement('div');
        let countdown = document.createElement('div');

        overlay.id = 'overlay';
        overlay.style.position = 'fixed';
        overlay.style.top = '0';
        overlay.style.left = '0';
        overlay.style.width = '100%';
        overlay.style.height = '100%';
        overlay.style.backgroundColor = 'rgba(5,5,0,0.96)';
        overlay.style.zIndex = '9999';

        message.id = 'overlay-message';
        message.innerHTML = text;
        message.style.position = 'absolute';
        message.style.top = '30%';
        message.style.left = '50%';
        message.style.transform = 'translate(-50%, -50%)';
        message.style.color = 'white';
        message.style.fontFamily = 'sans-serif';
        message.style.fontSize = '32px';
        message.style.textAlign = 'center';

        countdown.style.position = 'absolute';
        countdown.style.top = '40%';
        countdown.style.left = '50%';
        countdown.style.transform = 'translate(-50%, -50%)';
        countdown.style.color = 'white';
        countdown.style.fontFamily = 'sans-serif';
        countdown.style.fontSize = '24px';
        countdown.style.textAlign = 'center';

        overlay.appendChild(message);
        overlay.appendChild(countdown);
        document.body.appendChild(overlay);

        if (duration) { // duration in ms
            let remainingTime = duration / 1000;
            countdown.innerText = `Zbývá ${remainingTime}s`;

            let countdownInterval = setInterval(() => {
                remainingTime -= 1;
                countdown.innerText = `Zbývá ${remainingTime}s`;

                if (remainingTime <= 0) {
                    clearInterval(countdownInterval);
                    this.removeOverlay();
                }
            }, 1000);
        }
    }

    removeOverlay() {
        let overlay = document.getElementById('overlay');
        if (overlay) {
            document.body.removeChild(overlay);
        }
    }
}

window.forrestHubLib = new ForrestHubLib("fh");
