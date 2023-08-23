const client = new SocketClient();

const numberInput = document.querySelector('#number');
const checkButton = document.querySelector('#check');
const addButton = document.querySelector('#add');
const resultDiv = document.querySelector('#result');

checkButton.addEventListener('click', async () => {
    let number = numberInput.value;
    // let numbersList = JSON.parse(sessionStorage.getItem('numbersList')) || [];
    let numbersList = await client.get('numbersList') || [];

    if(number.length != 4 || isNaN(number)) {
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

addButton.addEventListener('click', async () => {
    let number = numberInput.value;
    // let numbersList = JSON.parse(sessionStorage.getItem('numbersList')) || [];
    let numbersList = await client.get('numbersList') || [];


    // is it number?
    if (number.length == 4 && !isNaN(number)) {
        if (!numbersList.includes(number)) {
            numbersList.push(number);
        }
        // sessionStorage.setItem('numbersList', JSON.stringify(numbersList));
        client.set('numbersList', numbersList);
        resultDiv.innerHTML = '<span class="ok">Přidáno</span>';
    } else {
        resultDiv.innerHTML = '<span class="stop">Zadej čtyřmístné číslo</span>';
    }
    numberInput.value = "";
    setTimeout(() => { resultDiv.innerHTML = ''; }, 3000);
});