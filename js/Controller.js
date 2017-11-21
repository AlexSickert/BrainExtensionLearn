/*
 
 
 
 */



function Controller() {

    var objDataAccess = new DataAccess();
    var objUxUi;

    /*
     * this function runs when the html page loads initially
     */
    this.init = function (uxui) {

        // set navigation and main body area
        objUxUi = uxui;
        objUxUi.setNavi("");
        objUxUi.setLearnForm();

        return;
    };

    //===================================================
    // function to handle Ui Interaction

    this.setAddVocForm = function () {
        objUxUi.setNavi("add");
        objUxUi.setAddVocForm();
        return;
    };
    
    this.setLearnForm = function () {
        objUxUi.setNavi("learn");
        objUxUi.setLearnForm();
        return;
    };  
    
    this.setSettingsForm = function () {
        objUxUi.setNavi("settings");
        objUxUi.setSettingsForm();
        return;
    };   
    
    this.setResultsForm = function () {
        objUxUi.setNavi("results");
        objUxUi.setResultsForm();
        return;
    };       

    /*
     * loads a given url and its language from web and ads it to database
     */
    this.saveAddVoc = function () {
        var l = objUxUi.getValue("adVocLanguage");
        var u = objUxUi.getValue("adVocUrl");
        var w = objUxUi.getValue("adVocWord");
        var t = objUxUi.getValue("adVocText");
        objUxUi.setAddVocFormMessage("processing...");

	console.log("adVocLanguage = " + l);
	console.log("adVocUrl = " + u);
	console.log("adVocWord = " + w);
	console.log("adVocText = " + t);

        var r = new JsonAddVocRequest(l, u, w, t, "adVocFromUrl");
        objDataAccess.ajaxPost(this, r);
    };



    //===================================================
    // function to handle call back from Ajax

    this.callBack = function (responseObject) {

        console.log(responseObject["result"]);
        console.log(responseObject["action"]);
        
        if(responseObject["action"] === "adVocFromUrl"){            
            this.loadFromUrlResult(responseObject);            
        }
    };
    
    
    this.loadFromUrlResult = function (responseObject) {          
        objUxUi.setAddVocFormMessage(responseObject["result"]);        
    };
}