function DataAccess() {

    /*
     * get the list of files and its download links for a specific id
     */
    this.ajaxPost = function (controller, request) {
        console.log("in ajax post");

        console.log("----------- JSON object ajaxPost --------------");
        console.log(JSON.stringify(request));
        console.log("-----------------------------------------------");

        try {
            var r = request;
            var req = new AjaxRequest();
            req.onreadystatechange = function () {
                if (req.readyState === 4) {
                    try {
                        console.log("---------- ajaxPost result ---------------");
                        console.log(req.responseText);
                        console.log("------------------------------------------");
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


    this.ajaxPostJson = function (con, endpoint, json) {


        var req = new AjaxRequest();

        console.log("----------- JSON object in ajaxPostJson--------------");
        console.log(JSON.stringify(json));
        console.log("-----------------------------------------------------");


        req.onreadystatechange = function () {
            if (req.readyState === 4) {
                try {
                    console.log(req.responseText);
                    var resObj = JSON.parse(req.responseText);
                    con.callBack(resObj);
                } catch (x) {
                    console.log("Error in DataAccess ajaxPost() - onreadystatechange");
                    console.log(x);
                }
            }
        };
        //var obj = encodeURIComponent(JSON.stringify(json));
        var obj = JSON.stringify(json);
        req.open("POST", endpoint, true);
        //req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        req.setRequestHeader("Content-type", "application/json");
        req.send(obj);
        return;

    };

    this.getCookieValue = function (cname) {

        console.log("getCookieValue cname = " + cname);
        console.log("getCookieValue content = " + document.cookie);

        var name = cname + "=";
        var decodedCookie = decodeURIComponent(document.cookie);
        var ca = decodedCookie.split(';');
        for (var i = 0; i < ca.length; i++) {
            var c = ca[i];
            while (c.charAt(0) == ' ') {
                c = c.substring(1);
            }
            if (c.indexOf(name) == 0) {
                return c.substring(name.length, c.length);
            }
        }
        return "";
    };

    this.setCookieValue = function (cname, cvalue) {

        console.log("setCookieValue cname = " + cname);
        console.log("setCookieValue cvalue = " + cvalue);

        var d = new Date();
        d.setTime(d.getTime() + (999 * 24 * 60 * 60 * 1000));
        var expires = "expires=" + d.toUTCString();
        document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
    };
} // end of class


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
function JsonAddVocRequest(l, u, w, t, a, tl, tw, s) {
    this.language = l; // module
    this.url = u;
    this.word = w;
    this.text = t;
    this.action = a;
    this.translationLanguage = tl;
    this.translationWord = tw;
    this.session = s;
}

function JsonBulkAddVocRequest(t, s) {
    // used to upload tab separated tables copy/pasted from spreadsheet
    this.text = t;
    this.action = "bulkAddVoc";
    this.session = s;
}


function JsonTranslateVocRequest(l, w, tl, s) {
    this.language = l;
    this.translationLanguage = tl;
    this.word = w;
    this.translation = "";
    this.action = "translateWord";
    this.session = s;
}

function JsonLoadWordRequest(answer, wordId, sess) {
    this.action = "loadWord";
    this.answer = answer;
    this.wordId = wordId;
    this.session = sess;
}

function JsonLoadWordArrayRequest(answer, wordId, sess) {
    this.action = "loadWordArray";
    this.answer = answer;
    this.wordId = wordId;
    this.session = sess;
}


function JsonEditWordRequest(wordId, fromWord, toWord, sess) {
    this.action = "editWord";
    this.fromWord = fromWord;
    this.toWord = toWord;
    this.wordId = wordId;
    this.session = sess;
}


function JsonCheckSession(s) {
    this.action = "checkSession";
    this.session = s;
}

function JsonReportRequest(s) {
    this.action = "report";
    this.session = s;
}

function JsonStaticContentRequest(c) {
    this.action = c;
}

function JsonLogInRequest(u, p) {
    this.action = "logIn";
    this.user = u;
    this.password = p;
}

function JsonRegisterRequest(u) {
    this.action = "registerUser";
    this.user = u;
}

function JsonResetRequest(u) {
    this.action = "resetPassword";
    this.user = u;
}

function JsonGetLanguages(s) {
    this.action = "getLanguages";
    this.session = s;
}

function JsonGetSettings(s) {
    this.action = "getSettings";
    this.session = s;
}

function JsonSetSettings(s, data) {
    this.action = "setSettings";
    this.session = s;
    this.settings = data;
}
