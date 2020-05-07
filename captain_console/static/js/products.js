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
            if(searchText){

            }
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

        searchList.push(searchBox.val());

        // Clear out all the underlines for the filters
        for(let i = 0; i < filterButtons.length; i++)
            filterButtons[i].style.textDecoration = 'none';

        HandleSearch(event);
    });

    // When on the products site change the html to reflect the search and also change the searchText to be whatever the person searched
    if(window.location.pathname === '/products/'){
        const searchText = window.sessionStorage.getItem('searchText');
        if(searchText !== null && searchText !== undefined){
             searchBox.val(searchText);
             window.sessionStorage.removeItem('searchText');
        }

        const newHTML = window.sessionStorage.getItem('newHTML');
        if(newHTML !== null && newHTML !== undefined){
            $('#products').html(newHTML);
            window.sessionStorage.removeItem('newHTML');
        }
    }
});

function HandleSearch(event){
    event.preventDefault();
    displayChanges();
}

function displayChanges(){
    const searchText = searchList.join(' ');

    $.ajax({
        url: '/products?search=' + searchText,
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

            const joinedHTML = newHTML.join('');

            // Store data so that we can use it during a redirect
            window.sessionStorage.setItem('searchText', searchText);
            window .sessionStorage.setItem('newHTML', joinedHTML);

            // Change the html if we're at /products, else redirect to /products
            if(window.location.pathname === '/products/')
                $('#products').html(joinedHTML);
            else
                window.location.href = '/products/';
        },
        error: function(xhr, status, error){
            // TODO: Display error message (using toastr?)
            console.error(error);
        }
    });
}