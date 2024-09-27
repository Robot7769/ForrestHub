// forrestHubLib = window.forrestHubLib || new ForrestHubLib();
//
// document.addEventListener('DOMContentLoaded', function () {
//     const counterElement = document.getElementById('counter');
//     const incrementButton = document.getElementById('incrementButton');
//
//     // Načti počáteční hodnotu počítadla
//     forrestHubLib.getKey('my_number').then((value) => {
//         counterElement.innerText = value || 0;
//     }).catch((err) => {
//         console.error('Chyba při načítání počítadla:', err);
//     });
//
//     // Zvyšení počítadla po kliknutí
//     incrementButton.addEventListener('click', () => {
//         let currentValue = parseInt(counterElement.innerText, 10);
//         let newValue = currentValue + 1;
//
//         forrestHubLib.setKeyBroadcast('my_number', newValue).then((response) => {
//             counterElement.innerText = newValue;
//         }).catch((err) => {
//             console.error('Chyba při ukládání počítadla:', err);
//         });
//     });
//
//     // Automatické načítání změn v hodnotě počítadla
//     forrestHubLib.addEventListenerKey('my_number', (data) => {
//         counterElement.innerText = data || 0;
//     });
// });