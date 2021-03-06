const searchBox = $('#search-box');
const searchButton = $('#search-btn');
const products = $('#products');
let productList = [];
let ascendingOrder = true;

const filters = [];

let searchText = '';
let manufacturerList = [];
let typeList = [];
let systemList = [];

let doneFetchingMissingProducts = true;

$(document).ready(function(){
    // Set up all the onclick events for the buttons
    setupOrderByButtons();
    const filterButtons = setupFilterButtons();
    setupSearchButton(filterButtons);

    // Set the correct settings for the AJAX connection
    setupAjax();

    // When the site gets refreshed or the user was redirected do the following:
    if(window.location.pathname === '/products/'){
        const prodList = window.sessionStorage.getItem('productList');
        if(prodList){
            productList = JSON.parse(prodList);
            const newHTML = productList.map(product => { return product.html; });
            products.html(newHTML.join(''));
            window.sessionStorage.removeItem('productList');
        }
        else{
            // Fill up the product list if it's empty
            if(productList.length === 0){
                doneFetchingMissingProducts = false;
                $.ajax({
                   url: '/products?all',
                   method: 'GET',
                   success: function(response){
                       if(response.data){
                           response.data.forEach(prod => {
                              productList.push({
                                  product: prod,
                                  html: getProductHTML(prod)
                              });
                           });
                       }
                       doneFetchingMissingProducts = true;
                   }
                });
            }
        }
        const search = window.sessionStorage.getItem('search');
        if(search){
            searchBox.val(search);
            window.sessionStorage.removeItem('search');
        }

        const navClick = window.sessionStorage.getItem('navClick');
        if(navClick){
            highlightFilter(navClick);
            window.sessionStorage.removeItem('navClick');
        }
    }
    // Clear the stored clicked products when the user signs up or logs in
    else if(window.location.pathname === '/user/login' || window.location.pathname === '/user/signup')
        sessionStorage.removeItem('clickedProducts');
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

        const index = filters.length;
        filters.push({
            filter: filter,
            toggle: false,
            startingColor: filter.style.backgroundColor,
        });

        filter.addEventListener('click', function(event){
            if(!filters[index].toggle)
                filter.style.backgroundColor = '#99a6ac';
            else
                filter.style.backgroundColor = filters[index].startingColor;
            filters[index].toggle = !filters[index].toggle;

            if(filter.classList.contains('type')){
                const type = filter.textContent.trim();
                if(typeList.includes(type))
                    typeList = typeList.filter(s => s !== type);
                else
                    typeList.push(type);
            }
            else if(filter.classList.contains('manufacturer')){
                const manufacturer = filter.textContent.trim();
                if(manufacturerList.includes(manufacturer))
                    manufacturerList = manufacturerList.filter(s => s !== manufacturer);
                else
                    manufacturerList.push(manufacturer);
            }
            else if(filter.classList.contains('system')){
                const system = filter.textContent.trim();
                if(systemList.includes(system))
                    systemList = systemList.filter(s => s !== system);
                else
                    systemList.push(system);
            }
            searchText = searchBox.val();
            handleSearch(event);
        });
    }
    return filterButtons;
}

function setupSearchButton(filterButtons){
    // When the search button gets clicked
    searchButton.on('click', function(event){
        typeList = [];
        manufacturerList = [];
        systemList = [];
        searchText = searchBox.val();

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

function displayChanges(){
    $('.loader-wrapper-2').show();

    // All the different filters, excluding the search
    let typeText = typeList.join('_');
    let manufacturerText = manufacturerList.join('_');
    let systemText = systemList.join('_');

    // The url we're gonna GET a json response from
    let url = '';

    // If we are not filtering we grab all the products
    if(!searchText && !typeText && !manufacturerText && !systemText)
    {
        url = '/products?all';
        if(window.location.pathname === '/products/')
            dehighlightFilters();
    }

    // Otherwise we do some filtering by setting url params
    else{
        const urlParams = [];

        if(searchText){
            urlParams.push('search=' + searchText);
            dehighlightFilters();
        }
        else{
            if(typeText)
                urlParams.push('type=' + typeText);
            if(manufacturerText)
                urlParams.push('manufacturer=' + manufacturerText);
            if(systemText)
                urlParams.push('system=' + systemText);
        }
        url = '/products?' + urlParams.join('&');
    }

    $.ajax({
        url: url,
        type: 'GET',
        success: function(response){
            if(window.location.pathname === '/products/')
                $('.loader-wrapper-2').hide();


            productList = [];

            //Cache the products we got from the response so we can change the order we display the products
            response.data.forEach(product => {
                productList.push({
                   product: product,
                   html: getProductHTML(product)
                });
            });

            // Set the correct order for the products
            if(window.location.pathname === '/products/'){
                const activeOrderBtn = $('.product-order-bar-active')

                if(activeOrderBtn){
                    if($(activeOrderBtn).text() === 'Nafni')
                        orderByName(true);
                    else
                        orderByPrice(true);
                }
                else
                    orderByName(true);
            }
            // If we are not at /products we store the cached list in sessionStorage and redirect
            else{
                window.sessionStorage.setItem('productList', JSON.stringify(productList));
                if(searchText)
                    window.sessionStorage.setItem('search', searchText);
                else if(searchBox.val())
                    window.sessionStorage.setItem('search', searchBox.val());

                // Redirect to /products
                window.location.href = '/products?noproduct';
            }

        },
        error: function(xhr, status, error){
            $('.loader-wrapper-2').hide();
            toastr.error('Ekki gekk að ná í vörurnar');
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
                                        ${product.quantity > 0 ? `<div role="button" onclick="addToCart(${product.id})" class="btn btn-success btn-block">Setja í körfu</div>` : '<div class="btn btn-secondary btn-block disabled" aria-disabled="true" style="font-size: 1.2rem;cursor: default;">Væntanlegt</div>'}
                                    </div>
                                </div>
                            </div>
                        </div>`;
}

// Send which product was clicked to the server to store in search history
function onDetailClick(productId){
    const clickedProducts = sessionStorage.getItem('clickedProducts');

    if(clickedProducts){
        const products = JSON.parse(clickedProducts);

        // Only stop from sending the server data when we already have
        if(products.includes(productId))
            return;

        // Otherwise we store locally that we've clicked on the given product
        else{
            products.push(productId);
            sessionStorage.setItem('clickedProducts', JSON.stringify(products));
        }
    }
    else
        sessionStorage.setItem('clickedProducts', JSON.stringify([productId]));

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

function orderByName(jsOrder=false){
    // If a click resulted in this function call and the items aren't done loading
    if(!jsOrder && !doneFetchingMissingProducts){
        toastr.info('Er enn að sækja vörurnar, prófaðu að smella aftur innan skamms');
        return;
    }
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

function orderByPrice(jsOrder=false){
    // If a click resulted in this function call and the items aren't done loading
    if(!jsOrder && !doneFetchingMissingProducts){
        toastr.info('Er enn að sækja vörurnar, prófaðu að smella aftur innan skamms');
        return;
    }
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

function navigationClick(text){
    if(window.location.pathname === '/products/'){
        dehighlightFilters();
        highlightFilter(text);
    }
    else{
        typeList = [];
        manufacturerList = [];
        systemList = [];
        searchText = '';
        manufacturerList.push(text);
        window.sessionStorage.setItem('navClick', text);
    }
    displayChanges();
}

function highlightFilter(text){
    filters.forEach(button => {
       if(button.filter.textContent == text){
           manufacturerList.push(text);
           button.toggle = true;
           if(button.toggle)
                button.filter.style.backgroundColor = '#99a6ac';
            else
                button.filter.style.backgroundColor = button.startingColor;
       }
    });
}

function dehighlightFilters(){
    typeList = [];
    manufacturerList = [];
    systemList = [];
    searchText = '';
    filters.forEach(button => {
        button.toggle = false;
        button.filter.style.backgroundColor = button.startingColor;
        button.filter.style.fontWeight = 'bold';
    });
}