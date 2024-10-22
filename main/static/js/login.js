document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".inp").forEach(input => {
        input.addEventListener('input', () => {
            if ((document.querySelector('.usrnm').value.length == 0) || (document.querySelector('.pswd').value.length == 0)) {
                document.querySelector('#accept-btn').disabled = true;
            }
            else {
                document.querySelector('#accept-btn').disabled = false;
            }
        });
        input.addEventListener('keyup', () => {
            if ((document.querySelector('.usrnm').value.length == 0) || (document.querySelector('.pswd').value.length == 0)) {
                document.querySelector('#accept-btn').disabled = true;
            }
            else {
                document.querySelector('#accept-btn').disabled = false;
            }
        });
        input.addEventListener('keydown', () => {
            if ((document.querySelector('.usrnm').value.length == 0) || (document.querySelector('.pswd').value.length == 0)) {
                document.querySelector('#accept-btn').disabled = true;
            }
            else {
                document.querySelector('#accept-btn').disabled = false;
            }
        });
    });
});
