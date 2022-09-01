var wishListButtons = document.getElementsByClassName('wish-list')
console.log('wishListButtons.length = ', wishListButtons.length)

for(i = 0; i < wishListButtons.length; i++){
    wishListButtons[i].addEventListener('click', function(){
        var productId = this.dataset.product 

        //for finding 'action', we have to get the clicked icon
        var wishIcons = this.getElementsByClassName('wish-list-icon')
        var action = wishIcons[0].dataset.action
        var clickedIcon = wishIcons[0]

        for(j = 0; j < wishIcons.length; j++){
            if(wishIcons[j].classList.contains('hidden') == false){
                action = wishIcons[j].dataset.action
                clickedIcon = wishIcons[j]
            }
        }

        console.log('productId:', productId, 'action:', action)

        console.log('USER: ', user)
        if(user == 'AnonymousUser'){
            alert('Login needed!')
        }else{
            updateWishList(productId, action, wishIcons)
        }
    })
}


function updateWishList(productId, action, wishIcons){
    console.log('User is authenticated, sending data...')

    url = '/update_wish_list/'

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
        console.log('response: ', response)
        return response.json()
    })

    .then((data)=>{
        console.log('data:', data)
        
        var addIcon = wishIcons[0]
        var removeIcon = wishIcons[1]

        if(action == 'add'){
            addIcon.classList.add("hidden")
            removeIcon.classList.remove("hidden")
        }
        else if(action == 'remove'){
            addIcon.classList.remove('hidden')
            removeIcon.classList.add('hidden')
        }
    })
}


// function addCookieItem(productId, action){
//     console.log('User is not logged in...')
//     if(action == 'add'){
//         if(cart[productId] == undefined){
//             cart[productId] = {'quantity': 1}
//         }else{
//             cart[productId]['quantity'] += 1
//         }
//     }else if(action == 'remove'){
//         cart[productId]['quantity'] -= 1

//         if(cart[productId]['quantity'] <= 0){
//             console.log('Item removed...')
//             delete cart[productId]
//         }
//     }
//     console.log('Cart: ', cart)
//     document.cookie = 'cart=' + JSON.stringify(cart) + ';domain=;path=/'
//     location.reload()
// }