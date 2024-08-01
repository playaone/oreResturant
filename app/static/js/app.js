document.querySelectorAll('.dropdown > a').forEach(e => {
    e.addEventListener('click', (event) => event.preventDefault())
})

document.querySelectorAll('.mega-dropdown > a').forEach(e => {
    e.addEventListener('click', (event) => event.preventDefault())
})

document.querySelector('#mb-menu-toggle').addEventListener('click', () => document.querySelector('#header-wrapper').classList.add('active'))

document.querySelector('#mb-menu-close').addEventListener('click', () => document.querySelector('#header-wrapper').classList.remove('active'))

products = document.querySelectorAll('.product-card');
badge = document.querySelector('.badge');

var cart = []

function setBadge() {
    badge.textContent = cart.length;
}

function getCart() {
    temp = localStorage.getItem('jayboyCart');
    if (temp) {
        cart = JSON.parse(temp);
        setBadge();
    }
}

function removeCartItem(productId){
    for(x=0; x<cart.length; x++){
        if(cart[x].productId == productId){
            cart.splice(x, 1)
            return true
        }
    }
    return false
}

function setCart(product) {    

    if(!removeCartItem(product.productId)){
        cart.push({
            'productId': product.productId,
            'productTitle': product.productTitle,
            'image': product.image,
            'currentPrice': product.currentPrice,
            'quantity': 1,
        })
    }


    localStorage.setItem('jayboyCart', (JSON.stringify(cart)))

    setBadge();
}

function checkTarget(e) {

    if (e.target.classList.contains('add-to-cart') || e.target.classList.contains('bxs-cart-add')) {
        
        return true
    }
    return false
}


function updateProductQnty(productId, qnty, div){

    if(qnty > 0){
        for(x=0; x<cart.length; x++){
            if(cart[x].productId == productId){
                cart[x].quantity = qnty
            }
        }
        div.textContent = qnty
        localStorage.setItem('jayboyCart', (JSON.stringify(cart)))

        return true
    }
    return false
}


if (products && products.length > 0) {

    products.forEach(product =>{
        product.addEventListener("click", e=>{
            if (checkTarget(e)){

                let productDetails = {
                    'productTitle' : product.querySelector('.product-card-name').textContent.trim(),
                    'currentPrice' : product.querySelector('.curr-price .price').textContent,
                    'image' : product.querySelector('.first-image').getAttribute('src'),
                    'productId' : product.dataset.id,
                }
                setCart(productDetails);
            }
        })
    });

}



getCart();