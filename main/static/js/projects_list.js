let direction = document.querySelector("#direction");

direction.onchange = (e) => {
    location.href = `/projects_list/by_direction/${e.target.value}/`;
}