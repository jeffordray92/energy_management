function filter_room() {
    room = document.getElementById("room").value;
    window.location.href = '?room=' + room;
}

function filter_frequency(frequency) {
    room = document.getElementById("room").value;
    window.location.href = '?room=' + room + '&freq=' + frequency;
}

function filter_frequency_range(frequency) {
    room = document.getElementById("room").value;
    start = document.getElementById("start").value;
    end = document.getElementById("end").value;
    window.location.href = '?room=' + room + '&freq=' + frequency + '&start=' + start + '&end=' + end;
}


function btn1() {
    document.getElementById("hourly").disabled = true;
    document.getElementById("daily").disabled = false;
    document.getElementById("weekly").disabled = false;
    document.getElementById("monthly").disabled = false;
    document.getElementById("range").disabled = false;
    document.getElementById("rangeform").hidden = true;
    filter_frequency("hourly");
}

function btn2() {
    document.getElementById("hourly").disabled = false;
    document.getElementById("daily").disabled = true;
    document.getElementById("weekly").disabled = false;
    document.getElementById("monthly").disabled = false;
    document.getElementById("range").disabled = false;
    document.getElementById("rangeform").hidden = true;
    filter_frequency("daily");
}

function btn3() {
    document.getElementById("hourly").disabled = false;
    document.getElementById("daily").disabled = false;
    document.getElementById("weekly").disabled = true;
    document.getElementById("monthly").disabled = false;
    document.getElementById("range").disabled = false;
    document.getElementById("rangeform").hidden = true;
    filter_frequency("weekly");
}

function btn4() {
    document.getElementById("hourly").disabled = false;
    document.getElementById("daily").disabled = false;
    document.getElementById("weekly").disabled = false;
    document.getElementById("monthly").disabled = true;
    document.getElementById("range").disabled = false;
    document.getElementById("rangeform").hidden = true;
    filter_frequency("monthly");
}

function btn5() {
    document.getElementById("hourly").disabled = false;
    document.getElementById("daily").disabled = false;
    document.getElementById("weekly").disabled = false;
    document.getElementById("monthly").disabled = false;
    document.getElementById("range").disabled = false;
    document.getElementById("rangeform").hidden = true;
    filter_frequency("yearly");
}

function btn6() {
    document.getElementById("hourly").disabled = false;
    document.getElementById("daily").disabled = false;
    document.getElementById("weekly").disabled = false;
    document.getElementById("monthly").disabled = false;
    document.getElementById("range").disabled = true;
    document.getElementById("rangeform").hidden = false;
}

function myFunction() {
    var x = document.getElementById("myNavbar");
    if (x.className === "navbar") {
      x.className += " responsive";
    } else {
      x.className = "navbar";
    }
  }

function rangedate() {
    filter_frequency_range("range");
}
