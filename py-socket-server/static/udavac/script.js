const client = new SocketClient();

const numberInput = document.querySelector('#number');
const udavacButton = document.querySelector('#udavac');
const resultDiv = document.querySelector('#result');

async function addNumber(number) {
    // let numbersList = JSON.parse(sessionStorage.getItem('numbersList')) || [];
    let numbersList = await client.get('numbersList') || [];


    // is it number?
    if (number.length == 4 && !isNaN(number)) {
        if (!numbersList.includes(number)) {
            numbersList.push(number);
        }
        // sessionStorage.setItem('numbersList', JSON.stringify(numbersList));
        client.set('numbersList', numbersList);
        resultDiv.innerHTML = '<span class="ok">Udáno</span>';
    } else {
        resultDiv.innerHTML = '<span class="stop">Zadej čtyřmístné číslo</span>';
    }
    numberInput.value = "";
    setTimeout(() => { resultDiv.innerHTML = ''; }, 3000);
}

udavacButton.addEventListener('click', async () => {
    let number = numberInput.value;
    await addNumber(number);
});

numberInput.addEventListener('keyup', async (event) => {
    // if backspace is pressed
    if (event.key == "Backspace") {
        return;
    }

    // Check if the pressed key is NOT a number (0-9)
    if (!event.key.match(/[0-9]/)) {
        event.preventDefault();
        let number = numberInput.value;
        await addNumber(number);
    }
});