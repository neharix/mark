function success(data) {
    let projects_list = document.querySelector("#projects-list");
    for (var i=0; i < data.length; i++) {
        let btn = document.createElement("button");
        btn.setAttribute('class', "btn-none my-card")
        btn.setAttribute("onclick", `console.log(${data[i].pk})`);
        btn.innerHTML = `<div class="my-3 "><div class="d-flex align-items-center"><div style="margin-right: 1rem;"><div class="d-flex justify-content-center align-items-center ico" style=""><i class="bi bi-credit-card"></i></div></div><div class="w-100"><div class="text-align-start">${ data[i].description }</div><div class="text-align-start">${data[i].full_name_of_manager}</div><div class="text-align-start">${data[i].agency}</div></div></div></div>`;
        projects_list.appendChild(btn);
    }

    let projects = document.querySelectorAll("#projects-list .my-card");

    set_borders(projects);
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
        $("#dialog").css('top',  winH/3-$("#dialog").height()/2);
        $("#dialog").css('left', winW/2-$("#dialog").width()/2);
        $("#dialog").fadeIn(300);
        $(".window").show();
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
