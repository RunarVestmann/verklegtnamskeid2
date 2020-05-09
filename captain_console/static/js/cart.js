let cartProducts = [];

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
            productInStorage.quantity += amount;
            cart.save();
        }
        else{
            $.ajax({
                url: `/products/${id}/json`,
                type: 'GET',
                success: function(response){
                    const productInStorage = cart.find(id);
                    if(productInStorage){
                        productInStorage.quantity = Number(productInStorage.quantity);
                        productInStorage.quantity += amount;
                        cart.save();
                        return;
                    }

                    const productFromServer = response.data;
                    if(productFromServer){
                        productFromServer.quantity = 1;
                        cart.products.push(productFromServer);
                        cart.save();
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
            product.quantity = quantity;
            cart.save();
        }
    },

    remove(id, amount=1){
        const productInStorage = cart.find(id);

        if(productInStorage){
            productInStorage.quantity -= amount;

            // Remove the item all together if it's quantity is at or below zero
            if(productInStorage.quantity <= 0)
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
    if(window.location.pathname === '/cart/')
        renderProductsInCart();
});

function renderProductsInCart(){
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
                    <div class="product-line-price">${(p.price * p.quantity).toLocaleString('is').replace(',', '.')}</div>
                    </div>`;
    });
    $('#products').html(newHTML.join(''));
}

function addToCart(productID){
    cart.add(productID);
}

// Credit goes to https://bootsnipp.com/snippets/qrOrg
/* Set rates + misc */
let shippingRate = 1500;
let fadeTime = 300;

/* Remove item from cart */
function removeItem(removeButton, id)
{
    /* Remove row from DOM and recalc cart total */
    let productRow = $(removeButton).parent().parent();
    productRow.slideUp(fadeTime, function() {
        productRow.remove();
        recalculateCart();
        cart.removeAll(id);
    });
}

/* Recalculate cart */
function recalculateCart()
{
  let subtotal = 0;

  /* Sum up row totals */
  $('.product').each(function () {
    subtotal += $(this).children('.product-line-price').text();
  });

  /* Calculate totals */
  let shipping = (subtotal > 0 ? shippingRate : 0);
  let total = subtotal;// + shipping;

  /* Update totals display */
  $('.totals-value').fadeOut(fadeTime, function() {
    $('#cart-subtotal').html(subtotal);
    //$('#cart-shipping').html(shipping);
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
  let quantity = $(quantityInput).val();
  if(quantity <= 0)
      return removeItem(quantityInput, id);

  /* Calculate line price */
  let productRow = $(quantityInput).parent().parent();
  let price = Number(productRow.children('.product-price').text().replace('.', ''));
  let linePrice = price * quantity;

  cart.changeQuantity(id, quantity);

  /* Update line price display and recalc cart totals */
  productRow.children('.product-line-price').each(function () {
    $(this).fadeOut(fadeTime, function() {
      $(this).text(linePrice.toLocaleString('is').replace(',', '.'));
      recalculateCart();
      $(this).fadeIn(fadeTime);
    });
  });
}