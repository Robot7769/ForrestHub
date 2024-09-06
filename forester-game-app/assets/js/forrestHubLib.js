class ForrestHubLib {
    // RUNNING = 1;
    RUNNING = "running";
    PAUSED = "paused";
    STOPPED = "stopped";

    constructor(isAdmin = false, url = `http://${window.location.hostname}:${window.location.port}`) {
        this.isGameMode = true;
        this.isAdmin = isAdmin;

        if (typeof io === 'undefined') {
            throw new Error('Socket.io is not loaded.');
        }
        this.socket = io.connect(url);

        this.addEventListenerKey('connect', () => {
            console.log('Connected to the server!');
            this.socket.emit('get_game_status');
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
                if (this.isGameMode) {
                    this.showAlert('success', 'Hra spuštěna', 5000);
                }
            } else if (status === this.PAUSED) {
                this.showOverlay('Hra je pozastavena', null, 'info');
            } else if (status === this.STOPPED) {
                this.showOverlay('Hra byla ukončena', null, 'danger');
            } else {
                this.showOverlay('Neznámý stav hry', null, 'warning');
            }
        });

        this.addEventListenerKey('full_screen', async (data) => {
            if (data === true) {
                await document.documentElement.requestFullscreen();
            } else {
                await document.exitFullscreen();
            }
        });

        this.addEventListenerKey("game_status", (data) => {
            this.updateGameStatusUI(data);
        });
    }

    setAdmin(isAdmin) {
        this.isAdmin = isAdmin;
    }

    setGameMode(isGameMode) {
        this.isGameMode = isGameMode;
    }

    emitWithResponse(event, data) {
        return new Promise((resolve, reject) => {
            this.emit(event, data, (response) => {
                if (response && response.status === 'ok') {
                    resolve(response);
                } else {
                    const message = `Chyba při zpracování události: ${event}`;
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
     * @param key
     * @param value
     * @returns {Promise<unknown>}
     */
    async setKey(key, value) {
        await this.emitWithResponse('set_key', { key, value });
    }

    async setKeyBroadcast(key, value) {
        await this.emitWithResponse('set_key_broadcast', { key, value });
    }

    async getKey(key) {
        const response = await this.emitWithResponse('get_key', key);
        return response.data;
    }

    async existKey(key) {
        const response = await this.emitWithResponse('exist_key', key);
        return !!response.exists;
    }

    async deleteKey(key) {
        await this.emitWithResponse('delete_key', key);
    }

    addEventListenerKey(eventKey, callback) {
        this.socket.on(eventKey, (data) => {
            callback(data);
        });
    }

    async getAllDatabase() {
        const db = await this.emitWithResponse('get_all_db');
        return db.data || {};
    }

    async deleteAllDatabase() {
        await this.emitWithResponse('delete_all_db');
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
