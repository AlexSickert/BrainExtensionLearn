
function ajaxTranslateStart(e) {

    //ele.style.backgroundColor = "#ffeeee";

    var l = globalChoosenLanguage.toUpperCase();  // defind in html main page

    console.log("start translateThis()");

    var ls = "";

    if (l.includes("ITALIAN")) {
        ls = "IT";
    }

    if (l.includes("SPANISH")) {
        ls = "ES";
    }

    if (l.includes("PORTUGUESE")) {
        ls = "PT";
    }

    if (l.includes("RUSSIAN")) {
        ls = "RU";
    }

    if (l.includes("FRENCH")) {
        ls = "FR";
    }

    if (l.includes("ENGLISH")) {
        ls = "EN";
    }

    var o = new JsonTranslateVocRequest(ls, e);
    console.log("translateThis() - sending data via ajax");
    ajaxCallBackend(o);


}

// =============================================================================

function ajaxCallBackend(request) {
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
                    // call back in controller
                    Con.callBack(resObj); // defind in html main page
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
}
;

// =============================================================================

function getCookieValue(cname) {

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
}

function setCookieValue(cname, cvalue) {

    console.log("setCookieValue cname = " + cname);
    console.log("setCookieValue cvalue = " + cvalue);

    var d = new Date();
    d.setTime(d.getTime() + (999 * 24 * 60 * 60 * 1000));
    var expires = "expires=" + d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

// =============================================================================

function JsonTranslateVocRequest(l, w) {
    this.language = l;
    this.translationLanguage = "DE";
    this.word = w;
    this.translation = "";
    this.action = "translateRss";

}

function JsonReaderSaveTextRequest(s, l, u, t) {
    this.session = s;
    this.language = l; // module
    this.url = u;
    this.text = t;
    this.action = "readerSaveText";
}

function JsonReaderLoadTextTitlesRequest(s) {
    this.session = s;
    this.action = "readerLoadTextTitles";
}

function JsonReaderLoadOneTextRequest(s, id) {
    this.session = s;
    this.id = id;
    this.action = "readerLoadOneText";
}

function JsonReaderSetTextReadRequest(s, id) {
    this.session = s;
    this.id = id;
    this.action = "readerSetTextRead";
}

function JsonCheckSession(s) {
    this.action = "checkSession";
    this.session = s;
}


function JsonLogInRequest(u, p) {
    this.action = "logIn";
    this.user = u;
    this.password = p;
}


/*
 * create the object that is being sent to server
 * JsonAddVocRequest(l, u, w, t, "adVocFromUrl");
 */
function JsonAddVocRequest(l, w, tl, tw, s) {
    this.language = l; // module
    this.url = "";
    this.word = w;
    this.text = "";
    this.action = "adVocFromUrl";
    this.translationLanguage = tl;
    this.translationWord = tw;
    this.session = s;
}

// =============================================================================

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