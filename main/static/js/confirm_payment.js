let confirmation_code = JSON.parse(document.querySelector("#confirmation-code").textContent);
let history_pk = JSON.parse(document.querySelector("#history-pk").textContent);
let code = document.querySelector("#code");
let accept_btn = document.querySelector("#accept-btn");


function update_accept_btn_text() {
    if (Number(code.value) == confirmation_code) {
        accept_btn.classList.remove("disabled");
    } else {
        if (code.classList.contains("disabled") == false) {
            accept_btn.classList.add("disabled");
        }
    }
}

code.onkeyup = update_accept_btn_text;
code.onkeydown = update_accept_btn_text;

accept_btn.onclick = (e) => {
    location.href += `success/${history_pk}/`;
}