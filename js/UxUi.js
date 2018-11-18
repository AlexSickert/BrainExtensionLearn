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

    var s = "<table><tr>";

    var homeButton = this.getButtonNavi("Exit", "window.location.href='./'");

    s += "<td class='blue'>" + homeButton + "</td>";



    if (current === "add") {
      s += "<td class='blue'>" + this.getButtonNavi("Learn", "con.setLearnForm()") + "</td>";
      //s += "<td class='blue'>" + this.getButtonNavi("Settings", "con.setSettingsForm()") + "</td>";
      s += "<td class='blue'>" + this.getButtonNavi("Logout", "con.logOut()") + "</td>";
      s += "<td class='blue'>" + this.getButtonNavi("Results", "con.setResultsForm()") + "</td>";
    }

    if (current === "learn" || current === "") {
      //s += "<td class='blue'>" + this.getButtonNavi("Add words", "con.setAddVocForm()") + "</td>";
      //s += "<td class='blue'>" + this.getButtonNavi("Settings", "con.setSettingsForm()") + "</td>";
      s += "<td class='blue'>" + this.getButtonNavi("Logout", "con.logOut()") + "</td>";
      s += "<td class='blue'>" + this.getButtonNavi("Results", "con.setResultsForm()") + "</td>";
    }

    if (current === "edit" || current === "") {
      //s += "<td class='blue'>" + this.getButtonNavi("Add words", "con.setAddVocForm()") + "</td>";
      //s += "<td class='blue'>" + this.getButtonNavi("Settings", "con.setSettingsForm()") + "</td>";
      s += "<td class='blue'>" + this.getButtonNavi("Logout", "con.logOut()") + "</td>";
      s += "<td class='blue'>" + this.getButtonNavi("Learn", "con.setLearnForm()") + "</td>";
      s += "<td class='blue'>" + this.getButtonNavi("Results", "con.setResultsForm()") + "</td>";
    }

    if (current === "results") {
      //s += "<td class='blue'>" + this.getButtonNavi("Add words", "con.setAddVocForm()") + "</td>";
      s += "<td class='blue'>" + this.getButtonNavi("Logout", "con.logOut()") + "</td>";
      s += "<td class='blue'>" + this.getButtonNavi("Learn", "con.setLearnForm()") + "</td>";
      //s += "<td class='blue'>" + this.getButtonNavi("Settings", "con.setSettingsForm()") + "</td>";
    }

    if (current === "settings") {
      //s += "<td class='blue'>" + this.getButtonNavi("Add words", "con.setAddVocForm()") + "</td>";
      s += "<td class='blue'>" + this.getButtonNavi("Learn", "con.setLearnForm()") + "</td>";
      s += "<td class='blue'>" + this.getButtonNavi("Results", "con.setResultsForm()") + "</td>";
    }

    s += "</tr></table>";
    this.setHtmlInDiv("mainNavi", s);
    this.adjustNaviFont();
    return;
  };


  this.adjustNaviFont = function(){

    var h = this.getHeight() - 0;

    var x = document.getElementsByClassName("buttonSmallBlue");
    var i;
    for (i = 0; i < x.length; i++) {
        x[i].style.fontSize = Math.floor(h * 0.1 * 0.4) + "px";
    }

  }

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

    console.log("---");
    console.log(l1);
    console.log(l2);
    console.log(w1);
    console.log(w2);
    console.log("---");
    //this.setHtmlInDiv("mainBody", this.getLearnForm());
    this.setHtmlInDiv("language1", l1.trim());
    this.setHtmlInDiv("word1", w1.trim());
    this.setHtmlInDiv("language2", l2.trim());
    this.setHtmlInDiv("word2", "");

    this.setHtmlInDiv("dlanguage1", l1.trim());
    this.setHtmlInDiv("dword1", w1.trim());
    this.setHtmlInDiv("dlanguage2", l2.trim());
    this.setHtmlInDiv("dword2", "");

    this.setHtmlInDiv("mllanguage1", l1.trim());
    this.setHtmlInDiv("mlword1", w1.trim());
    this.setHtmlInDiv("mllanguage2", l2.trim());
    this.setHtmlInDiv("mlword2", "");

    globalWord = w1.trim();
    globalWordHidden = w2.trim()

    // once we have set the words it is necessary to adjust layout
    this.showTrainingUi();
  };

  this.showHiddenWord = function() {
    this.setHtmlInDiv("word2", globalWordHidden);
    this.setHtmlInDiv("dword2", globalWordHidden);
    this.setHtmlInDiv("mlword2", globalWordHidden);
  }

  // show the login form
  this.setLoginForm = function(x) {
    this.setHtmlInDiv("mainBody", this.getLoginForm(x));
  };

  this.setAfterResetRegistration = function(x) {
    this.setHtmlInDiv("mainBody", this.getAfterResetRegistration(x));
  };

  this.setRegistrationForm = function(x) {
    this.setHtmlInDiv("mainBody", this.getRegistrationForm(x));
  };

  this.setPasswordResetForm = function(x) {
    this.setHtmlInDiv("mainBody", this.getPasswordResetForm(x));
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

  this.setEditVocForm = function() {

    this.setHtmlInDiv("mainBody", this.getEditVocForm());
    this.setValue("editFromWord", globalWord);
    this.setValue("editToWord", globalWordHidden);
  };

  this.setAddVocFormMessage = function(s) {
    s += this.getButton("Add words", "con.setAddVocForm()");
    this.setHtmlInDiv("mainBody", s);
  };

  // set the results in the html code and display
  this.setResults = function(learned, newWords) {
    var s = this.getResultsForm(learned, newWords);
    this.setHtmlInDiv("mainBody", s);
  };

  this.setLoading = function() {
    var s = this.getLoadingPlaceholder();
    this.setHtmlInDiv("mainBody", s);
  }

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
    //s = "<input type=\"button\" id=\"" + text + "\" name=\"" + text + "\" class=\"naviButton\"  value=\"" + text + "\"  onclick=\"" + code + "\"  />";
    s = "<span id=\"" + text + "\" class=\"buttonSmall\" onclick=\"" + code + "\">" + text + "</span>";

    return s;
  };

  this.getButtonNavi = function(text, code) {
    var s;
    //s = "<input type=\"button\" id=\"" + text + "\" name=\"" + text + "\" class=\"naviButton\"  value=\"" + text + "\"  onclick=\"" + code + "\"  />";
    s = "<span id=\"" + text + "\" class=\"buttonSmallBlue\" onclick=\"" + code + "\">" + text + "</span>";

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

   globalVisibleScreen = 1;

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

    //document.getElementById("dword2").innerHTML = navigator.userAgent;

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

    // set font sizes of the content

    var space = w * h;
    var s1 = this.getFontSize(space, document.getElementById("mlword1").innerHTML);
    var s2 = this.getFontSize(space, globalWordHidden);

    document.getElementById("mllanguage1").style.fontSize = Math.floor(h * 0.1 * 0.5) + "px";
    document.getElementById("mlword1").style.fontSize = Math.floor(s1) + "px";
    document.getElementById("mllanguage2").style.fontSize = Math.floor(h * 0.1 * 0.5) + "px";
    document.getElementById("mlword2").style.fontSize = Math.floor(s2) + "px";

  }


  this.fitMobilePortrait = function() {

    // disable scroll bars
    document.body.style.overflow = "hidden";

    var h = this.getHeight() - 0;
    var w = this.getWidth() - 0;

    // set width

    document.getElementById("topbuttons1").style.width = Math.floor(w * 0.2) + "px";
    document.getElementById("topbuttons2").style.width = Math.floor(w * 0.3) + "px";
    document.getElementById("topbuttons3").style.width = Math.floor(w * 0.2) + "px";
    document.getElementById("topbuttons4").style.width = Math.floor(w * 0.3) + "px";

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
    document.getElementById("topbuttons4").style.height = Math.floor(h * 0.1) + "px";

    document.getElementById("language1").style.height = Math.floor(h * 0.1) + "px";
    document.getElementById("word1").style.height = Math.floor(h * 0.25) + "px";
    document.getElementById("language2").style.height = Math.floor(h * 0.1) + "px";
    document.getElementById("word2").style.height = Math.floor(h * 0.25) + "px";

    document.getElementById("bottombuttons1").style.height = Math.floor(h * 0.2) + "px";
    document.getElementById("bottombuttons2").style.height = Math.floor(h * 0.2) + "px";
    document.getElementById("bottombuttons3").style.height = Math.floor(h * 0.2) + "px";

    // modify font size



    //alert(document.getElementById("test3").style.width)
    /*
    this.positionTest("test1", h, w, true, true);
    this.positionTest("test2", h, w, true, false);
    this.positionTest("test3", h, w, false, true);
    this.positionTest("test4", h, w, false, false);
    */


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

    // calcualte space of text areas
    var space = w * h;
    var content = space + "funktion noun konjunktion nomen )";

    // globalWordHidden

    var s1 = this.getFontSize(space, document.getElementById("word1").innerHTML);
    var s2 = this.getFontSize(space, globalWordHidden);

    var tst = document.getElementById("word1").innerHTML;
    tst = tst.trim();

    // following lines do not work properly, so we replace them with a function that works well in other places
    /*
    document.getElementById("topbuttons1").style.fontSize = Math.floor(h * 0.1 * 0.4) + "px";
    document.getElementById("topbuttons2").style.fontSize = Math.floor(h * 0.1 * 0.4) + "px";
    document.getElementById("topbuttons3").style.fontSize = Math.floor(h * 0.1 * 0.4) + "px";
    document.getElementById("topbuttons4").style.fontSize = Math.floor(h * 0.1 * 0.4) + "px";
    */
    this.adjustNaviFont();

    document.getElementById("language1").style.fontSize = Math.floor(h * 0.1 * 0.5) + "px";
    document.getElementById("word1").style.fontSize = Math.floor(s1) + "px";
    document.getElementById("language2").style.fontSize = Math.floor(h * 0.1 * 0.5) + "px";
    document.getElementById("word2").style.fontSize = Math.floor(s2) + "px";

    document.getElementById("bottombuttons1").style.fontSize = Math.floor(h * 0.2 * 0.3) + "px";
    document.getElementById("bottombuttons2").style.fontSize = Math.floor(h * 0.2 * 0.3) + "px";
    document.getElementById("bottombuttons3").style.fontSize = Math.floor(h * 0.2 * 0.3) + "px";




  };

  // dirty hack as Samsung browers did not work properly
  this.stringLength = function(s) {
    let i = 0;
    while (s != '') {
      i += 1;
      s = s.slice(1);
    }
    return i;
  }


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

    space = Math.sqrt(space);
    //var c = Math.sqrt(t.length);
    var l = this.stringLength(t) + 5; // to prevent weird effect for short strings
    var c = Math.sqrt(l);
    var s = 0.3 * space / c;
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



  this.getLoginForm = function(txt) {
    var s = "<br><br>";
    s += txt;
    s += "<br>";
    s += "<br>";
    s += "<table class='login'>";
    s += "<tr>";
    s += "<td><span id='xxxxxx'>Email: </span></td><td><input type='text' id='user' name='user' value='' /></td>";
    s += "</tr>";
    s += "<tr>";
    s += "<td><span id='xxxxxx'>Password: </span></td><td><input type='password' id='password' name='password' value='' /></td>";
    s += "</tr>";
    s += "</table>";
    s += "<br>";
    s += this.getButton("Login", "con.logIn()");
    s += "<br>";
    s += "<br>";
    s += this.getButton("Register", "con.gotRegistrationForm()");
    s += "<br>";
    s += "<br>";
    s += this.getButton("Forgot password", "con.gotResetForm()");
    return s;
  };


  this.getAfterResetRegistration = function(txt) {
    var s = "<br><br>";
    s += txt;
    s += "<br>";
    s += "<br>";
    s += this.getButton("Login", "con.gotLoginForm()");

    return s;
  };

  this.getRegistrationForm = function(txt) {
    var s = "<br><br>";
    s += txt;
    s += "<br>";
    s += "<br>";
    s += "<span id='xxxxxx'>Email: </span><input type='text' id='user' name='user' value='' /><br>";
    s += "<br>";
    s += "<br>";
    s += this.getButton("Register", "con.register()");
    s += "<br>";
    s += "<br>";
    s += this.getButton("Go to login", "con.gotLoginForm()");
    return s;
  };

  this.getPasswordResetForm = function(txt) {
    var s = "<br><br>";
    s += txt;
    s += "<br>";
    s += "<br>";
    s += "<span id='xxxxxx'>Email: </span><input type='text' id='user' name='user' value='' /><br>";
    s += "<br>";
    s += "<br>";
    s += this.getButton("Reset password", "con.resetPassword()");
    s += "<br>";
    s += "<br>";
    s += this.getButton("Go to login", "con.gotLoginForm()");
    return s;
  };


  /*
  This is probably not used anymore
  */
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
    s += "<textarea id='adVocText' rows='4' style='width:80%;'></textarea>";
    s += this.getButton("Save Text", "con.saveAddVoc()");
    s += "<hr>";
    s += "<textarea id='adVocUrl' rows='4' style='width:80%;'></textarea>";
    s += this.getButton("Process Text from URL", "con.saveAddVoc()");

    return s;
  };

  this.getEditVocForm = function() {
    var s = "";
    s += "Edit current word<br><br>";
    s += "<textarea id='editFromWord' rows='4' style='width:80%;'></textarea>";
    s += "<textarea id='editToWord' rows='4' style='width:80%;'></textarea>";
    s += "<br><br>";
    s += this.getButton("Save", "con.saveEditVoc()");
    s += "&nbsp;";
    s += this.getButton("Cancel", "con.setLearnForm()");
    return s;
  };

  this.getSettingsForm = function() {
    var s = "";
    s += "<span id='settingLabel1'>label1</span><input type='text' id='settingValue1' name='settingValue1' value='1' /><br>";
    s += "<span id='settingLabel2'>label2</span><input type='text' id='settingValue2' name='settingValue2' value='2' /><br>";
    s += "<span id='settingLabel3'>label3</span><input type='text' id='settingValue3' name='settingValue3' value='3' /><br>";
    return s;
  };

  this.getLoadingPlaceholder = function() {
    var s = "Content is loading...";
    return s;
  };

  this.getResultsForm = function(learned, newWords) {
    var s = "<br><br>";
    s += "<span id='resultLabel1'>words learned so far: " + learned + "</span><br>";
    s += "<span id='resultLabel1'>words remaining to learn: " + newWords + "</span><br>";
    return s;
  };

  this.makeToast = function(s,c) {

    // mmainPop

    e = document.getElementById("mainPop");

    if(c){
      e.className = "toastRed";
    }else{
      e.className = "toastGreen";
    }

    e.style.display = "block";
    e.innerHTML = s;

    var h = this.getHeight() - 0;
    var w = this.getWidth() - 0;

    var cw = document.getElementById("mainPop").clientWidth;
    var ch = document.getElementById('mainPop').clientHeight;

    var topD = Math.floor(0.5 * (h - ch));
    var leftD = Math.floor(0.5 * (w - cw));

    e.style.width = "50%";
    //e.style.height = "80%";
    e.style.zIndex = "99";
    //e.style.left = leftD + "px";
    e.style.left = "0px";
    //e.style.top = topD + "px";
    e.style.top = "0px";


    e.style.padding = "10px";

    setTimeout(function() {

      document.getElementById("mainPop").style.display = "none";

    }, 2000);

  };



}
