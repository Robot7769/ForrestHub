class ForesterLib {
    constructor(url = `http://${window.location.hostname}:${window.location.port}`) {
        if (io === undefined) {
            throw new Error('Socket.io is not loaded.');
        }
        this.socket = io.connect(url);

        if (window.location.pathname === '/admin/') {
            console.log('Admin page')
            this.socket.on('connect_admin', () => {
                console.log('Connected to the server!');
                this.removeOverlay();
            });

            this.socket.on('disconnect_admin', () => {
                console.log('Disconnected from the server.');
                this.showOverlay('Byl jsi odpojen od serveru. <br/>Hra nejspíš skončila nebo nastala neočekávaná chyba. <br/><small>Spojení bude automaticky obnoveno.</small>', null);
            });
        } else {
            console.log('Game page')
            this.socket.on('connect', () => {
                console.log('Connected to the server!');
                this.removeOverlay();
            });

            this.socket.on('disconnect', () => {
                console.log('Disconnected from the server.');
                this.showOverlay('Byl jsi odpojen od serveru. <br/>Hra nejspíš skončila nebo nastala neočekávaná chyba. <br/><small>Spojení bude automaticky obnoveno.</small>', null);
            });

            // this.socket.on('admin_message', (message) => {
            //     this.showOverlay(message, 5000); // Show for 5 seconds
            // });
        }
        this.socket.on('admin_messages', (message) => {
            this.showOverlay(message, 5000); // Show for 5 seconds
        });
    }

    set(key, value) {
        this.socket.emit('set', {key: key, value: value}, (response) => {
            if (response.status !== 'success') {
                console.error('Error setting value.');
                this.showOverlay('Nastala chyba při ukládání dat.', null);
            }
        });
    }

    getCallback(key, callback) {
        this.socket.emit('get', key, (response) => {
            callback(response.value);
        });
    }

    get(key) {
        return new Promise((resolve, reject) => {
            this.socket.emit('get', key, (response) => {
                if (response) {
                    resolve(response.value);
                } else {
                    reject('Error getting value');
                    this.showOverlay('Nastala chyba při načítání dat.', null);
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
        this.socket.emit('edit_data', {key: key, value: newValue}, (response) => {
            if (response.status !== 'success') {
                console.error('Error editing value.');
            }
        });
    }

    delete(key) {
        this.socket.emit('delete_data', key, (response) => {
            if (response.status !== 'success') {
                console.error('Error deleting value.');
            }
        });
    }

    showOverlay(text, duration = null) {
        // do not show messages with duration on admin page
        if (window.location.pathname === '/admin/' && duration) {
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
        overlay.style.backgroundColor = 'rgba(5,5,0,0.9)';
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
        }
    }

    removeOverlay() {
        let overlay = document.getElementById('overlay');
        if (overlay) {
            document.body.removeChild(overlay);
        }
    }

}
