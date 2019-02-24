/*



 */



function Controller() {

  var objDataAccess = new DataAccess();
  var objUxUi;
  var settings;

  this.wordArray = [];

  /*
   * this function runs when the html page loads initially
   */
  this.init = function(uxui) {

    // set navigation and main body area
    objUxUi = uxui;

    //objUxUi.setNavi("");
    //objUxUi.setLearnForm();

    objUxUi.hideDiv("mobilePortrait");
    objUxUi.hideDiv("mobileLandscape");
    objUxUi.hideDiv("desktop");

    this.checkForLogin();

    return;
  };


  /*
   * function to initialize check if we have a valid session
   * depending on that we show a login form or not
   */
  this.checkForLogin = function() {

    // getCookieValue
    var s = this.getCookie("session")

    if (s.length < 2) {
      console.log("session sting empty, therefore showing login form");
      // this means we have no session at all and can shot the login
      objUxUi.setLoginForm("Please log in.");
    } else {
      // check if the session is valid.
      var r = new JsonCheckSession(s);
      objDataAccess.ajaxPost(this, r);
    }
    return;
  };

  /*
   * to log out from app
   */

  this.logOut = function() {
    globalVisibleScreen = 0;
    this.setCookie("session", "");
    globalSession = "";
    objUxUi.hideTrainingUi();
    objUxUi.showDiv("mainNavi");
    objUxUi.showDiv("mainBody");
    objUxUi.setNavi("edit");  // ToDo this is not correct
    objUxUi.setLoginForm("Please log in.");
    return;
  };

  /*
   * function to register a new user
   */
  this.register = function() {

    globalVisibleScreen = 0;

    var user = objUxUi.getValue("user");

    if (this.validateEmail(user)) {
      var r = new JsonRegisterRequest(user);
      objDataAccess.ajaxPost(this, r);
    } else {
      alert("Not a valid email address. Please try again.");
    }
    return;
  };

  /*
   * function to register a new user
   */
  this.resetPassword = function() {

    globalVisibleScreen = 0;

    var user = objUxUi.getValue("user");

    // ToDo: make here a proper email check
    if (this.validateEmail(user)) {
      var r = new JsonResetRequest(user);
      objDataAccess.ajaxPost(this, r);
    } else {
      alert("Not a valid email address. Please try again.");
    }
    return;
  };

  /*
   * gets called by Uxui when user logs in
   */
  this.logIn = function(uxui) {
    globalVisibleScreen = 0;
    console.log("controller logIn()");
    var user = objUxUi.getValue("user");

    if (this.validateEmail(user)) {
      var password = objUxUi.getValue("password");
      var r = new JsonLogInRequest(user, password);
      console.log("controller logIn() - request object created");
      objDataAccess.ajaxPost(this, r);
    } else {
      alert("Not a valid email address. Please try again.");
    }
  }

  this.gotLoginForm = function() {
    globalVisibleScreen = 0;
    objUxUi.setLoginForm("Please log in.");
  }

  this.gotResetForm = function() {
    globalVisibleScreen = 0;
    objUxUi.setPasswordResetForm("Please enter the email address you are registered with.");
  }

  this.gotRegistrationForm = function() {
    globalVisibleScreen = 0;
    objUxUi.setRegistrationForm("Please enter a valid email address to register. The login password will be sent to this email address.");
  }


  this.saveEditVoc = function() {
    //  globalWordId
    //objUxUi.makeToast("controller saveEditVoc", true);
    objUxUi.globalVisibleScreen = 2;
    var fromWord = document.getElementById("editFromWord").value;
    var toWord = document.getElementById("editToWord").value;
    var s = this.getCookie("session");
    var r = new JsonEditWordRequest(globalWordId, fromWord, toWord, s);
    //objDataAccess.ajaxPostJson(this, "json", r);
    objDataAccess.ajaxPost(this, r);

  }


  //===================================================


  this.testJson = function() {
    var r = new JsonAddVocRequest("ldghfg", "udfghdfg", "wdfghdfgh", "tdfhf", "testJson");
    objDataAccess.ajaxPostJson(this, "json", r);
  }

  //===================================================
  // function to handle Ui Interaction

  this.setEditForm = function() {
    globalVisibleScreen = 2;
    // hide the training html decoded
    objUxUi.hideTrainingUi();
    objUxUi.showDiv("mainNavi");
    objUxUi.showDiv("mainBody");
    objUxUi.setNavi("edit");
    objUxUi.setEditVocForm();
    return;
  };


  this.setAddVocForm = function() {
    globalVisibleScreen = 0;
    // hide the training html decoded
    objUxUi.hideTrainingUi();
    objUxUi.showDiv("mainNavi");
    objUxUi.showDiv("mainBody");
    objUxUi.setNavi("add");
    objUxUi.setAddVocForm();
    // add value form cookies
    //objUxUi.setValue("adVocLanguage", this.getCookie("adVocLanguage"));
    //objUxUi.setValue("adVocTranslationLanguage", this.getCookie("adVocTranslationLanguage"));
    return;
  };




  this.setLearnForm = function() {
    globalVisibleScreen = 1;
    objUxUi.setNavi("learn");
    objUxUi.setLearnForm();
    // now load a word from the array
    this.nextWordFromArray(true);
    return;
  };

  this.setSettingsForm = function() {
    objUxUi.setNavi("settings");
    objUxUi.setSettingsForm();
    return;
  };

  // this is to show the report about progress
  this.setResultsForm = function() {
    globalVisibleScreen = 0;
    objUxUi.hideTrainingUi();
    objUxUi.showDiv("mainNavi");
    objUxUi.showDiv("mainBody");
    objUxUi.setNavi("results");
    objUxUi.setLoading();
    var s = this.getCookie("session");
    var r = new JsonReportRequest(s);
    objDataAccess.ajaxPost(this, r);
    return;
  };

  // load static content without session - like fax, terms, privacy...
  this.setStaticContentForm = function(s) {
    globalVisibleScreen = 0;
    objUxUi.hideTrainingUi();
    objUxUi.showDiv("mainNavi");
    objUxUi.showDiv("mainBody");
    objUxUi.setNavi("more");
    objUxUi.setLoading();
    objUxUi.setStaticContentForm("Content loading...");
    var r = new JsonStaticContentRequest(s);
    objDataAccess.ajaxPost(this, r);
    return;
  };



  this.setMoreForm = function() {
    globalVisibleScreen = 0;
    objUxUi.hideTrainingUi();
    objUxUi.showDiv("mainNavi");
    objUxUi.showDiv("mainBody");
    objUxUi.setNavi("more");
    objUxUi.setMoreForm();
    return;
  };

  /*
   * loads a given url and its language from web and ads it to database
   */
  this.saveAddVoc = function() {
    var l = objUxUi.getValue("adVocLanguage");
    var u = ""; //objUxUi.getValue("adVocUrl");
    var w = objUxUi.getValue("adVocWord");
    var t = ""; //objUxUi.getValue("adVocText");
    var tl = objUxUi.getValue("adVocTranslationLanguage");
    var tw = objUxUi.getValue("adVocTranslationWord");

    // save in cookie
    this.setCookie("adVocLanguage", l);
    this.setCookie("adVocTranslationLanguage", tl);


    objUxUi.setAddVocFormMessage("processing...");

    console.log("adVocLanguage = " + l);
    console.log("adVocUrl = " + u);
    console.log("adVocWord = " + w);
    console.log("adVocText = " + t);

    var s = this.getCookie("session");
    var r = new JsonAddVocRequest(l, u, w, t, "adVocFromUrl", tl, tw, s);
    objDataAccess.ajaxPost(this, r);
  };

  this.translateAddVoc = function() {
    var l = objUxUi.getValue("adVocLanguage");
    var u = ""; //objUxUi.getValue("adVocUrl");
    var w = objUxUi.getValue("adVocWord");
    var t = ""; //objUxUi.getValue("adVocText");
    var tl = objUxUi.getValue("adVocTranslationLanguage");
    var tw = objUxUi.getValue("adVocTranslationWord");

    // save in cookie
    this.setCookie("adVocLanguage", l);
    this.setCookie("adVocTranslationLanguage", tl);

    //objUxUi.setAddVocFormMessage("processing...");

    console.log("adVocLanguage = " + l);
    console.log("adVocWord = " + w);
    console.log("adVocTranslationLanguage = " + tl);

    var s = this.getCookie("session");
    var r = new JsonTranslateVocRequest(l, w, tl, s);
    objDataAccess.ajaxPost(this, r);
  };



   // function to process the bulk upload via copy/paste from Excel
  this.saveVocBulkCopyPaste = function() {

    var tab = objUxUi.getValue("adVocBulkCopyPaste");

    objUxUi.setAddVocFormMessage("processing...");

    // we need to ensure we have consistent table structure and values
    tab = tab.replace("\n\r", "\n");
    tab = tab.replace("\r\n", "\n");

    rows = tab.split("\n");

    var arrayLength = rows.length;
    console.log("rows: " + arrayLength);
    for (var i = 0; i < arrayLength; i++) {
        if(rows[i].length > 1){
            fields = rows[i].split("\t");
            //Do something
            console.log("fields: " + fields.length);

            var fieldsLength = fields.length;
            for (var k = 0; k < fieldsLength; k++) {
                field = fields[k];
                console.log("field = " + field.length);
            }
        }

    }

    // by now we need to be sure that values are OK and we can process on backend
    var s = this.getCookie("session");
    var r = new JsonBulkAddVocRequest(tab, s);
    objDataAccess.ajaxPost(this, r);


    return;
  };


  // handle cookies

  this.setCookie = function(key, value) {
    console.log("setCookie key = " + key);
    console.log("setCookie value = " + value);
    objDataAccess.setCookieValue(key, value);
  };

  this.getCookie = function(key) {
    return objDataAccess.getCookieValue(key);
  };

  //============================================================================
  // Function to handle the interaction from the training Gui

  this.answerYes = function(answer) {
    var s = this.getCookie("session");
    //var r = new JsonLoadWordRequest("YES", globalWordId, s);
    var r = new JsonLoadWordArrayRequest("YES", globalWordId, s);
    objUxUi.setLearnFormValues("...", "...", "...", "...");
    objUxUi.showHiddenWord();
    this.nextWordFromArray(true);
    objDataAccess.ajaxPost(this, r);
  }

  this.answerNo = function(answer) {
    var s = this.getCookie("session");
    //var r = new JsonLoadWordRequest("NO", globalWordId, s);
    var r = new JsonLoadWordArrayRequest("NO", globalWordId, s);
    objUxUi.setLearnFormValues("...", "...", "...", "...");
    objUxUi.showHiddenWord();
    this.nextWordFromArray(false);
    objDataAccess.ajaxPost(this, r);
  }


  this.getGoodRandomId = function(){

    if (this.wordArray.length > 0){

        var len = this.wordArray.length;
        // globalWordId
        // it can be that while ajax is executing the sort order and content of array changed
        for(i = 0; i < len; i++){
            if(this.wordArray[i]["wordId"] == globalWordId){
                globalWordIdIndex = i;
            }
        }


        if (this.wordArray.length > 1){

            var found = false;


            while (found == false){

                candidateId = Math.round(Math.random() * (len - 1));

                if(candidateId != globalWordIdIndex){
                    found = true;
                }
            }

            return candidateId;

        }else{
            return 0;
        }
    }else{
        return 0;
    }
  }

  this.debugArray = function(arr, info){

    console.log("------------ " + info + " ------------------");

    var arrayLength = arr.length;
    var ele = "";

    console.log(arrayLength)

    for (var i = 0; i < arrayLength; i++) {
        //console.log(i);
        //console.log(arr);
        ele = arr[i];
        //console.log(arr);
        console.log(ele);

    }
    console.log("------------------------------");

  }

  this.reOrderArray = function(answer){

    /*

    as the array might get replaced we need to check what index the just processed word has. if the word cannot be found
    then we do not change anything in the array.

    */

    var arrayLength = this.wordArray.length;
    var currIndex = -1;

    // find the index of the word we just tested
    for (var i = 0; i < arrayLength; i++) {
        if(this.wordArray[i]["wordId"] == globalWordId){
            currIndex = i;
        };
    }

    if(currIndex >= 0){  // we process only if the current array has the word

     // we know that each array element has always a value "position"

        p = this.wordArray[currIndex]["position"];  // the element we just looked at

        console.log("wordId processing " + this.wordArray[currIndex]["wordId"]);

        this.debugArray(this.wordArray, "before");

        console.log("position is now " + p);

        if(answer){
            console.log("answer is YES");
            // speed up with pushing backwards when the anser is yes
            if (p < 5){
                p = p + 2;
            }else{
                p = p +1; // shift position one step backward
            }

        }else{
             console.log("answer is NO");
             if( p > 2){
                // p = Math.round( p/2 );  // no answer causes distance from start to get reduced 50%
                p = p - 2;
             }
        }

        console.log("new position: " + p);

        // adjust the target position of the word just tested
        this.wordArray[currIndex]["position"] = p;

        this.debugArray(this.wordArray, "new position");

        arrayLength = this.wordArray.length;

        var arr_new = [];
        // we start with 1 and not 0 because we push this element later

        for (var i = 0; i < arrayLength; i++) {

            // insert the word at the new position
            // the rest of the array stays unchanged
            if(i == p){
                arr_new.push(this.wordArray[currIndex])
            }else{
                if(this.wordArray[i]["wordId"] != this.wordArray[currIndex]["wordId"]){
                    arr_new.push(this.wordArray[i]);
                }
            }
        }

        // if p is larger than array index
        if(p >= arrayLength){
            arr_new.push(this.wordArray[currIndex]);
        }

        this.wordArray = arr_new;
        this.debugArray(this.wordArray, "rearranged array");
    }
  }

  /*

  We create something similar to a exponential distribution to prevent that we too often chose the same words and
  some words further down the array show up too seldom

  */
  this.chooseNextWordFromArrayByDistribution = function(){

    // get array length

    // get random number

    // if < 0.6 then 1, < 0.9 2, else 3

    // l = array length
    // bucketSize = l/3
    // min =  (bucket - 1) *  bucketSize
    // max = bucket * bucketSize

    // random integer within range like here https://stackoverflow.com/questions/1527803/generating-random-whole-numbers-in-javascript-in-a-specific-range

    // make sure it is not equal to globalWordId, otherwise get other random od this bucket

  }

  // from the array we immediately load the next word and don't wait for the callback
  this.nextWordFromArray = function(answer){

    console.log("this.nextWordFromArray() this.wordArray.length = " + this.wordArray.length);

    if (this.wordArray.length > 0){

        this.reOrderArray(answer)

        //nextId = Math.round(Math.random() * (this.wordArray.length - 1));
        //nextId = this.getGoodRandomId();
        // as we now use ordered array we dont need random and pick alway the first value
        var nextId = 0

        //globalWordIdIndex = nextId; // this is not true and cannot be used becuase it might be that array is getting replaced
        // we set it therefore to nulll
        globalWordIdIndex = null;

        //we need to prevent that we load the same word like last time.
        if(globalWordId == this.wordArray[0]["wordId"]){
            nextId = 1;
        }else{
            nextId = 0;
        }

        // in 3% of the cases we chose the ned of the array to prevent words laying aroudn there too long
        var rnd = Math.random();

        if(rnd <= 0.03){
            //alert("using end...");
            nextId = this.wordArray.length -1;
            //alert(nextId);
        }

        globalWordId = this.wordArray[nextId]["wordId"]

        console.log("nextId = " + nextId);

        var l1 = this.wordArray[nextId]["language1"];
        var l2 = this.wordArray[nextId]["language2"];
        var w1 = this.wordArray[nextId]["word1"];
        var w2 = this.wordArray[nextId]["word2"];

        if(l1 == null){l1 = " ";};
        if(l2 == null){l2 = " ";};
        if(w1 == null){w1 = " ";};
        if(w2 == null){w2 = " ";};

        console.log("l1 = " + l1);
        console.log("w1 = " + w1);
        console.log("l2 = " + l2);
        console.log("w2 = " + w2);

        objUxUi.setLearnFormValues(l1, w1, l2, w2);
    }
  }

  this.answerQuestionmark = function() {
    objUxUi.showHiddenWord();
  }

  // initialize the loading. Result is handled by callback
  this.loadWord = function() {
    var s = this.getCookie("session");
    //var r = new JsonLoadWordRequest("", "", s);
    var r = new JsonLoadWordArrayRequest("", "", s);
    objDataAccess.ajaxPost(this, r);
  }

  // handle the events from keyboard
  this.handleKey = function(x) {

    // we need to prevent this from running when on mobile device otherwise when editing a word the keyboard gets
    // into the way

    if(Number(globalVisibleScreen) == Number(2)){
        // if we are in edit word
        return;
    }else{
        if (x == 37) {
          this.answerYes();
        }
        if (x == 39) {
          this.answerNo();
        }
        if (x == 38 || x == 40) {
          this.answerQuestionmark();
        }
    }


  }


  // handle settings
  this.getSettings = function(){

    var s = this.getCookie("session");
    var r = new JsonGetSettings(s);
    objDataAccess.ajaxPost(this, r);

  }

  this.setSettings = function(){

    if(Math.random() > 0.5){
        this.settings["Russian"]["From"] = false;
    }else{
        this.settings["Russian"]["From"] = true;
    }

    var s = this.getCookie("session");
    var r = new JsonSetSettings(s, this.settings);
    objDataAccess.ajaxPost(this, r);

  }

  //============================================================================
  //
  //  CALLBACK FUNCTIONS
  //
  //============================================================================
  // function to handle call back from Ajax

  this.callBack = function(responseObject) {

    var pushToGui;
    var nextId;

    //console.log(responseObject["result"]);
    console.log(responseObject["action"]);

    if (responseObject["action"] === "adVocFromUrl") {
      this.loadFromUrlResult(responseObject);
    } else if (responseObject["action"] === "loadWord") {
      globalWordId = responseObject["wordId"];
      var l1 = responseObject["language1"];
      var l2 = responseObject["language2"];
      var w1 = responseObject["word1"];
      var w2 = responseObject["word2"];
      objUxUi.setLearnFormValues(l1, w1, l2, w2);

      this.makeToast(responseObject["success"], responseObject["experiment"], responseObject["once_learned"]);

    } else if (responseObject["action"] === "loadWordArray") {

      // words

      console.log("this.wordArray.length = " + this.wordArray.length);
      if (this.wordArray.length < 1){
        pushToGui = true;
      }else{
        pushToGui = false;
      }

      this.wordArray = responseObject["words"];

      console.log("loaded the array of words");
      console.log("pushToGui = " + pushToGui);

      if(pushToGui){

        // as we use now a sorted array we don't need random
        //nextId = Math.round(Math.random() * this.wordArray.length);
        nextId = 0

        console.log("nextId = " + nextId);

        globalWordId = this.wordArray[nextId]["wordId"];

        var l1 = this.wordArray[nextId]["language1"];
        var l2 = this.wordArray[nextId]["language2"];
        var w1 = this.wordArray[nextId]["word1"];
        var w2 = this.wordArray[nextId]["word2"];

        if(l1 == null){l1 = " ";};
        if(l2 == null){l2 = " ";};
        if(w1 == null){w1 = " ";};
        if(w2 == null){w2 = " ";};


        // put a random value to the gui
        objUxUi.setLearnFormValues(l1, w1, l2, w2);


      }

      // we need to check for a toast no matter what
      this.makeToast(responseObject["success"], responseObject["experiment"], responseObject["once_learned"]);



    } else if (responseObject["action"] === "report") {
      var newWords = responseObject["newWords"];
      var learnedWords = responseObject["learnedWords"];
      objUxUi.setResults(learnedWords, newWords);
    } else if (responseObject["action"] === "checkSession") {
      // if session valid then we can start the application
      // otherwise we go to login form
      var check = responseObject["sessionValid"];
      if (check) {
        // session valid
        objUxUi.initializeTrainingGui();
        globalVisibleScreen = 1;
      } else {
        // need to login to get a session
        objUxUi.setLoginForm("Please log in");
      }
    } else if (responseObject["action"] === "logIn") {
      //  logIn
      var success = responseObject["success"];
      if (success) {
        console.log("login success");
        globalSession = responseObject["session"];
        this.setCookie("session", globalSession);
        console.log("loading app");
        //objUxUi.setNavi("");
        objUxUi.setLearnForm();

      } else {
        objUxUi.setLoginForm("Login failed. Please try again or reset password. If you are not registered, please register - it's free.");
      }

    } else if (responseObject["action"] === "registerUser") {
      var success = responseObject["success"];
      if (success) {
        objUxUi.setAfterResetRegistration("Please check your email and login using the provided password.");
      }

    } else if (responseObject["action"] === "resetPassword") {
      var success = responseObject["success"];
      if (success) {
        objUxUi.setAfterResetRegistration("Please check your email and login using the provided password.");
      }
    } else if (responseObject["action"] === "editWord") {

      // after editing a word
      objUxUi.setNavi("");
      objUxUi.setLearnForm();

    } else if(responseObject["action"] === "getSettings"){

      this.settings = responseObject["settings"];
        // settings
    } else if(responseObject["action"] === "setSettings"){

      console.log("set settings object received. result is: success = " + responseObject["success"]);
        // settings
    } else if(responseObject["action"] === "faq" || responseObject["action"] === "privacy" || responseObject["action"] === "terms" || responseObject["action"] === "feedback-contact"){

      objUxUi.setStaticContentForm(responseObject["content"]);
        // settings

    } else if (responseObject["action"] === "translateWord" ){

        objUxUi.setTranslationAddVoc(responseObject["translation"]);

    } else if (responseObject["action"] === "bulkAddVoc" ){


        objUxUi.setAddVocFormMessage("New words were uploaded. ");

    }else {
      console.log("ERROR in controller callBack - action not found: " + responseObject["action"]);
      console.log(responseObject);
    }
  };

  // TiDo: Where is this used ???
  this.loadFromUrlResult = function(responseObject) {
    objUxUi.setAddVocFormMessage(responseObject["result"]);
  };

  this.notImplemented = function() {
    objUxUi.makeToast("This functionality is not implemented yet. ");
  }


  //============================================================================
  //
  //  TOAST
  //
  //============================================================================

  // check what kind of toas we make and if we make a makeToast
  this.makeToast = function(success, experiment, once_learned) {
    if (experiment) {
      if (success) {
        objUxUi.makeToast("Good, you still know the word that you recently learned.", false);
      } else {
        objUxUi.makeToast("What a pity, you forgot a word.", true);
      };

    } else {
      if (success) {
        if (once_learned) {
          objUxUi.makeToast("Well done, you learned again the word that you forgot.", false);
        } else {
          objUxUi.makeToast("Well done, you learned a new word!!!", false);
        }

      }
    };

  };
  // ======================= utility functions =================================



  this.validateEmail = function(email) {
    var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(String(email).toLowerCase());
  }

}
