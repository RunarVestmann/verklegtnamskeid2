const searchBox = $('#search-box');
const searchButton = $('#search-btn');
const products = $('#products');
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
            const searchBoxValue = searchBox.val();

            if(searchBoxValue && searchList.length === 1 && searchList.includes(searchBoxValue))
                searchList = [];

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
            products.html(newHTML);
            window.sessionStorage.removeItem('newHTML');
        }
    }
    setupAjax();
});

function HandleSearch(event){
    event.preventDefault();
    displayChanges();
}

function displayChanges(){
    const searchText = searchList.join(' ');

    if(!searchText && window.location.href !== '/products/'){
        window.location.href = '/products/';
        return;
    }

    $.ajax({
        url: '/products?search=' + searchText,
        type: 'GET',
        success: function(response){
            const newHTML = response.data.map(p => {
                return `<div class="products-box">
                            <div class="container-fluid">
                                <div class="row">
                                    <div class="col-12 p-0">
                                        <div class="products-img-frame"><img class="product-img" src="${ p.first_image }" alt=${ p.name }></div>
                                    </div>
                                </div>
                                <div class="row mt-2">
                                    <div class="col-12 p-0">
                                        <div class="products-name">${ p.name }</div>
                                    </div>
                                </div>
                                 <div class="row my-2">
                                    <div class="col-7 p-0">
                                        <div class="products-type">${ p.system.manufacturer } / ${ p.system.abbreviation } / ${ p.type }</div>
                                    </div>
                                    <div class="col-5 p-0">
                                         <div class="products-price">Verð: <strong>${ p.price.toLocaleString('is').replace(',', '.') }</strong> ISK</div>
                                    </div>
                                </div>
                                <div class="row mt-3">
                                    <div class="col-6 p-1">
                                        <a href="/products/${p.id}" onclick="onDetailClick(${p.id})" class="btn btn-warning btn-block">Nánar</a>
                                    </div>
                                    <div class="col-6 p-1">
                                        <div role="button" onclick="addToCart(${p.id}")" class="btn btn-success btn-block">Setja í körfu</div>
                                    </div>
                                </div>
                            </div>
                        </div>`;
            });

            const joinedHTML = newHTML.join('');

            if(window.location.pathname === '/products/')
                products.html(joinedHTML);
            else{
                // Store data so that we can use it during a redirect
                window.sessionStorage.setItem('searchText', searchText);
                window .sessionStorage.setItem('newHTML', joinedHTML);

                // Redirect to /products
                window.location.href = '/products/';
            }

        },
        error: function(xhr, status, error){
            // TODO: Display error message (using toastr?)
            console.error(error);
        }
    });
}

function setupAjax(){
    $.ajaxSetup({
     beforeSend: function(xhr, settings) {
         function getCookie(name) {
             var cookieValue = null;
             if (document.cookie && document.cookie != '') {
                 var cookies = document.cookie.split(';');
                 for (var i = 0; i < cookies.length; i++) {
                     var cookie = jQuery.trim(cookies[i]);
                     // Does this cookie string begin with the name we want?
                     if (cookie.substring(0, name.length + 1) == (name + '=')) {
                         cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                         break;
                     }
                 }
             }
             return cookieValue;
         }
         if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
             // Only send the token to relative URLs i.e. locally.
             xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
         }
     }
});
}

function onDetailClick(productId){
   $.ajax({
       url: '/user/add_to_search',
       method: 'POST',
       data: JSON.stringify(productId)
   });

}
