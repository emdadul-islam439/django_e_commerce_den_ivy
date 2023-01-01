var updateBtns = document.getElementsByClassName('update-cart')
console.log('updateBtns.length = ', updateBtns.length)
for(i = 0; i < updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function(){
        var productId = this.dataset.product 
        var action = this.dataset.action
        console.log('productId:', productId, 'action:', action)


        console.log('USER: ', user)
        if(user == 'AnonymousUser'){
            updateCookieItem(productId, action)
        }else{
            updateUserOrder(productId, action)
        }
    })
}

function updateUserOrder(productId, action){
    console.log('User is authenticated, sending data...')

    url = '/update-item/'
    // var form = document.getElementById('form')
    // var csrftoken = form.getElementsByTagName('input')[0].value

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type' : 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            'productId': productId, 'action': action 
        })
    })

    .then((response) => {
        return response.json()
    })

    .then((data)=>{
        console.log('data:', data)
        location.reload()
    })
}

function updateCookieItem(productId, action){
    console.log('User is not logged in...')
    if(action == 'add'){
        if(cart[productId] == undefined){
            cart[productId] = {
                'quantity': 1, 
                'is_checked': true,
            }
        }else{
            cart[productId]['quantity'] += 1
        }
    }else if(action == 'remove'){
        cart[productId]['quantity'] -= 1

        if(cart[productId]['quantity'] <= 0){
            console.log('Item removed...')
            delete cart[productId]
        }
    }else if(action == 'check-uncheck'){
        cart[productId]['is_checked'] = !cart[productId]['is_checked']
    }

    console.log('Cart: ', cart)
    document.cookie = 'cart=' + JSON.stringify(cart) + ';domain=;path=/'
    location.reload()
}


var cannotAddBtns = document.getElementsByClassName('cannot-add-btn')
console.log('cannotAddBtns.length = ', cannotAddBtns.length)
for(i = 0; i < cannotAddBtns.length; i++){
    cannotAddBtns[i].addEventListener('click', function(){
        alert('Order Limit reached! Cannot add more!')
    })
}


var fadeInImages = document.getElementsByClassName('fade-while-hovering')
console.log('fadeInImages.length = ', fadeInImages.length)
for(i=0; i<fadeInImages.length; i++){
    fadeInImages[i].addEventListener('mouseover', function(){
        var counter = this.dataset.counter
        fadeInImages[counter].style.opacity = 0.5;
        document.getElementById("view-btn-id-"+counter).classList.remove("hidden")
    })
    fadeInImages[i].addEventListener('mouseout', function(){
        var counter = this.dataset.counter
        fadeInImages[counter].style.opacity = 1.0;
        document.getElementById("view-btn-id-"+counter).classList.add("hidden")
    })
}


var viewBtns = document.getElementsByClassName('view-btn')
console.log('viewBtns.length = ', viewBtns.length)
for(i=0; i<viewBtns.length; i++){
    viewBtns[i].addEventListener('mouseover', function(){
        var counter = this.dataset.counter
        viewBtns[counter].classList.remove("hidden")
        document.getElementById("img-id-"+counter).style.opacity = 0.5
    })
    viewBtns[i].addEventListener('mouseout', function(){
        var counter = this.dataset.counter
        viewBtns[counter].classList.add("hidden")
        document.getElementById("img-id-"+counter).style.opacity = 1.0
    })
}


var updateCartBtn = document.getElementById('update-cart-button')
if(updateCartBtn != null){
    updateCartBtn.addEventListener('click', function(){
        var cartId = this.dataset.cart 
        console.log('UPDATE-CART....  USER: ', user)
        if(user == 'AnonymousUser'){
            updateCookieCart()
        }else{
            updateRegisteredUserCart(cartId)
        }
    })
}


function updateRegisteredUserCart(cartId){
    url = '/update-registered-user-cart/'

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type' : 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            'cartId': cartId 
        })
    })

    .then((response) => {
        return response.json()
    })

    .then((data)=>{
        console.log('data:', data)
        location.reload()
    })
}

function updateCookieCart(){
    url = '/update-cookie-cart/'

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type' : 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            'cart': cart 
        })
    })

    .then((response) => {
        return response.json()
    })

    .then((data)=>{
        console.log('cart: ', cart)
        console.log('data[cart]:', data['cart'])
        cart = data['cart']
        document.cookie = 'cart=' + JSON.stringify(cart) + ';domain=;path=/'
        location.reload()
    })
}