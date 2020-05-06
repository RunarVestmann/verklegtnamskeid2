//Make all the symbols flip between being + or a - when clicked and reveal what's under
const symbols = document.getElementsByClassName('symbol');

for(let i = 0; i < symbols.length; i++){
    const symbol = symbols[i];
    const filterChild = symbol.nextElementSibling.nextElementSibling;

    symbol.addEventListener('click', function(){
        if(symbol.textContent === '−'){
            symbol.textContent = '+';
            filterChild.style.display = 'none';
        }
        else{
            symbol.textContent = '−';
            filterChild.style.display = 'block';
        }
    });
}