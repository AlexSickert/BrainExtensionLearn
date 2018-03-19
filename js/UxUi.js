/*
 * Handle everything that has to to with Gui interaction
 */

function UxUi() {

  /**
   * Set the navigation bar in the UI
   *
   */
  var controller;

  this.setController = function(c) {
    controller = c;
  }

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
    //this.setHtmlInDiv("mainBody", this.getLearnForm());
    this.hideDiv("mainBody");
    this.initializeTrainingGui();

  };


  /**
   * Set the vocabulary and labels for languages in the html decoded
   * ToDo: Don't set values in all divs, just in the ones that are needed
   */
  this.setLearnFormValues = function(l1, w1, l2, w2) {
    //this.setHtmlInDiv("mainBody", this.getLearnForm());
    this.setHtmlInDiv("language1", l1);
    this.setHtmlInDiv("word1", w1);
    this.setHtmlInDiv("language2", l2);
    this.setHtmlInDiv("word2", "");

    this.setHtmlInDiv("dlanguage1", l1);
    this.setHtmlInDiv("dword1", w1);
    this.setHtmlInDiv("dlanguage2", l2);
    this.setHtmlInDiv("dword2", "");

    this.setHtmlInDiv("mllanguage1", l1);
    this.setHtmlInDiv("mlword1", w1);
    this.setHtmlInDiv("mllanguage2", l2);
    this.setHtmlInDiv("mlword2", "");

    globalWordHidden = w2

    // once we have set the words it is necessary to adjust layout
    this.showTrainingUi();
  };

  this.showHiddenWord = function() {
    this.setHtmlInDiv("word2", globalWordHidden);
    this.setHtmlInDiv("dword2", globalWordHidden);
    this.setHtmlInDiv("mlword2", globalWordHidden);
  }


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


  /**
   * Geneal function to create a standard button
   */
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

  /*----------------------------------------------------------------*/

  // this one is needed as we first need to load the word, but we don't want to
  // make the user waiting. So we lead dummy values.
  this.initializeTrainingGui = function() {
    this.setLearnFormValues("loading...", "loading...", "loading...", "loading...")
    this.showTrainingUi();
    // now load the word1
    controller.loadWord();
  }


  this.showTrainingUi = function() {

    // hide all
    this.hideDiv("mobileLandscape");
    this.hideDiv("mobilePortrait");
    this.hideDiv("desktop");
    this.hideDiv("mainNavi");
    this.hideDiv("mainBody");

    // detect if mobile device
    var device = "d";

    if (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
      device = "m";
    }


    // detect if landscape or portrait
    var h = this.getHeight() - 0;
    var w = this.getWidth() - 0;
    var orientation = "l";

    if (h < w) {
      orientation = "l";
    } else {
      orientation = "p";
    }

    console.log("orientation: " + orientation);
    console.log("device: " + device);


    if (device === "m") {
      if (orientation === "p") {
        this.showDiv("mobilePortrait");
        this.fitMobilePortrait();
      } else {
        this.showDiv("mobileLandscape");
        this.fitMobileLandscape();
      }

    } else {
      // Desktop
      this.showDiv("desktop");
      this.fitDesktop();
      //show("mobileLandscape");
      //fitMobileLandscape()

      //show("mobilePortrait");
      //fitMobilePortrait();
    }
  };

  /**
   *
   *
   */
  this.hideTrainingUi = function() {
    this.hideDiv("desktop");
    this.hideDiv("mobileLandscape");
    this.hideDiv("mobilePortrait");
  }

  this.fitDesktop = function() {
    document.body.style.overflow = "hidden";

    var h = this.getHeight() - 0;
    var w = this.getWidth() - 0;

    document.getElementById("dspacer").style.height = Math.floor(h * 0.05) + "px";
    document.getElementById("dword1").style.height = Math.floor(h * 0.2) + "px";
    document.getElementById("dlanguage1").style.height = Math.floor(h * 0.1) + "px";
    document.getElementById("dword2").style.height = Math.floor(h * 0.2) + "px";
    document.getElementById("dlanguage2").style.height = Math.floor(h * 0.1) + "px";

    document.getElementById("dbottombuttons1").style.width = Math.floor(w * 0.1) + "px";
    document.getElementById("dbottombuttons2").style.width = Math.floor(w * 0.1) + "px";
    document.getElementById("dbottombuttons3").style.width = Math.floor(w * 0.1) + "px";

    document.getElementById("dbottombuttons1").style.height = Math.floor(h * 0.2) + "px";
    document.getElementById("dbottombuttons2").style.height = Math.floor(h * 0.2) + "px";
    document.getElementById("dbottombuttons3").style.height = Math.floor(h * 0.2) + "px";

  }

  this.fitMobileLandscape = function() {

    // disable scroll bars
    document.body.style.overflow = "hidden";

    var h = this.getHeight() - 0;
    var w = this.getWidth() - 0;

    console.log("settign width: " + Math.floor(w * 0.15) + "px");
    document.getElementById("mlyes").style.width = Math.floor(w * 0.1) + "px";
    document.getElementById("mlyes").style.height = Math.floor(h * 0.95) + "px";

    // set middle part
    document.getElementById("mlcontent").style.width = Math.floor(w * 0.8) + "px";
    document.getElementById("mlnavigation").style.height = Math.floor(h * 0.06) + "px";
    document.getElementById("mllanguage1").style.height = Math.floor(h * 0.1) + "px";
    document.getElementById("mlword1").style.height = Math.floor(h * 0.3) + "px";
    document.getElementById("mllanguage2").style.height = Math.floor(h * 0.1) + "px";
    document.getElementById("mlword2").style.height = Math.floor(h * 0.3) + "px";
    document.getElementById("mlquestion").style.height = Math.floor(h * 0.1) + "px";
    document.getElementById("mlno").style.width = Math.floor(w * 0.1) + "px";
    document.getElementById("mlno").style.height = Math.floor(h * 0.95) + "px";
    //document.getElementById("mlyes").innerHTML = "asfasfasdfasd";
  }


  this.fitMobilePortrait = function() {

    // disable scroll bars
    document.body.style.overflow = "hidden";

    var h = this.getHeight() - 0;
    var w = this.getWidth() - 0;

    // set width

    document.getElementById("topbuttons1").style.width = Math.floor(w * 0.3) + "px";
    document.getElementById("topbuttons2").style.width = Math.floor(w * 0.4) + "px";
    document.getElementById("topbuttons3").style.width = Math.floor(w * 0.3) + "px";

    document.getElementById("language1").style.width = Math.floor(w) + "px";
    document.getElementById("word1").style.width = Math.floor(w) + "px";
    document.getElementById("language2").style.width = Math.floor(w) + "px";
    document.getElementById("word2").style.width = Math.floor(w) + "px";

    document.getElementById("bottombuttons1").style.width = Math.floor(w * 0.35) + "px";
    document.getElementById("bottombuttons2").style.width = Math.floor(w * 0.30) + "px";
    document.getElementById("bottombuttons3").style.width = Math.floor(w * 0.35) + "px";

    // set height

    document.getElementById("topbuttons1").style.height = Math.floor(h * 0.1) + "px";
    document.getElementById("topbuttons2").style.height = Math.floor(h * 0.1) + "px";
    document.getElementById("topbuttons3").style.height = Math.floor(h * 0.1) + "px";

    document.getElementById("language1").style.height = Math.floor(h * 0.1) + "px";
    document.getElementById("word1").style.height = Math.floor(h * 0.22) + "px";
    document.getElementById("language2").style.height = Math.floor(h * 0.1) + "px";
    document.getElementById("word2").style.height = Math.floor(h * 0.22) + "px";

    document.getElementById("bottombuttons1").style.height = Math.floor(h * 0.2) + "px";
    document.getElementById("bottombuttons2").style.height = Math.floor(h * 0.2) + "px";
    document.getElementById("bottombuttons3").style.height = Math.floor(h * 0.2) + "px";

    // modify font size



    //alert(document.getElementById("test3").style.width)

    this.positionTest("test1", h, w, true, true);
    this.positionTest("test2", h, w, true, false);
    this.positionTest("test3", h, w, false, true);
    this.positionTest("test4", h, w, false, false);


    var ratio = window.devicePixelRatio || 1;
    var sw = screen.width;
    var sh = screen.height;


    var txt = " window.innerWidth = " + w + "; innerh= " + h + "; ";
    txt += " screen.width = " + w + "; ";
    txt += " window.devicePixelRatio = " + ratio;

    //document.getElementById("word2").innerHTML = txt ;


    // calucalte the real hight
    var rh = sh * ratio;
    var rw = sw * ratio;

    var area = rh * rw;

    var resAdj = Math.floor(Math.sqrt(area) / 30);


    // set font size

    // calcualte space of text areas
    var space = w * h * 0.22;

    space = Math.sqrt(space)

    var content = space + " faksjf ;lasj;flja sd;lkfa dfka s'dfk";



    var s1 = this.getFontSize(space, "Word1");
    var s2 = this.getFontSize(space, content);


    document.getElementById("word2").innerHTML = content;

    document.getElementById("topbuttons1").style.fontSize = Math.floor(h * 0.1 * 0.5) + "px";
    document.getElementById("topbuttons2").style.fontSize = Math.floor(h * 0.1 * 0.5) + "px";
    document.getElementById("topbuttons3").style.fontSize = Math.floor(h * 0.1 * 0.5) + "px";

    document.getElementById("language1").style.fontSize = Math.floor(h * 0.1 * 0.5) + "px";
    document.getElementById("word1").style.fontSize = Math.floor(s1) + "px";
    document.getElementById("language2").style.fontSize = Math.floor(h * 0.1 * 0.5) + "px";
    document.getElementById("word2").style.fontSize = Math.floor(s2) + "px";

    document.getElementById("bottombuttons1").style.fontSize = Math.floor(h * 0.2 * 0.5) + "px";
    document.getElementById("bottombuttons2").style.fontSize = Math.floor(h * 0.2 * 0.5) + "px";
    document.getElementById("bottombuttons3").style.fontSize = Math.floor(h * 0.2 * 0.5) + "px";


  };


  this.showDiv = function(id) {
    console.log("show: " + id);
    document.getElementById(id).style.display = "block";
    document.getElementById(id).style.visibility = "visible";
  }

  this.hideDiv = function(id) {
    console.log("hide: " + id);
    document.getElementById(id).style.display = "none";
    document.getElementById(id).style.visibility = "hidden";
  }

  this.getWidth = function() {
    var screenWidth = 0;

    try {
      if (screen.width > window.innerWidth) {
        screenWidth = window.innerWidth;
      } else {
        screenWidth = screen.width;
      };
    } catch (e) {
      //log("error", "2 getWidth()", "error when positioning id:  error: " + e.description);
    }

    //console.log("screenWidth: " + screenWidth);
    //log("info", "getWidth()", "screenWidth: " + screenWidth);
    return screenWidth;
  }


  this.getHeight = function() {
    var screenHeight = 0;

    try {
      if (screen.height > window.innerHeight) {
        screenHeight = window.innerHeight;
      } else {
        screenHeight = screen.height;
      }

    } catch (e) {
      //log("error", "2 getHeight()", "error when positioning id:  error: " + e.description);
    }

    //console.log("screenHeight: " + screenHeight);
    //log("info", "getHeight()", "screenHeight: " + screenHeight);
    return screenHeight;

  }

  this.getFontSize = function(space, t) {

    var c = Math.sqrt(t.length);

    var s = 0.7 * space / c;

    return s;
  }

  /**
   * Question is if this function is anywhere used.
   */
  this.positionTest = function(id, h, w, top, left) {

    var s = 10;

    ele = document.getElementById(id)

    ele.style.width = "10px";
    ele.style.height = "10px";

    var vertical = 0;
    var horizontal = 0;


    if (top) {

      vertical = 0
    } else {

      vertical = h - s;

    }

    if (left) {
      horizontal = 0;
    } else {
      horizontal = w - s;
    }

    ele.style.position = "absolute";
    ele.style.left = horizontal + 'px';
    ele.style.top = vertical + 'px';



  }


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
