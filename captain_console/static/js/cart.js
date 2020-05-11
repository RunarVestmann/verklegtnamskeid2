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

    add(id, amount=1){
        const productInStorage = cart.find(id);
        if(productInStorage){
            if(productInStorage.cartQuantity + amount > Number(productInStorage.quantity)){
                toastr.info(`Ekki er til nægilegt magn af ${productInStorage.name} til að setja í körfuna`);
                // Update quantity numbers
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
                        if(productInStorage.cartQuantity + amount > Number(productInStorage.quantity)){
                            toastr.info(`Ekki er til nægilegt magn af ${productInStorage.name} til að setja í körfuna`);
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
                        if(productFromServer.cartQuantity + amount > Number(productFromServer.quantity)){
                            toastr.info(`Ekki er til nægilegt magn af ${productInStorage.name} til að setja í körfuna`);
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
        if(index > -1){}
            array.splice(index, 1);
}

$(document).ready(function(){
    cart.init();
    shoppingCartBtn.textContent = cart.count();
    if(window.location.pathname === '/cart/'){
        renderProductsInCart();
        recalculateCart();
    }
});

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
                        <input type="number" value="${p.quantity}" min="1" max="99" onchange="updateQuantity(this , ${p.id})">
                    </div>
                    <div class="cart-product-removal" >
                        <button class="remove-cart-product" onclick="removeItem(this, ${p.id});">Eyða</button>
                    </div>
                        <div class="cart-product-line-price">${(p.price * p.quantity).toLocaleString('it')}</div>
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

function updateQuantity(quantityInput, id)
{
    let quantity = $(quantityInput).val();
    if(quantity <= 0)
        return removeItem(quantityInput, id);
    else if(quantity > 99){
        $(quantityInput).val(99);
        quantity = 99;
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
