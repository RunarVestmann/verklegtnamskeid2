const inputBox = document.getElementById('search-box');
const searchBtn = document.getElementById('search-btn');

inputBox.addEventListener("keyup", function(event) {
    if (event.keyCode === 13) {
        event.preventDefault();
        searchBtn.click();
    }
});

function navigationClick(searchText){
    inputBox.value = searchText;
    searchBtn.click();
}