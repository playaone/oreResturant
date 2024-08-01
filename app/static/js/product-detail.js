document.querySelectorAll('.product-img-item').forEach(e => {
    e.addEventListener('click', () => {
        let img = e.querySelector('img').getAttribute('src')
        document.querySelector('#product-img > img').setAttribute('src', img)
    })
})

document.querySelector('#view-all-description')?.addEventListener('click', () => {
    let content = document.querySelector('.product-detail-description-content')
    content.classList.toggle('active')
    document.querySelector('#view-all-description').innerHTML = content.classList.contains('active') ? 'view less' : 'view all'
})

let productInfo = document.querySelector(".product-info")
var productDetails = {}

function updateProductDetails(){
    productDetails.productId = productInfo.dataset.id;
    productDetails.productTitle = productInfo.querySelector('h1').textContent.trim();
    productDetails.currentPrice = productInfo.querySelector('.price').textContent;
    productDetails.image = document.querySelector('.product-img img').getAttribute('src');
}

function updateAddToCartBtn(){
    let flag = false
    for (x=0; x<cart.length; x++){
        flag = cart[x].productId == productInfo.dataset.id ? true : flag
    }

    productInfo.querySelector('.add-to-cart').textContent = flag ? "Remove from cart" : "Add to cart";
}

productInfo.addEventListener('click', e => {
    if (e.target.classList.contains('add-to-cart')){
        updateProductDetails();
        setCart(productDetails);
        updateAddToCartBtn();
    }
}, false)

updateAddToCartBtn();