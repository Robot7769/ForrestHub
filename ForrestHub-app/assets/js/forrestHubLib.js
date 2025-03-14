/**
 * ForrestHubLib - Library for communication with the server
 */

class ForrestHubLib {
    RUNNING = "running";
    PAUSED = "paused";
    STOPPED = "stopped";

    constructor(isGame = true, url = "http://" + window.location.hostname + ":" + window.location.port) {
        this.project = window.location.pathname.split('/')[1];
        this.isGamePage = isGame;

        if (typeof io === 'undefined') {
            throw new Error('Socket.io is not loaded.');
        }
        this.socket = io.connect(url);

        this.addEventListenerKey('connect', () => {
            console.log('Connected to the server!');
            this.socket.emit('game_status_get', null);
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
                    this.showAlert('success', 'Hra spuštěna', 2000);
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

    /////////////////////////// DATABASE OPERATIONS ///////////////////////////

    /**
     * Set database value
     * @returns {Promise<{}>}
     */
    async dbGetAllData() {
        const db = await this.emitWithResponse('db_get_all_data');
        return db.data || {};
    }

    /**
     * Set database value
     * @returns {Promise<void>}
     */
    async dbDeleteAllData() {
        await this.emitWithResponse('db_delete_all_data');
    }

    /////////////////////////// DATABASE VAR ///////////////////////////

    _getProject(projectOverride = null) {
        if (projectOverride) {
            return projectOverride;
        }
        return this.project;
    }

    /**
     * Set key with value and return response
     * @param key {string} - key name
     * @param value {any} - value to set
     * @param projectOverride {string} - override project name if accessing from Admin page
     */
    async varKeySet(key, value, projectOverride = null) {
        const project = this._getProject(projectOverride);
        await this.emitWithResponse('var_key_set', { project, key, value });
    }

    /**
     * Get key value
     * @param key {string} - key name
     * @param projectOverride {string} - override project name if accessing from Admin page
     * @returns {Promise<*>}
     */
    async varKeyGet(key, projectOverride = null) {
        const project = this._getProject(projectOverride);
        const response = await this.emitWithResponse('var_key_get', { project, key, project });
        return response.data;
    }

    /**
     * Check if key exists
     * @param key {string} - key name
     * @param projectOverride {string} - override project name if accessing from Admin page
     * @returns {Promise<boolean>} - true if key exists
     */
    async varKeyExist(key, projectOverride = null) {
        const project = this._getProject(projectOverride);
        const response = await this.emitWithResponse('var_key_exist', { project, key });
        return !!response?.exists;
    }

    /**
     * Delete key
     * @param key {string} - key name
     * @param projectOverride {string} - override project name if accessing from Admin page
     * @returns {Promise<void>}
     */
    async varKeyDelete(key, projectOverride = null) {
        const project = this._getProject(projectOverride);
        await this.emitWithResponse('var_key_delete', { project, key });
    }

    /////////////////////////// DATABASE ARRAY ///////////////////////////

    /**
     * Add record to array
     * each record will have got unique id (recordId)
     * Store format: {y3XX50fxYK: <value>, 0U_dTy3IKg: <value>, ...}
     * @param arrayName {string} - array name
     * @param value {any} - initial value
     * @param projectOverride {string} - override project name if accessing from Admin page
     * @returns {Promise<void>}
     */
    async arrayAddRecord(arrayName, value, projectOverride = null) {
        const project = this._getProject(projectOverride);
        await this.emitWithResponse('array_add_record', {project , arrayName, value });
    }

    /**
     * Remove record from array by recordId
     * Store format: {y3XX50fxYK: <value>, 0U_dTy3IKg: <value>, ...}
     * @param arrayName {string} - array name
     * @param recordId {string} - record id
     * @param projectOverride {string} - override project name if accessing from Admin page
     * @returns {Promise<void>}
     */
    async arrayRemoveRecord(arrayName, recordId, projectOverride = null) {
        const project = this._getProject(projectOverride);
        await this.emitWithResponse('array_remove_record', { project, arrayName, recordId });
    }

    /**
     * Update record in array by recordId
     * @param arrayName {string} - array name
     * @param recordId {string} - record id
     * @param value {any} - new value
     * @param projectOverride {string} - override project name if accessing from Admin page
     * @returns {Promise<void>}
     */
    async arrayUpdateRecord(arrayName, recordId, value, projectOverride = null) {
        const project = this._getProject(projectOverride);
        await this.emitWithResponse('array_update_record', { project, arrayName, recordId, value });
    }

    /**
     * Get all records from array by arrayName
     * Store format: {y3XX50fxYK: <value>, 0U_dTy3IKg: <value>, ...}
     * @param arrayName {string} - array name
     * @param projectOverride {string} - override project name if accessing from Admin page
     * @returns {Promise<*>} - record map {recordId: value, ...}
     */
    async arrayGetAllRecords(arrayName, projectOverride = null) {
        const project = this._getProject(projectOverride);
        const response = await this.emitWithResponse('array_get_all_records', { project, arrayName });
        return response.data;
    }

    /**
     * Clear all records from array
     * @param arrayName {string} - array name
     * @param projectOverride {string} - override project name if accessing from Admin page
     * @returns {Promise<void>}
     */
    async arrayClearRecords(arrayName, projectOverride = null) {
        const project = this._getProject(projectOverride);
        await this.emitWithResponse('array_clear_records', { project, arrayName });
    }

    /**
     * List all projects stored in the database
     * @returns {Promise<*>}
     */
    async arrayListProjects() {
        const response = await this.emitWithResponse('array_list_projects', {});
        return response.data;
    }


    updateGameStatusUI(status) {
        let statusText = "";
        switch (status) {
            case this.RUNNING:
                statusText = "Hra běží";
                break;
            case this.PAUSED:
                statusText = "Hra pozastavena";
                break;
            case this.STOPPED:
                statusText = "Hra ukončena";
                break;
            default:
                statusText = "?";
        }
        document.querySelectorAll(".game_status").forEach((element) => {
            element.innerText = statusText;
        });
    }

    showAlert(type, message, duration = 4000) {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show shadow`;
        alertDiv.style.position = 'fixed';
        alertDiv.style.top = '10px';
        alertDiv.style.left = '10px';
        alertDiv.style.right = '10px';
        alertDiv.style.margin = '0 auto';
        alertDiv.style.maxWidth = '600px';
        alertDiv.style.zIndex = '9999';
        alertDiv.role = 'alert';
        alertDiv.innerHTML = `
        <div class="d-flex justify-content-between align-items-center">
            <div>${message}</div>
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    `;

        document.body.appendChild(alertDiv);
        setTimeout(() => alertDiv.remove(), duration);
    }


    showOverlay(text, duration = null, status = 'info', forceShow = false) {
        if (!forceShow && !this.isGamePage) {
            console.log('Overlay not shown on non-game page');
            console.log("forceShow: " + forceShow);
            console.log("isGamePage: " + this.isGamePage);
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
