const input = document.getElementById("search-box");
input.addEventListener("keyup", function(event) {
    if (event.keyCode === 13) {
        event.preventDefault();
        document.getElementById("search-btn").click();
    }
});
