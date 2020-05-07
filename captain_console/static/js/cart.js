const cartDOM = document.getElementById('cart');

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
        await localStorage.setItem(cart.key, JSON.stringify(cart.products))
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

    clear(){
        cart.products = [];
        cart.sync();
    }
}

$(document).ready(() =>{
    cart.init();
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

function showCart(){
    cartDOM.style
}