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


document.getElementById("order-status").addEventListener("change", function(e){
    prepareChangingStatus(this.value, this, this.dataset.order)
})

function prepareChangingStatus(text, valueList, orderID){
    console.log("text = "+text+"  valueList = "+valueList+" orderID = "+orderID)
    var selectedIdx = getSelectedIndex(text, valueList)
    changeBackEndStatus(selectedIdx, orderID, valueList)
}

function changeBackEndStatus(selectedIdx, orderID, valueList){
    url = 'update-admin-order-status/'
    console.log("selectedIdx = "+selectedIdx+"  orderID = "+orderID)

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type' : 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            'orderID': orderID, 'statusIdx': selectedIdx 
        })
    })

    .then((response) => {
        return response.json()
    })

    .then((data)=>{
        console.log('data:', data)
        changeFrontEndStatus(selectedIdx, valueList)
    })
}

function changeFrontEndStatus(selectedIdx, valueList){
    for(var i=0; i<valueList.length; i++){
        if(i > selectedIdx){
            document.getElementById("track-"+valueList[i].text).classList.remove("completed")
        }else{
            document.getElementById("track-"+valueList[i].text).classList.add("completed")
        }
    }
}

function getSelectedIndex(text, valueList){
    for(var i = 0; i<valueList.length; i++){
        if(valueList[i].text == text){
            return i;
        }
    }
}


var updateBtns = document.getElementsByClassName('update-admin-order-item')
console.log('updateBtns.length = ', updateBtns.length)

for(i = 0; i < updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function(){
        var itemId = this.dataset.item 
        var action = this.dataset.action
        console.log('itemId:', itemId, 'action:', action)
        updateAdminOrderItem(itemId, action)
    })
}

function updateAdminOrderItem(itemId, action){
    var quantity = getItemQuantity(itemId)
    if(quantity <= 1 && action == "remove"){
        alert("Quantity has to be more than 0")
        return;
    }

    url = 'update-admin-order-item/'

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


var removeBtns = document.getElementsByClassName('rmv-admin-order-item-btn')
console.log('removeBtns.length = ', removeBtns.length)

for(i = 0; i < removeBtns.length; i++){
    removeBtns[i].addEventListener('click', function(){
        var itemId = this.dataset.item 
        var itemCount = this.dataset.itemcnt
        console.log('itemId:', itemId, 'itemCount:', itemCount)
        removeAdminOrderItem(itemId, itemCount)
    })
}

function removeAdminOrderItem(itemId, itemCount){
    if(itemCount <= 1){
        alert("Order items count has to be more than 0!")
        return;
    }

    url = 'remove-admin-order-item/'

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


document.getElementById("btn-add-all").addEventListener("click", function(e){
    var productCheckBoxes = document.getElementsByClassName("add-item-admin-order")
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
    addProductListIntoOrder(checkedProductIdList)
})

function addProductListIntoOrder(checkedProductIdList){
    if(checkedProductIdList.length == 0){
        alert("No item selected!")
        return;
    }

    url = 'add-admin-order-items/'

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