var csrftoken = getToken('csrftoken');
function getToken(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


var updateBtns = document.getElementsByClassName('update-admin-cart-item')
console.log('updateBtns.length = ', updateBtns.length)

for(i = 0; i < updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function(){
        var itemId = this.dataset.item 
        var action = this.dataset.action
        console.log('itemId:', itemId, 'action:', action)
        updateAdminCartItem(itemId, action)
    })
}


function updateAdminCartItem(itemId, action){
    var quantity = getItemQuantity(itemId)
    if(quantity <= 1 && action == "remove"){
        alert("Quantity has to be more than 0")
        return;
    }

    url = 'update-admin-cart-item/'

    // var form = document.getElementById('form')
    // var csrftoken = form.getElementsByTagName('input')[0].value

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type' : 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            'itemId': itemId, 'action': action 
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

function getItemQuantity(itemId){
    var qtyText = document.getElementById("quantity-"+itemId).textContent
    return parseInt(qtyText)
}


var removeBtns = document.getElementsByClassName('rmv-admin-cart-item-btn')
console.log('removeBtns.length = ', removeBtns.length)

for(i = 0; i < removeBtns.length; i++){
    removeBtns[i].addEventListener('click', function(){
        var itemId = this.dataset.item 
        var itemCount = this.dataset.itemcnt
        console.log('itemId:', itemId, 'itemCount:', itemCount)
        removeAdminCartItem(itemId, itemCount)
    })
}


function removeAdminCartItem(itemId, itemCount){
    url = 'remove-admin-cart-item/'
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type' : 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            'itemId': itemId
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


var addAllBtn = document.getElementById("btn-add-all")
if(addAllBtn != null){
    addAllBtn.addEventListener("click", function(e){
        var productCheckBoxes = document.getElementsByClassName("add-item-admin-cart")
        var checkedProductIdList = []
        var j = 0

        for(var checkBox of productCheckBoxes){
            if(checkBox.checked){
                console.log("checkbox.checked....  checkbox.value = "+checkBox.value+";")
                checkedProductIdList[j++] = parseInt(checkBox.value)
            }
        }

        console.log("checkedItemIdList.length="+checkedProductIdList.length+";   productCheckBoxes.length = "+productCheckBoxes.length)

        clearCheckBoxes(productCheckBoxes)
        addProductListIntoCart(checkedProductIdList)
    })
}

function addProductListIntoCart(checkedProductIdList){
    if(checkedProductIdList.length == 0){
        alert("No item selected!")
        return;
    }

    url = 'add-admin-cart-items/'

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type' : 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            'productIdList': checkedProductIdList
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

function clearCheckBoxes(productCheckBoxes){
    for(var checkBox of productCheckBoxes){
        checkBox.checked = false;
    }
}