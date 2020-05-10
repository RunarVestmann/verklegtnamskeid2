const searchBox = $('#search-box');
const searchButton = $('#search-btn');
const products = $('#products');
let productList = [];
let ascendingOrder = true;
let searchList = [];

$(document).ready(function(){
    // Set up all the onclick events for the buttons
    setupOrderByButtons();
    const filterButtons = setupFilterButtons();
    setupSearchButton(filterButtons);

    // Set the correct settings for the AJAX connection
    setupAjax();

    // When the site gets refreshed or the user was redirected do the following:
    if(window.location.pathname === '/products/'){

        // Set the search box text to be what the user searched for
        const searchText = window.sessionStorage.getItem('searchText');
        if(searchText !== null && searchText !== undefined){
             searchBox.val(searchText);
             window.sessionStorage.removeItem('searchText');
        }

        // Store behind the scenes all the products being displayed if they aren't already being stored
        else if(productList.length === 0)
             getAndStoreAllProducts();
    }
});

function setupOrderByButtons(){
    const orderByButtons = $('.order-by-btn');
    for(let i = 0; i < orderByButtons.length; i++) {
        const button = orderByButtons[i];
        button.onmousedown = function () {
            const arrow = $('#arrow');
            $(arrow).insertAfter($(button));
            if(button.classList.contains('product-order-bar-link')){
                $('.order-by-btn').each(function () {
                    $(this).toggleClass('product-order-bar-link');
                    $(this).toggleClass('product-order-bar-active');
                });
            }
            else flipArrow();
        }
    };
}

function setupFilterButtons(){
    const filterButtons = $('.filter-btn');
    for(let i = 0; i < filterButtons.length; i++){
        const filter = filterButtons[i];

        const startingColor = filter.style.backgroundColor;

        filter.addEventListener('click', function(event){
            if(filter.style.fontWeight !== 'bold'){
                filter.style.fontWeight = 'bold';
                filter.style.backgroundColor = '#99a6ac';
                filter.style.borderRadius = '1.3rem';
            }
            else{
                filter.style.fontWeight = 'normal';
                filter.style.backgroundColor = startingColor;
                filter.style.borderRadius = '0rem';
            }
            const searchBoxValue = searchBox.val();

            if(searchBoxValue && searchList.length === 1 && searchList.includes(searchBoxValue))
                searchList = [];

            const searchText = filter.textContent;

            if(searchList.includes(searchText))
                searchList = searchList.filter(s => s !== searchText);
            else
                searchList.push(searchText);
            handleSearch(event);
        });
    }
    return filterButtons;
}

function setupSearchButton(filterButtons){
    // When the search button gets clicked
    searchButton.on('click', function(event){
        searchList = [];
        searchList.push(searchBox.val());

        // Clear out all the underlines for the filters
        for(let i = 0; i < filterButtons.length; i++){
            filterButtons[i].style.textDecoration = 'none';
            filterButtons[i].style.fontWeight = 'normal';
        }
        handleSearch(event);
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

function handleSearch(event){
    event.preventDefault();
    displayChanges();
}

function getAndStoreAllProducts(){
    $.ajax({
        url: '/products?search=',
        type: 'GET',
        success: function(response){
            productList = [];
            response.data.forEach(product => {
                const productHTML = getProductHTML(product);

                //Store all the products in a list for further use
                productList.push({
                    product: product,
                    html: productHTML
                });
            });
            if($('.product-order-bar-active').text() === 'Nafni')
                orderByName();
            else
                orderByPrice();
        }
    });
}

function displayChanges(){
    const searchText = searchList.join(' ');

    if(!searchText && window.location.pathname !== '/products/'){
        window.location.href = '/products/';
        return;
    }

    $.ajax({
        url: '/products?search=' + searchText,
        type: 'GET',
        success: function(response){
            productList = [];
            const newHTML = response.data.map(product => {
                const productHTML = getProductHTML(product);

                //Store all the products in a list for further use
                productList.push({
                   product: product,
                   html: productHTML
                });
                return productHTML;
            });

            if(window.location.pathname === '/products/')
                products.html(newHTML.join(''));
            else{
                // Store data so that we can use it on the redirect page
                window.sessionStorage.setItem('searchText', searchText);

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

function getProductHTML(product){
    return `<div class="products-box">
                            <div class="container-fluid">
                                <div class="row">
                                    <div class="col-12 p-0">
                                        <div class="products-img-frame"><img class="product-img" src="${ product.first_image }" alt=${ product.name }></div>
                                    </div>
                                </div>
                                <div class="row mt-2">
                                    <div class="col-12 p-0">
                                        <div class="products-name">${ product.name }</div>
                                    </div>
                                </div>
                                 <div class="row my-2">
                                    <div class="col-7 p-0">
                                        <div class="products-type">${ product.system.manufacturer } / ${ product.system.abbreviation } / ${ product.type }</div>
                                    </div>
                                    <div class="col-5 p-0">
                                         <div class="products-price">Verð: <strong>${ product.price.toLocaleString('it') }</strong> ISK</div>
                                    </div>
                                </div>
                                <div class="row mt-3">
                                    <div class="col-6 p-1">
                                        <a href="/products/${product.id}" onclick="onDetailClick(${product.id})" class="btn btn-warning btn-block">Nánar</a>
                                    </div>
                                    <div class="col-6 p-1">
                                        <div role="button" onclick="addToCart(${product.id})" class="btn btn-success btn-block">Setja í körfu</div>
                                    </div>
                                </div>
                            </div>
                        </div>`;
}

function onDetailClick(productId){
    const clickedProducts = localStorage.getItem('clickedProducts');

    if(clickedProducts){
        const products = JSON.parse(clickedProducts);

        // Only stop from sending the server data when we already have
        if(products.includes(productId))
            return;

        // Otherwise we store locally that we've clicked on the given product
        else{
            products.push(productId);
            localStorage.setItem('clickedProducts', JSON.stringify(products));
        }
    }
    else
        localStorage.setItem('clickedProducts', JSON.stringify([productId]));

   $.ajax({
       url: '/user/add_to_search',
       method: 'POST',
       data: JSON.stringify(productId)
   });

}

function flipArrow(){
    const arrow = $('#arrow');
    ascendingOrder = !ascendingOrder;
    if(ascendingOrder)
        arrow.attr('transform', '');
    else
        arrow.attr('transform', 'rotate(180)');
}

function orderByName(){
    productList.sort(function(a, b){
        const aName = a.product.name.toUpperCase();
        const bName = b.product.name.toUpperCase();

        if(aName > bName)
            return ascendingOrder ? 1 : -1;
        if(aName < bName)
            return ascendingOrder ? -1 : 1;
        return 0;
    });

    const newHTML = productList.map(product => {
       return product.html;
    });
    products.html(newHTML.join(''));
}

function orderByPrice(){
    productList.sort(function(a, b){
        const aPrice = Number(String(a.product.price).split('.').join(''));
        const bPrice = Number(String(b.product.price).split('.').join(''));

        return ascendingOrder ? aPrice -bPrice : bPrice - aPrice;
    });

    const newHTML = productList.map(product => {
       return product.html;
    });
    products.html(newHTML.join(''));
}
