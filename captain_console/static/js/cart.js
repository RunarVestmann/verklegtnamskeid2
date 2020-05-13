const shoppingCartBtn = document.getElementsByClassName('shopping-cart-btn')[0];

const cart = {
    key: 'cart',
    products: [],
    init(){
        const storedProducts = localStorage.getItem(cart.key);

        if(storedProducts)
            cart.products = JSON.parse(storedProducts);
        else
            cart.save();
    },

    // Sync the local storage with what's in the cart object
    save(){
        localStorage.setItem(cart.key, JSON.stringify(cart.products));
    },

    find(id){
        return cart.products.find(product => product.id == id);
    },

    updateLocalProducts(){
        cart.products.forEach(product => {
            const index = cart.products.indexOf(product);
            $.ajax({
                url: `/products/${product.id}/json`,
                method: 'GET',
                success: function(response){
                    productFromServer = response.data;
                    if(productFromServer.id){
                        const quantityInCart = product.cartQuantity;

                        product = productFromServer;
                        if(quantityInCart <= product.quantity)
                            product.cartQuantity = quantityInCart;
                        else{
                            product.cartQuantity = product.quantity;
                            toastr.info(`Núna er${product.cartQuantity > 1 || product.cartQuantity == 0 ? 'u' : ''}
                             ${product.cartQuantity} stk af ${product.name} í körfunni vegna skorts á magni`);
                        }
                        cart.products[index] = product;
                        cart.save();
                        shoppingCartBtn.textContent = cart.count();
                        if(window.location.pathname === '/cart/'){
                            renderProductsInCart();
                            recalculateCart();
                        }
                    }
                    else{
                        toastr.info(`${cart.products[index].name} selst ekki lengur og fjarlægðist úr körfunni`);
                        cart.products.splice(index, 1);
                        cart.save();
                        shoppingCartBtn.textContent = cart.count();
                        if(window.location.pathname === '/cart/'){
                            renderProductsInCart();
                            recalculateCart();
                        }
                    }
                },
                error: function(xhr, status, error){
                    if(xhr.status == 404){
                        toastr.info(`${cart.products[index].name} selst ekki lengur og fjarlægðist úr körfunni`);
                        cart.products.slice(index, 1);
                        cart.save();
                        shoppingCartBtn.textContent = cart.count();
                        if(window.location.pathname === '/cart/'){
                            renderProductsInCart();
                            recalculateCart();
                        }
                    }
                }
            });
        })

    },

    canAdd(product, amount){
        if(product.cartQuantity + amount > Number(product.quantity)){
            toastr.info(`Ekki er til nægilegt magn af ${product.name} til að setja í körfuna`);
            cart.updateLocalProducts();
            return false;
        }
        return true;
    },

    add(id, amount=1){
        const productInStorage = cart.find(id);
        if(productInStorage){
            if(!cart.canAdd(productInStorage, amount)){
                return;
            }else{
                productInStorage.cartQuantity += amount;
                cart.save();
                toastr.success(`${productInStorage.name} bættist í körfuna`);
                shoppingCartBtn.textContent = cart.count();
            }
        }
        else{
            $.ajax({
                url: `/products/${id}/json`,
                type: 'GET',
                success: function(response){
                    const productInStorage = cart.find(id);
                    if(productInStorage){
                        if(!cart.canAdd(productInStorage, amount)){
                            return;
                        }
                        productInStorage.cartQuantity = Number(productInStorage.cartQuantity);
                        productInStorage.cartQuantity += amount;
                        cart.save();
                        toastr.success(`${productInStorage.name} bættist í körfuna`);
                        shoppingCartBtn.textContent = cart.count();
                        return;
                    }

                    const productFromServer = response.data;
                    if(productFromServer){
                        if(!cart.canAdd(productFromServer, amount)){
                            return;
                        }
                        productFromServer.cartQuantity = 1;
                        cart.products.push(productFromServer);
                        cart.save();
                        toastr.success(`${productFromServer.name} bættist í körfuna`);
                        shoppingCartBtn.textContent = cart.count();
                    }
                    else{
                        // TODO: Show a message that says that the product id was not found
                        console.log('Product with id ' + id + ' was not found');
                    }
                },
                error: function(xhr, status, error){
                    // TODO: Show error message using toastr?
                    console.error(error);
                }
            });
        }
    },

    changeQuantity(id, quantity){
        const product = cart.find(id);
        if(product){
            product.cartQuantity = Number(quantity);
            cart.save();
        }
    },

    remove(id, amount=1){
        const productInStorage = cart.find(id);

        if(productInStorage){
            productInStorage.cartQuantity -= amount;

            // Remove the item all together if it's quantity is at or below zero
            if(productInStorage.cartQuantity <= 0)
                removeItemFromArray(cart.products, productInStorage);
            cart.save();
        }
    },

    removeAll(id){
        const product = cart.find(id);
        if(product){
            removeItemFromArray(cart.products, product);
            cart.save();
            return product;
        }
    },

    count(){
        let counter = 0;
        for(let i = 0; i < cart.products.length; i++)
            counter += Number(cart.products[i].cartQuantity);
        return counter;
    },

    clear(){
        cart.products = [];
        cart.save();
    }
}

function removeItemFromArray(array, item){
    const index = array.indexOf(item);
        if(index > -1)
            array.splice(index, 1);
}

$(document).ready(function(){
    cart.init();
    shoppingCartBtn.textContent = cart.count();

    if(window.location.pathname.includes('cart')){
        cart.updateLocalProducts();
        if(window.location.pathname !== '/cart/overview')
            sendCartProductsToServer();
    }

    if(window.location.pathname === '/cart/'){
        renderProductsInCart();
        recalculateCart();
    }
    else if(window.location.pathname === '/cart/overview'){
        renderProductsInCartOverview();
        recalculateCart();
    }
});

function sendCartProductsToServer(){
    $.ajax({
        url: '/cart/sync',
        method: 'PUT',
        data: JSON.stringify(cart.products),
        success: function(response){
            if(response.nonExistingProductIds){
                response.nonExistingProductIds.forEach(id => {
                   const removedProduct = cart.removeAll(id);
                   if(removedProduct)
                       toastr.info(`${removedProduct.name} selst ekki lengur og fjarlægðist úr körfunni`);
                });
            }
        }
    });
}

function renderProductsInCart(){
    const newHTML = cart.products.map(p => {
        return `<div class="cart-product">
                    <div class="cart-product-image">
                      <img src="${p.first_image}">
                    </div>
                    <div class="cart-product-details">
                      <div class="cart-product-title">${p.name}</div>
                    </div>
                    <div class="cart-product-price">${p.price.toLocaleString('it')}</div>
                    <div class="cart-product-quantity">
                        <input type="number" value="${p.cartQuantity}" min="1" max="${p.quantity}" onchange="updateQuantity(this , ${p.id}, ${p.quantity})">
                    </div>
                    <div class="cart-product-removal" >
                        <button class="remove-cart-product" onclick="removeItem(this, ${p.id});">Eyða</button>
                    </div>
                        <div class="cart-product-line-price">${(p.price * p.cartQuantity).toLocaleString('it')}</div>
                    </div>`;
    });
    $('#cart-products').html(newHTML.join(''));
}

function addToCart(productID){
    cart.add(productID);
}

const fadeTime = 300;

function removeItem(removeButton, id)
{
    /* Remove row from DOM and recalc cart total */
    let productRow = $(removeButton).parent().parent();
    productRow.slideUp(fadeTime, function() {
        productRow.remove();
        recalculateCart();
        cart.removeAll(id);
        shoppingCartBtn.textContent = cart.count();
    });
}

function recalculateCart()
{
    let total = 0;
    /* Sum up row totals */
    $('.cart-product').each(function () {
        total += Number($(this).children('.cart-product-line-price').text().split('.').join(''));
    });
    updateTotalsDisplay(total);
}

function updateTotalsDisplay(total){
    $('.totals-value').fadeOut(fadeTime, function() {
        $('#cart-total').html(total.toLocaleString('it'));
        if(total == 0){
            $('.checkout').addClass('disabled');
            $('.checkout').attr('aria-disabled', 'true').css('opacity', 0.5);
        }
        else{
            $('.checkout').removeClass('disabled');
            $('.checkout').attr('aria-disabled', 'false').css('opacity', 1);
        }
        $('.totals-value').fadeIn(fadeTime);
    });
}

function updateQuantity(quantityInput, id, max)
{
    let quantity = $(quantityInput).val();
    if(quantity <= 0)
        return removeItem(quantityInput, id);
    else if(quantity > max){
        $(quantityInput).val(max);
        quantity = max;
    }

    /* Calculate line price */
    let productRow = $(quantityInput).parent().parent();
    let price = Number(productRow.children('.cart-product-price').text().split('.').join(''));
    let linePrice = price * quantity;

    cart.changeQuantity(id, quantity);
    shoppingCartBtn.textContent = cart.count();

  /* Update line price display and recalc cart totals */
    productRow.children('.cart-product-line-price').each(function () {
        $(this).fadeOut(fadeTime, function() {
            $(this).text(linePrice.toLocaleString('it'));
            recalculateCart();
            $(this).fadeIn(fadeTime);
        });
    });
}

function renderProductsInCartOverview(){
    let totalprice = 0;
    const newHTML = cart.products.map(p => {
        totalprice += (p.price * p.cartQuantity)
        return `<div class="row cart-overview-lines">       
                     <div class="col-12 col-lg-6">${p.name}</div>
                      <div class="col-6 col-lg-2">${p.cartQuantity} stk</div>
                      <div class="col-6 col-lg-4 text-right">Verð: ${(p.price * p.cartQuantity).toLocaleString('it')} ISK</div>
                    </div>`;
    });
    $('#cart-products').html(newHTML.join(''));
    $('#total').html(totalprice.toLocaleString('it'));

}


