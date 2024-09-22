const image = document.getElementById('forrestHub');

let clickCount = 0;
image.addEventListener('click', function () {
    clickCount++;
    if (clickCount === 10) {
        window.location.href = '/';
    }
});

// work also on touch devices
image.addEventListener('touchstart', function () {
    clickCount++;
    if (clickCount === 10) {
        window.location.href = '/';
    }
});
