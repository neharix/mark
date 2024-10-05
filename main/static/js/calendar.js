var month = [
	"Ýanwar",
	"Fewral",
	"Mart",
	"Aprel",
	"Maý",
	"Iýun",
	"Iýul",
	"Awgust",
	"Sentýabr",
	"Oktýabr",
	"Noýabr",
	"Dekabr"
];
var weekday = [
	"Sunday",
	"Monday",
	"Tuesday",
	"Wednesday",
	"Thursday",
	"Friday",
	"Saturday"
];
var weekdayShort = [
	"sun",
	"mon",
	"tue",
	"wed",
	"thu",
	"fri",
	"sat"
];
var monthDirection = 0;
 
var today = new Date();
var dd = String(today.getDate()).padStart(2, '0');
var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
var yyyy = today.getFullYear();
var selected_date =  dd + "/" + mm +'/' + yyyy;

function getNextMonth() {
	monthDirection++;
	var current;
	var now = new Date();
	if (now.getMonth() == 11) {
		current = new Date(now.getFullYear() + monthDirection, 0, 1);
	} else {
		current = new Date(now.getFullYear(), now.getMonth() + monthDirection, 1);
	}
	initCalender(getMonth(current));
}
 
function getPrevMonth() {
	monthDirection--;
	var current;
	var now = new Date();
	if (now.getMonth() == 11) {
		current = new Date(now.getFullYear() + monthDirection, 0, 1);
	} else {
		current = new Date(now.getFullYear(), now.getMonth() + monthDirection, 1);
	}
	initCalender(getMonth(current));
}
Date.prototype.isSameDateAs = function (pDate) {
	return (
		this.getFullYear() === pDate.getFullYear() &&
		this.getMonth() === pDate.getMonth() &&
		this.getDate() === pDate.getDate()
	);
};
 
function getMonth(currentDay) {
	var now = new Date();
	var currentMonth = month[currentDay.getMonth()];
	var monthArr = [];
	for (i = 1 - currentDay.getDate(); i < 31; i++) {
		var tomorrow = new Date(currentDay);
		tomorrow.setDate(currentDay.getDate() + i);
		if (currentMonth !== month[tomorrow.getMonth()]) {
			break;
		} else {
			monthArr.push({
				date: {
					weekday: weekday[tomorrow.getDay()],
					weekday_short: weekdayShort[tomorrow.getDay()],
					day: tomorrow.getDate(),
					month: month[tomorrow.getMonth()],
					year: tomorrow.getFullYear(),
					current_day: now.isSameDateAs(tomorrow) ? true : false,
					date_info: tomorrow
				}
			});
		}
	}
	return monthArr;
}
 
function clearCalender() {
	$("#calendar tbody tr").each(function () {
		$(this).find("td").removeClass("active selectable currentDay between hover").html("");
	});
	$("#calendar tr td").each(function () {
		$(this).unbind('mouseenter').unbind('mouseleave');
	});
	$("#calendar tr td").each(function () {
		$(this).unbind('click');
	});
	clickCounter = 0;
}
 
function initCalender(monthData) {
	var row = 0;
	var classToAdd = "";
	var currentDay = "";
	var today = new Date();
 
	clearCalender();
	$.each(monthData,
		function (i, value) {
			var weekday = value.date.weekday_short;
			var day = value.date.day;
			var column = 0;
			var index = i + 1;
 
			$(".sideb .header .month").html(value.date.month);
			$(".sideb .header .year").html(value.date.year);
			if (value.date.current_day) {
				currentDay = "currentDay";
        classToAdd = "selectable";
				$(".right-wrapper .header span").html(value.date.weekday);
				$(".right-wrapper .day").html(value.date.day);
				$(".right-wrapper .month").html(value.date.month);
			}
			if (today.getTime() < value.date.date_info.getTime()) {
				classToAdd = "selectable";
 
			}
			$("tr.weedays th").each(function () {
				var row = $(this);
				if (row.data("weekday") === weekday) {
					column = row.data("column");
					return;
				}
			});
			$($($($("tr.days").get(row)).find("td").get(column)).addClass(classToAdd + " " + currentDay).html(day));
			currentDay = "";
			if (column == 6) {
				row++;
			}
		});
	$("td.selectable").click(function () {
		dateClickHandler($(this));
		selected_date = document.querySelector(".active").innerHTML + `/${month.indexOf(document.querySelector(".month").innerHTML) + 1}/` + document.querySelector(".year").innerHTML;
		console.log(selected_date);
	});
}
initCalender(getMonth(new Date()));
 
var clickCounter = 0;

function dateClickHandler(elem) {
 
	var day1 = parseInt($(elem).html());
	if (clickCounter === 0) {
		$("td.selectable").each(function () {
			$(this).removeClass("active between hover");
		});
	}
	clickCounter++;
	if (clickCounter === 2) {
		$("td.selectable").each(function () {
			$(this).unbind('mouseenter').unbind('mouseleave');
		});
		clickCounter = 0;
		return;
	}
	$(elem).toggleClass("active");
}
$(".bi-chevron-left").click(function () {
	getPrevMonth();
});
 
$(".bi-chevron-right").click(function () {
	getNextMonth();
});