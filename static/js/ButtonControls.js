function filter_room() {
    room = document.getElementById("room").value;
    window.location.href = '?room=' + room;
}

function filter_frequency(frequency) {
    room = document.getElementById("room").value;
    window.location.href = '?room=' + room + '&freq=' + frequency;
}


function btn1() {
    document.getElementById("hourly").disabled = true;
    document.getElementById("daily").disabled = false;
    document.getElementById("weekly").disabled = false;
    document.getElementById("monthly").disabled = false;
    document.getElementById("yearly").disabled = false;
    filter_frequency("hourly");
}

function btn2() {
    document.getElementById("hourly").disabled = false;
    document.getElementById("daily").disabled = true;
    document.getElementById("weekly").disabled = false;
    document.getElementById("monthly").disabled = false;
    document.getElementById("yearly").disabled = false;
    filter_frequency("daily");
}

function btn3() {
    document.getElementById("hourly").disabled = false;
    document.getElementById("daily").disabled = false;
    document.getElementById("weekly").disabled = true;
    document.getElementById("monthly").disabled = false;
    document.getElementById("yearly").disabled = false;
    filter_frequency("weekly");
}

function btn4() {
    document.getElementById("hourly").disabled = false;
    document.getElementById("daily").disabled = false;
    document.getElementById("weekly").disabled = false;
    document.getElementById("monthly").disabled = true;
    document.getElementById("yearly").disabled = false;
    filter_frequency("monthly");
}

function btn5() {
    document.getElementById("hourly").disabled = false;
    document.getElementById("daily").disabled = false;
    document.getElementById("weekly").disabled = false;
    document.getElementById("monthly").disabled = false;
    document.getElementById("yearly").disabled = true;
    filter_frequency("yearly");
}
