const foresterLib = new ForesterLib();

const numberInput = document.querySelector('#number');
const checkButton = document.querySelector('#check');
const resultDiv = document.querySelector('#result');

let timeout = null;

async function checkNumber(number) {
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

    if (numbersList.includes(number)) {
        resultDiv.innerText = 'Stůj';
        resultDiv.classList.add('alert', 'alert-danger');
    } else {
        resultDiv.innerText = 'Můžeš dál';
        resultDiv.classList.add('alert', 'alert-success');
    }
    numberInput.value = "";
    timeout && clearTimeout(timeout);
    timeout = setTimeout(() => {
        resultDiv.innerText = '';
        resultDiv.classList.remove('alert', 'alert-danger', 'alert-success');
    }, 3000);
}

checkButton.addEventListener('click', async () => {
    let number = numberInput.value;
    await checkNumber(number);
});

numberInput.addEventListener('keyup', async (event) => {
    if (event.key === "Backspace") {
        return;
    }

    // Check if the pressed key is NOT a number (0-9)
    if (!event.key.match(/[0-9]/)) {
        event.preventDefault();
        let number = numberInput.value;
        await checkNumber(number);
    }
});
