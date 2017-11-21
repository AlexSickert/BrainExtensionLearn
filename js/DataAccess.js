


function DataAccess() {


    /*
     * get the list of files and its download links for a specific id
     */
    this.ajaxPost = function (controller, request) {
        console.log("in ajax post");
        try {
            var r = request;
            var req = new AjaxRequest();
            req.onreadystatechange = function () {
                if (req.readyState === 4) {
                    try {
                        var resObj = JSON.parse(req.responseText);
                        controller.callBack(resObj);
                    } catch (x) {
                        console.log("Error in ajaxPost - onreadystatechange");
                        console.log(x);
                    }
                }
            };
            var obj = encodeURIComponent(JSON.stringify(r));
            req.open("POST", "ajaxPost", true);
            //req.open("POST", "objParameterArray", true);
            req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
//            req.send("objParameterArray=" + obj);
            req.send("objJSON=" + obj);
            return;
        } catch (x) {
            console.log("Error in BeDataAccess getFileList()");
            console.log(x);
        }
    };
}


// ========================================================

function AjaxRequest() {
    var http = false;
    try {
        http = new XMLHttpRequest();
    } catch (e1) {
        try {
            http = new ActiveXObject("Msxml2.xmlhttp");
        } catch (e2) {
            try {
                http = new ActiveXObject("Microsoft.xmlhttp");
            } catch (e3) {
                http = false;
            }
        }
    }
    return http;
}

/*
 * create the object that is being sent to server
 * JsonAddVocRequest(l, u, w, t, "adVocFromUrl");
 */
function JsonAddVocRequest(l, u, w, t, a) {
    this.language = l;  // module
    this.url = u; 
    this.word = w; 
    this.text = t; 
    this.action = a; 
}