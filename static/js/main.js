function dataSend() {
    const csrfToken = getCookie('csrftoken');
    // console.log(csrfToken)
    var filterList = [];
    var query = document.getElementById("filter");
    var prodData = ""
    console.log("Token", csrfToken)
    var fdata = query.getElementsByTagName("input");
    /*console.log("Data :",data[0].value)*/
    for (let i = 0; i < fdata.length; i++) {
        if (fdata[i].checked == true) {

            console.log("Data", i, fdata[i].value)
            filterList.push(fdata[i].value)
        }
    }
    url = '/home/';
    fetch(url, {
        method: 'POST',
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken,
        },
        body: JSON.stringify({ 'filterQ': filterList }),
    })
        .then(response => {
            if (response.ok) {
                console.log("Data send : ", response);
                return response.json(); // Return the JSON data here
            }
            else {
                console.log("Error occurred");
                throw new Error("Error occurred"); // You can throw an error here if needed
            }
        })




};

function CookieUpdate(prod_id, method) {
    var guestCookie = getCookie('GuestUserCart');
    var present = false;
    // applying method on data
    var cookieArr = guestCookie.split("+");
    console.log("Array", cookieArr);
    if (guestCookie != "$") {
        for (var i = 0; i < cookieArr.length; i++) {
            // console.log(JSON.parse(cookieArr[i]))
            var check = JSON.parse(cookieArr[i]);


            // check if the product Id exist 
            if (check["id"] === prod_id && check["quantity"] > 0) {
                if (method == "add") {
                    check['quantity'] += 1;
                    console.log("Add");
                }
                else {
                    check['quantity'] -= 1;
                    console.log("Remove");
                }
                if (check["quantity"] <= 0) {
                    cookieArr.splice(i, 1)
                }
                else {
                    data = JSON.stringify(check);
                    cookieArr[i] = data;
                }
                present = true;
                break;
            }

        }
    }
    // create first dict
    if (present == false && method == "add") {
        cart = { "id": 0, "quantity": 0 };
        cart['id'] = prod_id;
        cart['quantity'] = 1;
        console.log("New Dict :", cart);
        data = JSON.stringify(cart);
        cookieArr.push(data)
    }
    console.log("Cookie list :", guestCookie)
    if (guestCookie === "$") {
        guestCart = data
    }
    else {
        if (cookieArr.length === 1) {
            guestCart = cookieArr
        }
        else {
            guestCart = cookieArr.join("+")

        }
    }
    document.cookie = 'GuestUserCart' + '=' + guestCart + '; path=/';
    window.location.reload();
};

function getCookie(name) {
    // finding cookie 
    var Gcookie = document.cookie.split(';');

    for (var i = 0; i < Gcookie.length; i++) {
        var cookieArr = Gcookie[i].split('=');


        if (cookieArr[0].trim() == name) {

            var guest = cookieArr[1];
            console.log("getcookie", guest)
            return guest
        }
        // console.loÍg(cookie)
    }
    return null;
};

function formSubmit() {
    var  order_items = document.getElementById("total_item").innerHTML;
    var user = document.getElementById('name').value;
    console.log("Items",order_items);
    
    if (user == "Username") {
        console.log("User :", user);
        alert("You need to Login before Checkout", "Login and continue cart")
        window.location.href = '/signup/';
    }
    else if(order_items ==0){
        alert("**** No Item for order ****");
        window.location.reload();
    }
    else {

        console.log("User :", user)
        var form = {
            "address": null ,
            "city": null ,
            "state": null ,
            "pincode":null 
        };
        form['address'] = document.getElementById("address").value;
        form['city'] = document.getElementById("city").value;
        form['state'] = document.getElementById("state").value;
        form['pincode'] = document.getElementById("pincode").value;

        if (
            form['address'] &&
            form['city'] &&
            form['state'] &&
            form['pincode']
        ) {
            // All fields have values, proceed with your logic here
            console.log("All fields are filled. Proceeding...");
        } else {
            // Not all fields have values, display an error message or take appropriate action
            alert("Please fill in all fields.");
            return
        }
        var url = '/processorder/'
        fetch(url, {
            method: 'POST', // HTTP method (e.g., GET, POST, PUT, DELETE)
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
                // Other headers can be added here
            },
            body: JSON.stringify({ "PaymentForm": form })
        })
            .then((response) => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                console.log("Form Successful");
                console.log("Response :", response);
            });
        console.log(form)
        
       
        document.getElementById('form-button').classList.add("invisible");
        alert("Form Submited Successfull!");
        document.getElementById('Payment-info').classList.remove("invisible");
        // window.location.href = '/processorder/';
    }

};


