let mark_inputs = document.querySelectorAll("input[maxvalue]");
console.log(mark_inputs);

function normalize_value (e) {
    console.log(e.target.value);
    if (Number(e.target.value) > Number(e.target.getAttribute("maxvalue"))) {
        e.target.value = e.target.getAttribute("maxvalue");
    }
    else if (Number(e.target.value) < 0) {
        e.target.value = 0;
    }
}

mark_inputs.forEach(mark_input => {
    mark_input.onkeyup = normalize_value;
    mark_input.onkeydown = normalize_value;
})