/*
 * Handle everything that has to to with Gui interaction
 */

function UxUi() {

  this.setNavi = function(current) {

    console.log("in this.setNavi = function (current) ");

    var s = "";

    var homeButton = this.getButton("Exit", "window.location.href='./'");

    s += homeButton;

    if (current === "add") {
      s += this.getButton("Learn", "con.setLearnForm()");
      s += this.getButton("Settings", "con.setSettingsForm()");
      s += this.getButton("Results", "con.setResultsForm()");
    }

    if (current === "learn" || current === "") {
      s += this.getButton("Add words", "con.setAddVocForm()");
      s += this.getButton("Settings", "con.setSettingsForm()");
      s += this.getButton("Results", "con.setResultsForm()");
    }

    if (current === "results") {
      s += this.getButton("Add words", "con.setAddVocForm()");
      s += this.getButton("Learn", "con.setLearnForm()");
      s += this.getButton("Settings", "con.setSettingsForm()");
    }

    if (current === "settings") {
      s += this.getButton("Add words", "con.setAddVocForm()");
      s += this.getButton("Learn", "con.setLearnForm()");
      s += this.getButton("Results", "con.setResultsForm()");
    }

    this.setHtmlInDiv("mainNavi", s);
    return;
  };

  this.setLearnForm = function() {
    this.setHtmlInDiv("mainBody", this.getLearnForm());
  };

  this.setSettingsForm = function() {
    this.setHtmlInDiv("mainBody", this.getSettingsForm());
  };

  this.setResultsForm = function() {
    this.setHtmlInDiv("mainBody", this.getResultsForm());
  };

  this.setAddVocForm = function() {
    this.setHtmlInDiv("mainBody", this.getAddVocForm());
  };

  this.setAddVocFormMessage = function(s) {
    s += this.getButton("Add words", "con.setAddVocForm()");
    this.setHtmlInDiv("mainBody", s);
  };

  this.setHtmlInDiv = function(id, html) {

    if (id === null) {
      console.log("id for this.setHtmlInDiv is null");
    } else {
      console.log("id to insert html into is: " + id);
    }

    if (html === null) {
      console.log("HTML content for this.setHtmlInDiv is null");
    } else {
      console.log("HTML content length for  this.setHtmlInDiv is: " + html.length);
    }
    document.getElementById(id).innerHTML = html;

    return;
  };


  this.getButton = function(text, code) {

    var s;
    s = "<input type=\"button\" id=\"" + text + "\" name=\"" + text + "\" class=\"naviButton\"  value=\"" + text + "\"  onclick=\"" + code + "\"  />";

    return s;
  };

  /*
   * retrieve values from a form for further usage
   */
  this.getValue = function(id) {
    //return document.getElementById(id).innerHTML;
    return document.getElementById(id).value;
  };

  this.setValue = function(id, value) {
    //return document.getElementById(id).innerHTML;
    document.getElementById(id).value = value;
  };

  // ======================= TEMPLATES =======================================

  this.getLearnForm = function() {
    var s = "";
    s += "<span id='leanFromLanguage'>language from</span><br>";
    s += "<span id='leanFromText'> textfrom</span><br>";
    s += "<span id='leanToLanguage'>language to</span><br>";
    s += "<span id='leanToText'>text  to</span><br>";
    s += this.getButton("YES", "");
    s += this.getButton("?", "");
    s += this.getButton("NO", "");
    return s;
  };

  this.getAddVocForm = function() {
    var s = "";
    s += "<input type='text' id='adVocLanguage' name='adVocLanguage' value = '' />";
    s += "<input type='text' id='adVocWord' name='adVocWord'  />";
    s += "<input type='text' id='adVocTranslationLanguage' name='adVocTranslationLanguage' value = '' />";
    s += "<input type='text' id='adVocTranslationWord' name='adVocTranslationWord'  />";
    s += this.getButton("Save Word", "con.saveAddVoc()");
    s += "<hr>";
    s += "<textarea id='adVocText' rows='4' cols='50'></textarea>";
    s += this.getButton("Save Text", "con.saveAddVoc()");
    s += "<hr>";
    s += "<textarea id='adVocUrl' rows='4' cols='50'></textarea>";
    s += this.getButton("Process Text from URL", "con.saveAddVoc()");
  
    return s;
  };


  this.getSettingsForm = function() {
    var s = "";
    s += "<span id='settingLabel1'>label1</span><input type='text' id='settingValue1' name='settingValue1' value='1' /><br>";
    s += "<span id='settingLabel2'>label2</span><input type='text' id='settingValue2' name='settingValue2' value='2' /><br>";
    s += "<span id='settingLabel3'>label3</span><input type='text' id='settingValue3' name='settingValue3' value='3' /><br>";
    return s;
  };

  this.getResultsForm = function() {
    var s = "";
    s += "<span id='resultLabel1'>result1</span><br>";
    s += "<span id='resultLabel2'>result2</span><br>";
    s += "<span id='resultLabel3'>result3</span><br>";
    return s;
  };
}
