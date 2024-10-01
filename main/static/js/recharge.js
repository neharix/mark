let count = document.querySelector("#count");
let accept_btn = document.querySelector("#accept-btn");
let cards = document.querySelectorAll("#dialog .my-card");
let card_input = document.querySelector("#card");

$(document).ready(function() {
    $('#card').keyup(function(e) {
        e.preventDefault();
        var id = $(this).attr('data');
        var backHeight = $(document).height();
        var backWidth = $(window).width();
        $('#back').css({'width':backWidth,'height':backHeight});
        $('#back').fadeIn(300);
        $('#back').fadeTo(300,0.8);
        var winH = $(window).height();
        var winW = $(window).width();
        $(id).css('top',  winH/2-$(id).height()/2);
        $(id).css('left', winW/2-$(id).width()/2);
        $(id).fadeIn(300);
        $(".window").show();
    });
    $('#card').keydown(function(e) {
        e.preventDefault();
        var id = $(this).attr('data');
        var backHeight = $(document).height();
        var backWidth = $(window).width();
        $('#back').css({'width':backWidth,'height':backHeight});
        $('#back').fadeIn(300);
        $('#back').fadeTo(300,0.8);
        var winH = $(window).height();
        var winW = $(window).width();
        $(id).css('top',  winH/2-$(id).height()/2);
        $(id).css('left', winW/2-$(id).width()/2);
        $(id).fadeIn(300);
        $(".window").show();
    });
    $('#card').click(function(e) {
        e.preventDefault();
        var id = $(this).attr('data');
        var backHeight = $(document).height();
        var backWidth = $(window).width();
        $('#back').css({'width':backWidth,'height':backHeight});
        $('#back').fadeIn(300);
        $('#back').fadeTo(300,0.8);
        var winH = $(window).height();
        var winW = $(window).width();
        $(id).css('top',  winH/2-$(id).height()/2);
        $(id).css('left', winW/2-$(id).width()/2);
        $(id).fadeIn(300);
        $(".window").show();
    });
    $('.window .close').click(function (e) {
        e.preventDefault();
        $('#back, .window').hide();
    });
    $('#back').click(function () {
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

set_borders(cards);

function select_card(card_index) {
    card_input.value = cards[card_index].children[0].children[0].children[1].children[1].children[0].innerHTML + " " + cards[card_index].children[0].children[0].children[1].children[1].children[1].innerHTML
    card_input.setAttribute("data", cards[card_index].getAttribute("data"));
    $('#back, .window').hide();
}

function update_accept_btn_text() {
    if (count.value == "") {
        accept_btn.innerHTML = `JEMI TÖLEG: 0 TMT`;
    } else {
        accept_btn.innerHTML = `JEMI TÖLEG: ${count.value} TMT`;
    }
}

count.onkeyup = update_accept_btn_text;
count.onkeydown = update_accept_btn_text;

accept_btn.onclick = () => {
    location.href = `/recharge/card/${card_input.getAttribute('data')}/value/${count.value || 0}/`;
}