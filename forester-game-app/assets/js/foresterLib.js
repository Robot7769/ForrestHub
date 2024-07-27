class ForesterLib {
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

        this.socket.on('connect', () => {
            console.log('Connected to the server!');
            this.socket.emit('get_game_status');
            this.removeOverlay();
        });

        this.socket.on('disconnect', () => {
            console.log('Disconnected from the server.');
            this.showOverlay('Byl jsi odpojen od serveru. <br/>Hra nejspíš skončila nebo nastala neočekávaná chyba.', null, "danger", true);
        });

        this.socket.on('admin_messages', (message) => {
            this.showOverlay(message, 5000, 'warning'); // Show for 5 seconds
        });

        this.socket.on('game_status', (status) => {
            if (status === this.RUNNING) {
                this.removeOverlay();
                if (this.isGameMode) {
                    // this.showOverlay('Hra spuštěna', 500, 'success');
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


        this.addEventListener("game_status", (data) => {
            if (data === this.RUNNING) {
                document.querySelectorAll(".game_status").forEach((element) => {
                    element.innerText = "Běží";
                });
            } else if (data === this.PAUSED) {
                document.querySelectorAll(".game_status").forEach((element) => {
                    element.innerText = "Pozastavena";
                });
            } else if (data === this.STOPPED) {
                document.querySelectorAll(".game_status").forEach((element) => {
                    element.innerText = "Ukončena";
                });
            } else {
                document.querySelectorAll(".game_status").forEach((element) => {
                    element.innerText = "?";
                });
            }
        });

    }

    setAdmin(isAdmin) {
        this.isAdmin = isAdmin;
    }

    setGameMode(isGameMode) {
        this.isGameMode = isGameMode;
    }

    set(key, value) {
        return new Promise((resolve, reject) => {
            this.socket.emit('set', {key: key, value: value}, (response) => {
                if (response.status === 'success') {
                    resolve(response);
                } else {
                    console.error('Error setting value.');
                    this.showOverlay('Nastala chyba při ukládání dat.', null);
                    reject(new Error('Error setting value'));
                }
            });
        });
    }

    get(key) {
        return new Promise((resolve, reject) => {
            this.socket.emit('get', key, (response) => {
                if (response) {
                    resolve(response.value);
                } else {
                    console.error('Error getting value');
                    this.showOverlay('Nastala chyba při načítání dat.', null);
                    reject(new Error('Error getting value'));
                }
            });
        });
    }

    getAll() {
        return new Promise((resolve, reject) => {
            this.socket.emit('get_all', (response) => {
                if (response) {
                    resolve(response);
                } else {
                    console.error('Error getting all data');
                    this.showOverlay('Nastala chyba při načítání dat.', null);
                    reject(new Error('Error getting all data'));
                }
            });
        });
    }

    addEventListener(eventKey, callback) {
        this.socket.on(eventKey, (data) => {
            callback(data);
        });
    }

    edit(key, newValue) {
        return new Promise((resolve, reject) => {
            this.socket.emit('edit_data', {key: key, value: newValue}, (response) => {
                if (response.status === 'success') {
                    resolve(response);
                } else {
                    console.error('Error editing value.');
                    reject(new Error('Error editing value'));
                }
            });
        });
    }

    delete(key) {
        return new Promise((resolve, reject) => {
            this.socket.emit('delete_data', key, (response) => {
                if (response.status === 'success') {
                    resolve(response);
                } else {
                    console.error('Error deleting value.');
                    reject(new Error('Error deleting value'));
                }
            });
        });
    }

    showAlert(type, message, duration = 5000) {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
        // keep alert on top of the page - allow scrolling
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
        // do not show messages with duration on admin page
        if (this.isAdmin && !forceShow) {
            this.showAlert('info', `Zpráva: ${text}`, 5000);
            return;
        }
        // Create overlay elements
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

        // if (!duration && !this.isGameMode) {
        //     duration = 5000;
        // }

        // Countdown logic
        if (duration) {
            let remainingTime = duration / 1000; // convert to seconds
            countdown.innerText = `Zbývá ${remainingTime}s`;

            let countdownInterval = setInterval(() => {
                remainingTime -= 1;
                countdown.innerText = `Zbývá ${remainingTime}s`;

                if (remainingTime <= 0) {
                    clearInterval(countdownInterval);
                    this.removeOverlay();
                }
            }, 1000);
        } else {
            //     slowly fade in and out in infinit loop
            let opacity = 1;
            let fadeIn = false;
            let fadeInterval = setInterval(() => {
                if (fadeIn) {
                    opacity += 0.0008;
                    if (opacity >= 0.96) {
                        fadeIn = false;
                    }
                } else {
                    opacity -= 0.0008;
                    if (opacity <= 0.8) {
                        fadeIn = true;
                    }
                }
                overlay.style.backgroundColor = `rgba(5,5,0,${opacity})`;
            }, 20);
        }
    }

    removeOverlay() {
        let overlay = document.getElementById('overlay');
        if (overlay) {
            document.body.removeChild(overlay);
        }
    }

}

// let foresterLib = new ForesterLib();
