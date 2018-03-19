/*



 */



function Controller() {

  var objDataAccess = new DataAccess();
  var objUxUi;

  /*
   * this function runs when the html page loads initially
   */
  this.init = function(uxui) {


    // set navigation and main body area
    objUxUi = uxui;

    //objUxUi.setNavi("");
    //objUxUi.setLearnForm();
    objUxUi.initializeTrainingGui();
    return;
  };

  //===================================================


  this.testJson = function() {

    var r = new JsonAddVocRequest("ldghfg", "udfghdfg", "wdfghdfgh", "tdfhf", "testJson");

    objDataAccess.ajaxPostJson(this, "json", r);


  }

  //===================================================
  // function to handle Ui Interaction

  this.setAddVocForm = function() {
    // hide the training html decoded
    objUxUi.hideTrainingUi();
    objUxUi.showDiv("mainNavi");
    objUxUi.showDiv("mainBody");
    objUxUi.setNavi("add");
    objUxUi.setAddVocForm();
    // add value form cookies
    objUxUi.setValue("adVocLanguage", this.getCookie("adVocLanguage"));
    objUxUi.setValue("adVocTranslationLanguage", this.getCookie("adVocTranslationLanguage"));
    return;
  };

  this.setLearnForm = function() {
    objUxUi.setNavi("learn");
    objUxUi.setLearnForm();
    return;
  };

  this.setSettingsForm = function() {
    objUxUi.setNavi("settings");
    objUxUi.setSettingsForm();
    return;
  };

  this.setResultsForm = function() {
    objUxUi.setNavi("results");
    objUxUi.setResultsForm();
    return;
  };

  /*
   * loads a given url and its language from web and ads it to database
   */
  this.saveAddVoc = function() {
    var l = objUxUi.getValue("adVocLanguage");
    var u = objUxUi.getValue("adVocUrl");
    var w = objUxUi.getValue("adVocWord");
    var t = objUxUi.getValue("adVocText");
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

    var r = new JsonAddVocRequest(l, u, w, t, "adVocFromUrl", tl, tw);
    objDataAccess.ajaxPost(this, r);
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
    var r = new JsonLoadWordRequest("YES",globalWordId);
    objDataAccess.ajaxPost(this, r);
  }

  this.answerNo = function(answer) {
    var r = new JsonLoadWordRequest("NO",globalWordId);
    objDataAccess.ajaxPost(this, r);
  }

  this.answerQuestionmark = function() {
    objUxUi.showHiddenWord();    
  }

  // initialize the loading. Result is handled by callback
  this.loadWord = function() {
    var r = new JsonLoadWordRequest("","");
    objDataAccess.ajaxPost(this, r);
  }


  //============================================================================
  // function to handle call back from Ajax

  this.callBack = function(responseObject) {

    console.log(responseObject["result"]);
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
    }
  };


  // TiDo: Where is this used ???
  this.loadFromUrlResult = function(responseObject) {
    objUxUi.setAddVocFormMessage(responseObject["result"]);
  };
}
