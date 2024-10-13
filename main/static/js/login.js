document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".inp").forEach(input => {
        if (input.id != "email"){
            input.addEventListener('input', () => {
                if ((document.querySelector('.usrnm').value.length == 0) || (document.querySelector('.email').value.length == 0) || (document.querySelector('.pswd').value.length == 0)) {
                    document.querySelector('#accept-btn').disabled = true;
                }
                else {
                    document.querySelector('#accept-btn').disabled = false;
                }
            });
            input.addEventListener('keyup', () => {
                if ((document.querySelector('.usrnm').value.length == 0) || (document.querySelector('.email').value.length == 0) || (document.querySelector('.pswd').value.length == 0)) {
                    document.querySelector('#accept-btn').disabled = true;
                }
                else {
                    document.querySelector('#accept-btn').disabled = false;
                }
            });
            input.addEventListener('keydown', () => {
                if ((document.querySelector('.usrnm').value.length == 0) || (document.querySelector('.email').value.length == 0) || (document.querySelector('.pswd').value.length == 0)) {
                    document.querySelector('#accept-btn').disabled = true;
                }
                else {
                    document.querySelector('#accept-btn').disabled = false;
                }
            });
        } else {
            console.log("its me");
            input.addEventListener('input', () => {
                if ((document.querySelector('.usrnm').value.length == 0) || (document.querySelector('.email').value.length == 0) || (document.querySelector('.pswd').value.length == 0)) {
                    document.querySelector('#accept-btn').disabled = true;
                }
                else {
                    document.querySelector('#accept-btn').disabled = false;
                }
                if (document.querySelector('.email').value.length == 0) {
                    document.querySelector('#get-verification-code').disabled = true;
                }
                else{
                    document.querySelector('#get-verification-code').disabled = false;
                }
            });
            input.addEventListener('keyup', () => {
                if ((document.querySelector('.usrnm').value.length == 0) || (document.querySelector('.email').value.length == 0) || (document.querySelector('.pswd').value.length == 0)) {
                    document.querySelector('#accept-btn').disabled = true;
                }
                else {
                    document.querySelector('#accept-btn').disabled = false;
                }
                if (document.querySelector('.email').value.length == 0) {
                    document.querySelector('#get-verification-code').disabled = true;
                }
                else{
                    document.querySelector('#get-verification-code').disabled = false;
                }
            });
            input.addEventListener('keydown', () => {
                if ((document.querySelector('.usrnm').value.length == 0) || (document.querySelector('.email').value.length == 0) || (document.querySelector('.pswd').value.length == 0)) {
                    document.querySelector('#accept-btn').disabled = true;
                }
                else {
                    document.querySelector('#accept-btn').disabled = false;
                }
                if (document.querySelector('.email').value.length == 0) {
                    document.querySelector('#get-verification-code').disabled = true;
                }
                else{
                    document.querySelector('#get-verification-code').disabled = false;
                }
            });
        }
    });
});

document.querySelector("#get-verification-code").onclick = (e) => {
    document.querySelector("#otp-field").classList.remove("d-none");
    document.querySelector("#get-verification-code").parentElement.classList.add("d-none");
    $.post("/api/v1/otp/", {username: document.querySelector("#username").value, email: document.querySelector("#email").value}, (data) => 
        {
            console.log(data);
            
        }
    );
};