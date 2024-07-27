const foresterLib = new ForesterLib(true);
foresterLib.isEnabled = true;

const numberInput = document.querySelector('#number');
const udavacButton = document.querySelector('#udavac');
const resultDiv = document.querySelector('#result');

let timeout = null;
async function addNumber(number) {
    let numbersList = await foresterLib.get('numbersList') || [];

    if (number.length !== 4 || isNaN(number)) {
        resultDiv.innerText = 'Zadej čtyřmístné číslo';
        resultDiv.classList.add('alert', 'alert-danger');
        numberInput.value = "";

        timeout && clearTimeout(timeout);
        timeout = setTimeout(() => {
            resultDiv.innerText = '';
            resultDiv.classList.remove('alert', 'alert-danger');
        }, 3000);
        return;
    }


    if (!numbersList.includes(number)) {
        numbersList.push(number);
    }
    foresterLib.set('numbersList', numbersList);
    resultDiv.innerText = 'Číslo bylo přidáno';
    resultDiv.classList.add('alert', 'alert-success');

    numberInput.value = "";
    timeout && clearTimeout(timeout);
    timeout = setTimeout(() => {
        resultDiv.innerText = '';
        resultDiv.classList.remove('alert', 'alert-success');
    }, 3000);
}

udavacButton.addEventListener('click', async () => {
    let number = numberInput.value;
    await addNumber(number);
});

numberInput.addEventListener('keyup', async (event) => {
    // if backspace is pressed
    if (event.key === "Backspace") {
        return;
    }

    // Check if the pressed key is NOT a number (0-9)
    if (!event.key.match(/[0-9]/)) {
        event.preventDefault();
        let number = numberInput.value;
        await addNumber(number);
    }
});