

let user_signed_in = false;
let preview_state = true;
const CLIENT_ID = encodeURIComponent('526064511697-g8ehfcclqnbar3uqgq44uq55d07aflsn.apps.googleusercontent.com');
const RESPONSE_TYPE = encodeURIComponent('id_token');
const REDIRECT_URI = encodeURIComponent('https://keffbblkhabiogfmcpmgddlfimhpooah.chromiumapp.org');
const STATE = encodeURIComponent('meet' + Math.random().toString(36).substring(2, 15));
const SCOPE = encodeURIComponent('openid');
const PROMPT = encodeURIComponent('consent');


function create_oauth2_url() {
    let nonce = encodeURIComponent(Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15))

    let url =
        `https://accounts.google.com/o/oauth2/v2/auth
?client_id=${CLIENT_ID}
&response_type=${RESPONSE_TYPE}
&redirect_uri=${REDIRECT_URI}
&scope=${SCOPE}
&state=${STATE}
&nonce=${nonce}
&prompt=${PROMPT}`;

    console.log(url);
    return (url);
}


function is_user_signed_in() {
    return user_signed_in;
}

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.message == "login") {
        let is_user_signed_in = false;
        if (is_user_signed_in) {
            console.log("User is already signed in")
        } else {

            //SIGN IN HERE

            chrome.identity.launchWebAuthFlow({
                url: create_oauth2_url(),
                interactive: true
            }, function (redirect_url) {

                let id_token = redirect_url.substring(redirect_url.indexOf('id_token=') + 9);
                id_token = id_token.substring(0, id_token.indexOf('&'));

                user_signed_in = true;

                sendResponse('success');
            });
            return true;
        }

    } else if (request.message == "logout") {

        //SIGN OUT

        user_signed_in = false;
        return true;
    }
})

chrome.commands.onCommand.addListener((command) => {
    if (command == 'Fill') {
        if (preview_state) {
            // TODO: CALL PREIVEW LINK
            chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {

                // since only one tab should be active and in the current window at once
                // the return variable should only have one entry
                var activeTab = tabs[0];
                activeTab = activeTab.url;
                var tabURL = activeTab.split('/');
                console.log(tabURL[5]);
                //request_url('http://localhost:5000//api/preview-autocomplete?document_id=' + tabURL[5])
                fetch('http://127.0.0.1:5000/api/preview-autocomplete?document_id=' + tabURL[5])
            });
        } else {
            // TODO: CONFIRM AUTO COMPLETE
        }
    }
})

function request_url(requested_URL) {

}



/**
 *     if (request.message == "login"){
        let is_user_signed_in = false;
        if(is_user_signed_in){
            console.log("User is already signed in")
        } else {

            //SIGN IN HERE

            chrome.identity.launchWebAuthFlow({
                url: create_oauth2_url(),
                interactive: true
            }, function(redirect_url){

                let id_token = redirect_url.substring(redirect_url.indexOf('id_token=')+9);
                id_token = id_token.substring(0, id_token.indexOf('&'));

                user_signed_in = true;

                sendResponse('success');
            });
            return true;
        }

    } else if (request.message == "logout"){

        //SIGN OUT
        
        user_signed_in = false;
        return true;
    }
 */