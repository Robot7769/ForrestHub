const foresterLib = new ForrestHubLib();

document.addEventListener('DOMContentLoaded', function () {
    const counterElement = document.getElementById('counter');
    const decrementButton = document.getElementById('decrementButton');

    // Načti počáteční hodnotu počítadla
    foresterLib.getKey('my_number').then((value) => {
        counterElement.innerText = value || 0;
    }).catch((err) => {
        console.error('Chyba při načítání počítadla:', err);
    });

    // Zvyšení počítadla po kliknutí
    decrementButton.addEventListener('click', () => {
        let currentValue = parseInt(counterElement.innerText, 10);
        let newValue = currentValue - 1;

        foresterLib.setKeyBroadcast('my_number', newValue).then((response) => {
            counterElement.innerText = newValue;
        }).catch((err) => {
            console.error('Chyba při ukládání počítadla:', err);
        });
    });

    // Automatické načítání změn v hodnotě počítadla
    foresterLib.addEventListenerKey('my_number', (data) => {
        counterElement.innerText = data || 0;
    });
});