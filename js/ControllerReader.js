
function Controller() {

    var objUxUi;

    this.setUxUi = function (x) {
        objUxUi = x;
    };


    /* main handling of flow of screena dn logic of the app - without using the data
     access object  */


    this.init = function () {
        /**
         * This function gets called first to setup the initla screen
         */

        // ToDo: handle session validation and login etc. 

        // check if valid session and if not then login


        console.log("in Controller() function init()");
        //objUxUi.setScreen(1, 0);

        this.checkForLogin();
    };


    /*
     * function to initialize check if we have a valid session
     * depending on that we show a login form or not
     */
    this.checkForLogin = function () {

        // getCookieValue
        var s = getCookieValue("session");

        if (s.length < 2) {
            console.log("session sting empty, therefore showing login form");
            // this means we have no session at all and can shot the login
            //UxUi.setLoginForm("Please log in.");
            objUxUi.setScreen(0, 0);
        } else {
            console.log("session string is: " + s);
            // check if the session is valid.
            var r = new JsonCheckSession(s);
            ajaxCallBackend(r);
        }
        return;
    };


    this.login = function () {

        console.log("in Controller() function login()");
        var u = document.getElementById("user").value;
        var p = document.getElementById("pw").value;
        var r = new JsonLogInRequest(u, p);
        ajaxCallBackend(r);
    };

    this.logout = function () {
        console.log("in Controller() function logout()");
    };

    this.translateWord = function () {
        globalTranslateWhat = "word";
        e = document.getElementById("word").value;
        ajaxTranslateStart(e);
    };

    this.translateSentence = function () {
        globalTranslateWhat = "sentence";
        e = document.getElementById("sentence").value;
        ajaxTranslateStart(e);
    };

    this.saveTranslation = function () {
        var s = getCookieValue("session");
        var sw = "";
        var tl = "DE";

        if (globalTranslateWhat === "sentence") {
            sw = document.getElementById("sentence").value;
        } else {
            sw = document.getElementById("word").value;
        }

        // restult of translation
        var res = document.getElementById("result").value;
        var obj = new JsonAddVocRequest(globalChoosenLanguage, sw, tl, res, s);
        ajaxCallBackend(obj);
    };


    this.saveText = function () {
        var s = getCookieValue("session");
        console.log("this.saveText, session is: " + s);
        var obj = new JsonReaderSaveTextRequest(s, globalChoosenLanguage, "url", globalCurrentText);
        ajaxCallBackend(obj);
    };

    this.loadTextList = function () {
        var s = getCookieValue("session");
        console.log("this.loadTextList, session is: " + s);
        var obj = new JsonReaderLoadTextTitlesRequest(s);
        ajaxCallBackend(obj);
    };

    this.loadText = function (id, language) {
        globalChoosenLanguage = language;
        var s = getCookieValue("session");
        console.log("this.loadText, session is: " + s);
        var obj = new JsonReaderLoadOneTextRequest(s, id);
        ajaxCallBackend(obj);
    };

    this.setTextRead = function () {
        // globalCurrentTextId
        var s = getCookieValue("session");
        console.log("this.setTextRead, session is: " + s);
        console.log("this.setTextRead, globalCurrentTextId: " + globalCurrentTextId);
        var obj = new JsonReaderSetTextReadRequest(s, globalCurrentTextId);
        ajaxCallBackend(obj);
    };



    // =============================================================================

    this.callBack = function (obj) {

        if (obj["action"] === "translateRss") {
            //obj["translation"]
            document.getElementById("result").value = obj["translation"];
        }

        if (obj["action"] === "readerSaveText") {
            console.log("readerSaveText callback");
            globalCurrentTextId = obj["text_id"]; // to be able to set the text read
            objUxUi.toast("Saved text");
        }

        if (obj["action"] === "readerLoadTextTitles") {
            console.log("readerLoadTextTitles");
            objUxUi.setScreen(8, obj["titles"]);
        }

        if (obj["action"] === "readerLoadOneText") {
            console.log("readerLoadOneText");
            console.log(obj["text"]);
            // set id of current reading text            
            globalCurrentTextId = obj["text_id"];
            objUxUi.convertSavedText(obj["text"]);
        }

        if (obj["action"] === "readerSetTextRead") {
            console.log("readerSetTextRead");
            objUxUi.toast("Set the text as 'read'");
        }


        if (obj["action"] === "checkSession") {
            // if session valid then we can start the application
            // otherwise we go to login form
            var check = obj["sessionValid"];
            if (check) {
                // session valid - go to main screen
                objUxUi.setScreen(1, 0);

            } else {
                // need to login to get a session
                objUxUi.setScreen(0, 0);
            }
        }

        if (obj["action"] === "logIn") {
            var success = obj["success"];
            if (success) {
                console.log("login success");
                globalSession = obj["session"];
                this.setCookie("session", globalSession);
                console.log("loading app");
                //objUxUi.setNavi("");
                objUxUi.setScreen(1, 0);
            } else {
                console.log("login failed");
                //objUxUi.setLoginForm("Login failed. Please try again or reset password. If you are not registered, please register - it's free.");
                objUxUi.setScreen(0, 0);
            }
        }

        if (obj["action"] === "adVocFromUrl") {
            objUxUi.toast(JSON.stringify(obj));
        }
    };
}