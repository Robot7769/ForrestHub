class WSClient {
    constructor(url) {
        this.socket = new WebSocket(url);
        this.setupListeners();
        this.eventListeners = {};
    }

    setupListeners() {
        this.socket.onopen = () => console.log('WebSocket is connected.');
        this.socket.onerror = error => console.error(`WebSocket Error: ${error}`);
        this.socket.onmessage = event => {
            const responseData = JSON.parse(event.data);
            console.log(responseData);
            if (responseData.key) {
                this.triggerEventListeners(responseData.key, responseData.payload);
            }
        };
        this.socket.onclose = event => {
            if (event.wasClean) {
                console.log(`Connection closed cleanly, code=${event.code}, reason=${event.reason}`);
            } else {
                console.error('Connection died');
            }
        };
    }

    addEventListener(key, callback) {
        if(!this.eventListeners[key]) {
            this.eventListeners[key] = [];
        }
        this.eventListeners[key].push(callback);
    }

    triggerEventListeners(key, data) {
        if(this.eventListeners[key]) {
            for(let callback of this.eventListeners[key]) {
                callback(data);
            }
        }
    }

    send(action, payload) {
        return new Promise((resolve, reject) => {
            const message = {
                action: action,
                payload: payload
            };
            this.socket.send(JSON.stringify(message));

            this.socket.onmessage = event => {
                const responseData = JSON.parse(event.data);
                if (responseData.status === 'success') {
                    resolve(responseData.payload);
                } else {
                    reject(responseData.message);
                }
            };
        });
    }

    async getKeyValue(key) {
        return await this.send("get", { key: key });
    }

    setKeyValue(key, value) {
        this.send("set", { key: key, value: value });
    }

    close() {
        this.socket.close();
    }
}
