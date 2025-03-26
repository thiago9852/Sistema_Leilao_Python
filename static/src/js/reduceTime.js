document.addEventListener('DOMContentLoaded', function() {
        /*  */
    // Decrementa o tempo do leilão

    var countDownDate = new Date("mar 30, 2025 15:17:25").getTime();

    var x = setInterval(function() {

    var now = new Date().getTime();

    var distance = countDownDate - now;

    var days = Math.floor(distance / (1000 * 60 * 60 * 24));
    var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
    var seconds = Math.floor((distance % (1000 * 60)) / 1000);

    var timers = document.querySelectorAll('.countdownTimer');

    timers.forEach(function(timer) {
        timer.innerHTML = days + "d " + hours + "h " + minutes + "m " + seconds + "s ";
    });

    if (distance < 0) {
        clearInterval(x);
        timers.forEach(function(timer) {
            timer.innerHTML = "Expirado";
        });
    }
    }, 1000);

});