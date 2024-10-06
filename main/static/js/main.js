function set_borders(node_list) {
    for (var i = 0; i < node_list.length; i++) {
        if (i != node_list.length - 1) {
            node_list[i].classList.add("border-bottom");
        }
    }
}
try{
    let schedules = document.querySelectorAll("#quenes .my-card");
    set_borders(schedules);
} catch {}

try{
    let projects = document.querySelectorAll("#projects .my-card");
    let juries = document.querySelectorAll("#juries .my-card");
    set_borders(projects);
    set_borders(juries);
} catch {}

