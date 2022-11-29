var wishItemButtons = document.getElementsByClassName('wish-list')
console.log('wishListButtons.length = ', wishItemButtons.length)
for(i = 0; i < wishItemButtons.length; i++){
    wishItemButtons[i].addEventListener('click', function(){
        var productId = this.dataset.product
        console.log("productId = " + productId)

        //for finding 'action', we have to get the clicked icon
        var addIcon = document.getElementById("add-btn-" + productId)
        var action = ""

        if(addIcon.classList.contains("hidden")){
            action = "remove"
        }else{
            action = "add"
        }

        console.log('productId:', productId, 'action:', action)

        console.log('USER: ', user)
        if(user == 'AnonymousUser'){
            alert('Login needed!')
        }else{
            updateWishListItem(productId, action)
        }
    })
}

function updateWishListItem(productId, action){
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
        var addIcon = document.getElementById("add-btn-" + productId)
        var removeIcon = document.getElementById("remove-btn-" + productId)

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