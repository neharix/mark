const s_table = document.querySelector('#schedule-table');
const schedule_pk = JSON.parse(document.getElementById('schedule-pk').textContent);

const s_draggables = document.querySelectorAll('tr[draggable="true"]');

s_draggables.forEach(draggable => {
    draggable.addEventListener('dragstart', () => {
    draggable.classList.add('dragging');
    });

    draggable.addEventListener('dragend', () => {
    draggable.classList.remove('dragging');
    });
});

s_table.addEventListener('dragover', (event) => {
    event.preventDefault();
    const afterElement = getDragAfterElement(table, event.clientY);
    const draggable = document.querySelector('.dragging');
    if (afterElement == null) {
    s_table.appendChild(draggable);
    } else {
    s_table.insertBefore(draggable, afterElement);
    }
    for (let i=0; i < s_table.children.length; i++) {
        s_table.children[i].children[1].innerHTML = i + 1;
        s_table.children[i].children[5].querySelector("button").setAttribute("onclick", `delete_schedule_row(${i})`);
    }
});

function getDragAfterElement(table, y) {
    const draggableElements = [...table.querySelectorAll('tr:not(.dragging)')];

    return draggableElements.reduce((closest, child) => {
    const box = child.getBoundingClientRect();
    const offset = y - box.top - box.height / 2;

    if (offset < 0 && closest === null) {
        return child;
    } else if (offset < 0) {
        return offset > closest.offset ? child : closest;
    } else {
        return closest;
    }
    }, null);
}

let projects = null;
let juries = null;

function success(data) {
    let projects_list = document.querySelector("#projects-list");
    projects_list.innerHTML = "";
    let pks = [];
    for (let i=0; i<data.length; i++){
        pks.push(data[i].pk);
    }
    let table = document.querySelector("#schedule-table");
    for (let i=0; i < table.children.length; i++) {
        if (pks.includes(Number(table.children[i].getAttribute("data")))) {
            data.splice(data.findIndex(project => project.pk == Number(table.children[i].getAttribute("data"))), 1);
        }
    }
    for (var i=0; i < data.length; i++) {
        let btn = document.createElement("button");
        btn.setAttribute('class', "btn-none my-card");
        btn.setAttribute("onclick", `select_project(${i})`);
        btn.innerHTML = `<div class="my-3 "><div class="d-flex align-items-center"><div style="margin-right: 1rem;"><div class="d-flex justify-content-center align-items-center ico" style=""><i class="bi bi-box"></i></div></div><div class="w-100"><div class="text-align-start">${ data[i].description }</div><div class="text-align-start">${data[i].full_name_of_manager}</div><div class="text-align-start">${data[i].agency}</div><div class="d-none">${data[i].pk}</div></div></div></div>`;
        projects_list.appendChild(btn);
    }

    projects = document.querySelectorAll("#projects-list .my-card");

    set_borders(projects);
}

function juries_success(data) {
    let juries_list = document.querySelector("#juries-list");
    juries_list.innerHTML = "";
    let pks = [];
    for (let i=0; i<data.length; i++){
        pks.push(data[i].pk);
    }
    let table = document.querySelector("#juries-table");
    for (let i=0; i < table.children.length; i++) {
        if (pks.includes(Number(table.children[i].getAttribute("data")))) {
            data.splice(data.findIndex(jury => jury.pk == Number(table.children[i].getAttribute("data"))), 1);
        }
    }
    for (var i=0; i < data.length; i++) {
        let btn = document.createElement("button");
        btn.setAttribute('class', "btn-none my-card");
        btn.setAttribute("onclick", `select_jury(${i})`);
        btn.innerHTML = `<div class="my-3 "><div class="d-flex align-items-center"><div style="margin-right: 1rem;"><div class="d-flex justify-content-center align-items-center ico" style=""><i class="bi bi-person"></i></div></div><div class="w-100"><div class="text-align-start">${ data[i].last_name } ${ data[i].first_name }</div><div class="d-none">${data[i].id}</div></div></div></div>`;
        juries_list.appendChild(btn);
    }

    juries = document.querySelectorAll("#juries-list .my-card");

    set_borders(juries);
}


$(document).ready(function() {
    $('#add-project-btn').click(function(e) {
        e.preventDefault();
        $.ajax({
            url: "/api/v1/unrated_projects/",
            type: 'GET',
            dataType: 'json',
            success: success,
        });
        var backHeight = $(document).height();
        var backWidth = $(window).width();
        $('#back').css({'width':backWidth,'height':backHeight});
        $('#back').fadeIn(300);
        $('#back').fadeTo(300,0.8);
        var winH = $(window).height();
        var winW = $(window).width();
        $("#dialog").css('top',  winH/2.5-$("#dialog").height()/2);
        $("#dialog").css('left', winW/2-$("#dialog").width()/2);
        $("#dialog").fadeIn(300);
        $("#dialog").show();
    });
    $('#add-jury-btn').click(function(e) {
        e.preventDefault();
        $.ajax({
            url: "/api/v1/juries/",
            type: 'GET',
            dataType: 'json',
            success: juries_success,
        });
        var backHeight = $(document).height();
        var backWidth = $(window).width();
        $('#back').css({'width':backWidth,'height':backHeight});
        $('#back').fadeIn(300);
        $('#back').fadeTo(300,0.8);
        var winH = $(window).height();
        var winW = $(window).width();
        $("#jury-dialog").css('top',  winH/2.5-$("#dialog").height()/2);
        $("#jury-dialog").css('left', winW/2-$("#dialog").width()/2);
        $("#jury-dialog").fadeIn(300);
        $("#jury-dialog").show();
    });

    $('.window .close-btn').click(function (e) {
        e.preventDefault();
        document.querySelector("#projects-list").innerHTML = "";
        $('#back, .window').hide();
    });
    $('#back').click(function () {
        document.querySelector("#projects-list").innerHTML = "";
        $(this).hide();
        $('.window').hide();
    });
});

function set_borders(node_list) {
    for (var i = 0; i < node_list.length; i++) {
        if (i != node_list.length - 1) {
            node_list[i].classList.add("border-bottom");
        }
    }
}


function select_jury(jury_index) {
    let table_row = document.createElement("tr");

    table_row.setAttribute("data", juries[jury_index].children[0].children[0].children[1].children[1].innerHTML);
    table_row.innerHTML = `
        <td></td>
        <td class="text-center">${juries_table.children.length + 1}</td>
        <td>${juries[jury_index].children[0].children[0].children[1].children[0].innerHTML}</td>
        <td><button onclick="delete_jury_row(${juries_table.children.length})" class="btn btn-danger"><i class="bi bi-trash"></i></button></td>`;
    juries_table.appendChild(table_row);
    $('#back, .window').hide();
}


function select_project(project_index) {
    let table_row = document.createElement("tr");

    table_row.setAttribute("data", projects[project_index].children[0].children[0].children[1].children[3].innerHTML);
    table_row.innerHTML = `
        <td class="text-center drag-handle">☰</td>
        <td class="text-center">${table.children.length + 1}</td>
        <td>${projects[project_index].children[0].children[0].children[1].children[0].innerHTML}</td>
        <td>${projects[project_index].children[0].children[0].children[1].children[1].innerHTML}</td>
        <td>${projects[project_index].children[0].children[0].children[1].children[2].innerHTML}</td>
        <td><button onclick="delete_schedule_row(${table.children.length})" class="btn btn-danger"><i class="bi bi-trash"></i></button></td>`;

    table_row.setAttribute("draggable", "true");
    table_row.addEventListener('dragstart', () => {
        table_row.classList.add('dragging');
    });
    
    table_row.addEventListener('dragend', () => {
        table_row.classList.remove('dragging');
    });
    table.appendChild(table_row);
    $('#back, .window').hide();
}

const table = document.querySelector('#schedule-table');
const juries_table = document.querySelector('#juries-table');
const draggables = document.querySelectorAll('tr[draggable="true"]');

draggables.forEach(draggable => {
    draggable.addEventListener('dragstart', () => {
        draggable.classList.add('dragging');
    });

    draggable.addEventListener('dragend', () => {
        draggable.classList.remove('dragging');
    });
});

table.addEventListener('dragover', (event) => {
    event.preventDefault();
    const afterElement = getDragAfterElement(table, event.clientY);
    const draggable = document.querySelector('.dragging');
    if (afterElement == null) {
    table.appendChild(draggable);
    } else {
    table.insertBefore(draggable, afterElement);
    }

    for (let i=0; i < table.children.length; i++) {
        table.children[i].children[1].innerHTML = i + 1;
        table.children[i].children[5].querySelector("button").setAttribute("onclick", `delete_schedule_row(${i})`);
    }
});

function getDragAfterElement(table, y) {
    const draggableElements = [...table.querySelectorAll('tr:not(.dragging)')];

    return draggableElements.reduce((closest, child) => {
    const box = child.getBoundingClientRect();
    const offset = y - box.top - box.height / 2;

    if (offset < 0 && closest === null) {
        return child;
    } else if (offset < 0) {
        return offset > closest.offset ? child : closest;
    } else {
        return closest;
    }
    }, null);
}

function delete_schedule_row(row_index) {
    let table = document.querySelector("#schedule-table");
    let project_id = Number(table.children[row_index].getAttribute("data"));
    $.post("/api/v1/delete_project_from_schedule/", {schedule_pk: schedule_pk, project_id: project_id}, (data) => 
        {
            console.log(data);
        }
    );
    $("#schedule-table tr").eq(row_index).remove();
    for (let i=0; i < table.children.length; i++) {
        
        table.children[i].children[1].innerHTML = i + 1;
        table.children[i].children[5].querySelector("button").setAttribute("onclick", `delete_schedule_row(${i})`);
    }
}
function delete_jury_row(row_index) {
    let table = document.querySelector("#juries-table");
    let jury_id = Number(table.children[row_index].getAttribute("data"));
    $.post("/api/v1/delete_jury_from_schedule/", {schedule_pk: schedule_pk, jury_id: jury_id}, (data) => 
        {
            console.log(data);
        }
        
    );
    $("#juries-table tr").eq(row_index).remove();
    for (let i=0; i < table.children.length; i++) {
        table.children[i].children[1].innerHTML = i + 1;
        table.children[i].children[3].querySelector("button").setAttribute("onclick", `delete_jury_row(${i})`);
    }
}


let accept_btn = document.querySelector("#accept-btn");

function save_schedule(){
    let table = document.querySelector("#schedule-table");
    let pks = [];
    for (let i=0; i < table.children.length; i++) {
        pks.push(Number(table.children[i].getAttribute("data")));
    }
    let juries_table = document.querySelector("#juries-table");
    let juries_ids = [];
    for (let i=0; i < juries_table.children.length; i++) {
        juries_ids.push(Number(juries_table.children[i].getAttribute("data")));
    }
    $.post("/api/v1/edit_schedule/", {schedule_pk: schedule_pk, date: selected_date, schedule: JSON.stringify(pks), juries: JSON.stringify(juries_ids)}, (data) => 
        {
            console.log(data);
            let alert_box = document.querySelector("#alert-box");
            if (data.detail == "fail") {
                alert_box.classList.remove("d-none");
                alert_box.classList.add("d-flex");
                alert_box.querySelector(".mes").innerHTML = "Reje ýatda saklanylmady!"
            }
            else if (data.detail == "you need to be a moderator") {
                alert_box.classList.remove("d-none");
                alert_box.classList.add("d-flex");
                alert_box.querySelector(".mes").innerHTML = "Reje goşmak üçin moderator bolmak gerek!"
            }
            else if (data.detail == "schedule was made on the given date") {
                alert_box.classList.remove("d-none");
                alert_box.classList.add("d-flex");
                alert_box.querySelector(".mes").innerHTML = "Berlen senede eýýäm reje bellenildi!"
            }
            else {
                location.href = "/schedules/";
            }
        }
    );

}

accept_btn.onclick = save_schedule;