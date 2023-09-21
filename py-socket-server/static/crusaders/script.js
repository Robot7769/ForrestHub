const client = new SocketClient();

const numberInput = document.querySelector('#number');
const checkButton = document.querySelector('#check');
const addButton = document.querySelector('#add');
const resultDiv = document.querySelector('#result');

async function checkNumber(number) {
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
}
checkButton.addEventListener('click', async () => {
    let number = numberInput.value;
    await checkNumber(number);
});

numberInput.addEventListener('keyup', async (event) => {
    if (event.key == "Backspace") {
        return;
    }

    // Check if the pressed key is NOT a number (0-9)
    if (!event.key.match(/[0-9]/)) {
        event.preventDefault();
        let number = numberInput.value;
        await checkNumber(number);
    }
});