const client = new WSClient(`ws://${window.location.hostname}:8765`);

client.addEventListener("update_time", (count) => {
	document.getElementById("update_time").textContent = "Herní čas: " + count;
});


const numberInput = document.getElementById('number');
const checkButton = document.getElementById('check');
const addButton = document.getElementById('add');
const resultDiv = document.getElementById('result');

checkButton.onclick = (() => {
    let number = numberInput.value;
    let numbersList = client.getKeyValue('numbersList') || [];

    if(number.length != 5 || isNaN(number)) {
        resultDiv.innerHTML = '<span class="stop">Zadej čtyřmístné číslo</span>';
        numberInput.value = "";
        setTimeout(() => { resultDiv.innerHTML = ''; }, 3000);
        return;
    }

    if (numbersList.includes(number)) {
        resultDiv.innerHTML = '<span class="stop">Stůj</span>';
    } else {
        resultDiv.innerHTML = '<span class="ok">Můžeš dál</span>';
    }
    numberInput.value = "";
    setTimeout(() => { resultDiv.innerHTML = ''; }, 3000);
});

addButton.click(() => {
    let number = numberInput.value;
    let numbersList = client.getKeyValue('numbersList') || [];

    // is it number?
    if (number.length == 5 && !isNaN(number)) {
        numbersList.push(number);
        client.setKeyValue('numbersList', numbersList);
        resultDiv.innerHTML = '<span class="ok">Přidáno</span>';
    } else {
        resultDiv.innerHTML = '<span class="stop">Zadej čtyřmístné číslo</span>';
    }
    numberInput.value = "";
    setTimeout(() => { resultDiv.innerHTML = ''; }, 3000);
});