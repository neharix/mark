function set_borders(node_list) {
    for (var i = 0; i < node_list.length; i++) {
        if (i != node_list.length - 1) {
            node_list[i].classList.add("border-bottom");
        }
    }
}

let histories = document.querySelectorAll("#history .my-card");

set_borders(histories);