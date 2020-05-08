const cart = {
    key: 'cart',
    products: [],
    init(){
        const storedProducts = localStorage.getItem(cart.key);

        if(storedProducts)
            cart.products = JSON.parse(storedProducts);
        else{
            cart.products = [];
            cart.sync();
        }
    },

    // Sync the local storage with what's in the cart object
    async sync(){
        await localStorage.setItem(cart.key, JSON.stringify(cart.products));
    },

    find(id){
        return cart.products.find(product => product.id == id);
    },

    add(id, amount=1){
        const product = cart.find(id);
        if(product){
            product.quantity += amount;
            cart.sync();
        }
        else{
            $.ajax({
                url: `/products/${id}/json`,
                type: 'GET',
                success: function(response){
                    const prod = response.data;
                    if(prod){
                        prod.quantity = 1;
                        cart.products.push(prod);
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

    remove(id, amount=1){
        const product = cart.find(id);

        if(product){
            product.quantity -= amount;

            // Remove the item all together if it's quantity is at or below zero
            if(product.quantity <= 0){
                const index = cart.products.indexOf(product);
                if(index > -1)
                    cart.products.splice(index, 1);
            }
            cart.sync();
        }
    },

    delete(id){
        const product = cart.find(id);
        if(product){
            const index = cart.products.indexOf(product);
            if(index > -1){
                cart.products.splice(index, 1);
                cart.sync();
            }
        }
    },

    clear(){
        cart.products = [];
        cart.sync();
    }
}

$(document).ready(() =>{
    cart.init();
    if(window.location.pathname === '/cart/'){
        const newHTML = cart.products.map(p => {
            return `<div class="product-cart-view">
                        <div class="product-cart-image">
                          <img src="${p.first_image}">
                        </div>
                        <div class="product-details">
                          <div class="product-title">${p.name}</div>
                        </div>
                        <div class="product-price">${p.price.toLocaleString('is').replace(',', '.')}</div>
                        <div class="product-quantity">
                          <input type="number" value="${p.quantity}" min="1" onchange="updateQuantity(this , ${p.id})">
                        </div>
                        <div class="product-removal" >
                          <button class="remove-product" onclick="removeItem(this, ${p.id});">
                            Remove
                          </button>
                        </div>
                        <div class="product-line-price">${p.price * p.quantity}</div>
                        </div>`;
        });
        $('#products').html(newHTML.join(''));
    }
});

function addToCart(id, ){
    cart.add(id);
    console.log(cart);
}

function removeFromCart(){
    cart.remove(id);
}

function clearCart(){
    cart.clear();
}

// Credit goes to https://bootsnipp.com/snippets/qrOrg

/* Set rates + misc */
let shippingRate = 15.00;
let fadeTime = 300;

/* Remove item from cart */
function removeItem(removeButton, id)
{
  /* Remove row from DOM and recalc cart total */
  let productRow = $(removeButton).parent().parent();
  productRow.slideUp(fadeTime, function() {
      productRow.remove();
      recalculateCart();
      cart.delete(id);
  });
}

/* Recalculate cart */
function recalculateCart()
{
  let subtotal = 0;

  /* Sum up row totals */
  $('.product').each(function () {
    subtotal += parseFloat($(this).children('.product-line-price').text());
  });

  /* Calculate totals */
  let shipping = (subtotal > 0 ? shippingRate : 0);
  let total = subtotal + shipping;

  /* Update totals display */
  $('.totals-value').fadeOut(fadeTime, function() {
    $('#cart-subtotal').html(subtotal);
    $('#cart-shipping').html(shipping);
    $('#cart-total').html(total);
    if(total == 0){
      $('.checkout').fadeOut(fadeTime);
    }else{
      $('.checkout').fadeIn(fadeTime);
    }
    $('.totals-value').fadeIn(fadeTime);
  });
}

/* Update quantity */
function updateQuantity(quantityInput, id)
{
  /* Calculate line price */
  let productRow = $(quantityInput).parent().parent();
  let price = parseFloat(productRow.children('.product-price').text());
  let quantity = $(quantityInput).val();
  let linePrice = price * quantity;

  const product = cart.find(id);
  if(product) {
      product.quantity = quantity;
      cart.sync();
  }

  /* Update line price display and recalc cart totals */
  productRow.children('.product-line-price').each(function () {
    $(this).fadeOut(fadeTime, function() {
      $(this).text(linePrice.toFixed(2));
      recalculateCart();
      $(this).fadeIn(fadeTime);
    });
  });


}