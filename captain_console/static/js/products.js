const searchBox = $('#search-box');
const searchButton = $('#search-btn');
let searchList = [];

$(document).ready(function(){
    // When a filter gets clicked
    const filterButtons = $('.filter-btn');
    for(let i = 0; i < filterButtons.length; i++){
        const filter = filterButtons[i];
        filter.onmousedown = function(){
          if(filter.style.textDecoration !== 'underline')
              filter.style.textDecoration = 'underline';
          else
              filter.style.textDecoration = 'none';
        };
        filter.addEventListener('click', function(event){
            const searchText = filter.textContent;
            if(searchList.includes(searchText))
                searchList = searchList.filter(s => s !== searchText);
            else
                searchList.push(searchText);
            HandleSearch(event);
        });
    }

    // When the search button gets clicked
    searchButton.on('click', function(event){
        searchList = [];
        const value = searchBox.val();

        if(value)
            searchList.push(searchBox.val());

        // Clear out all the underlines for the filters
        for(let i = 0; i < filterButtons.length; i++)
            filterButtons[i].style.textDecoration = 'none';

        HandleSearch(event);
    });

    if(window.location.pathname === '/products/')
        $('#products').html(window.name);
});

function HandleSearch(event){
    event.preventDefault();

    displayChanges();
    if(window.location.pathname !== '/products/')
        window.location.href = '/products/';
}

function displayChanges(){
    $.ajax({
        url: '/products?search=' + searchList.join(' '),
        type: 'GET',
        success: function(response){
            const newHTML = response.data.map(p => {
                return `<div class="card" style="background-color: #38b8c3;">
                            <img class="card-img-top product-img m-2" src="${ p.first_image }" alt="Product image">
                            <div class="card-body">
                                <h5 class="card-title">${ p.name }</h5>
                                <p class="card-text">${ p.system.manufacturer } / ${ p.system.abbreviation } / ${ p.type }</p>
                                <p>Verð: <strong>${ p.price.toLocaleString('is') }</strong> ISK</p>
                                <a href="/products/${p.id}" class="btn btn-primary">Sjá nánar</a>
                                <a href="#" class="btn btn-success">Setja í körfu</a>
                            </div>
                        </div>`
            });

            if(window.location.pathname === '/products/')
                $('#products').html(newHTML.join(''));
            else
                window.name = newHTML.join('');
        },
        error: function(xhr, status, error){
            // TODO: Display error message (using toastr?)
            console.error(error);
        }
    });
}