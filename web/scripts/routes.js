// scripts

// allow python to reload the page after changing the markup
eel.expose(reload_page);
function reload_page() {
    location.reload();
}

// used to check for existence of a specific attribute
function attributeExists(data, attr) {
	if (typeof data[attr] !== 'undefined') {
  	    return true
	} else {
  	    return false
    }
}

function processRequest(data, e) {
    let time = new Date();
    let expire_time = sessionStorage.getItem('expires');
    // verify the user's session isn't expired
    if (time.getTime() > expire_time.getTime()) {
        // verify the request has a route
        if (typeof data['args']['target'] !== 'undefined') {
            // prevent default behavior
            e.preventDefault();
            // call python behavior
            eel.process_request(data);
        } // otherwise we want to allow the normal behavior to continue
    } else {
        // if the session is expired, prompt the user to log in
        console.log('you need to log in...')
    }
}

// catch the click of a link
$('.link').click(function(e) {
    let data = new Object;
    data['args'] = $(this).data();
    data['args']['session_token'] = sessionStorage.getItem('session-token');
    data['args']['user_id'] = sessionStorage.getItem('user-id');
    processRequest(data, e);
})

eel.expose(loginSuccessful)
function loginSuccessful(session_token, user_id) {
    // create new datetime
    let expire_time = new Date();
    let time = expire_time.getTime();
    // +30 min for client
    time += 3600 * 500;
    expire_time.setTime(time);
    // set the cookie for the session token, user id and expiry time 
    // (to be checked by client and reset with successful requests)
    sessionStorage.setItem('session-token', session_token);
    sessionStorage.setItem('expires', expire_time.toGMTString());
    sessionStorage.setItem('user-id', user_id);
}

// handle a specific form or something
$('#login').submit(function(e) {

    let data = new Object;

    // add all of the arguments from the form
    data['args']['form_values'] = {};
    let form_data = $(this).serializeArray();
    for (let i = 0; i < form_data.length; i++) {
        data['args']['form_values'][form_data[i]['name']] = form_data[i]['value'];
    }

    // add any data arguments from the form
    data['args'] = $(this).data();
    data['args']['session_token'] = sessionStorage.getItem('session-token');
    data['args']['user_id'] = sessionStorage.getItem('user-id');

    processRequest(data, e);
    
});
