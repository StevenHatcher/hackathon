/* Modified from https://www.w3schools.com/howto/howto_js_dropdown.asp */
/* When the user clicks on the button, 
toggle between hiding and showing the dropdown content */
function dropDown() {
document.getElementById("searchDropdown").classList.toggle("show");
}

// Close the dropdown if the user clicks outside of it
window.onclick = function(event) {
if (!event.target.matches('.dropbtn')) {
    var dropdowns = document.getElementsByClassName("dropdown-content");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
    var openDropdown = dropdowns[i];
    if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
    }
    }
}
}

function add_dropDown() {
document.getElementById("addDropdown").classList.toggle("show");
}