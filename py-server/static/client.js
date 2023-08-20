const client = new WSClient(`ws://${window.location.hostname}:8765`);

client.addEventListener("countdown", (count) => {
	document.getElementById("countdown").textContent = "Countdown: " + count + " seconds left";
});

function setValue() {
    let key = document.getElementById('setKey').value;
    let value = document.getElementById('setValue').value;
    client.setKeyValue(key, value);
}

async function getValue() {
    let key = document.getElementById('getKey').value;
    const resp = await client.getKeyValue(key);
	document.getElementById('response').innerHTML = resp;
}
