var wishListButtons = document.getElementsByClassName('wishlist-class-wish-list')
console.log('wishListButtons.length = ', wishListButtons.length)
for(i = 0; i < wishListButtons.length; i++){
    wishListButtons[i].addEventListener('click', function(){
        var productId = this.dataset.product
        console.log("productId = " + productId)

        //for finding 'action', we have to get the clicked icon
        var addIcon = document.getElementById("add-btn-" + productId)
        var action = "remove"

        console.log('productId:', productId, 'action:', action)

        console.log('USER: ', user)
        if(user == 'AnonymousUser'){
            alert('Login needed!')
        }else{
            removeFromWishList(productId, action)
        }
    })
}

function removeFromWishList(productId, action){
    console.log('User is authenticated, sending data...')

    url = '/update-wishlist/'

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
        // location.reload()
        var clickedItemId = document.getElementById("wishlist-item-id-" + productId)
        clickedItemId.classList.add("hidden")

        if(isAllItemHidden()){
            showNoContentText()
        }
    })
}

function isAllItemHidden(){
    var wishlistItemList = document.getElementsByClassName("wishlist-page-item")
    var hiddenItemCount = 0
    for(var i = 0; i < wishlistItemList.length; i++){
        if(wishlistItemList[i].classList.contains("hidden")){
            hiddenItemCount += 1
        }
    }
    
    return wishlistItemList.length == hiddenItemCount
}

function showNoContentText(){
    document.getElementById("wishlist-item-id-items").classList.add("hidden")
    document.getElementById("wishlist-item-id-no-content").classList.remove("hidden")
}