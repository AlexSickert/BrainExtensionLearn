



    function AjaxTranslate(request) {
    console.log("in ajax post");

    console.log("----------- JSON object ajaxPost --------------");
    console.log(JSON.stringify(request));
    console.log("-----------------------------------------------");

    try {
      var r = request;
      var req = new AjaxRequest();
      req.onreadystatechange = function() {
        if (req.readyState === 4) {
          try {
            console.log("---------- ajaxPost result ---------------");
            console.log(req.responseText);
            console.log("------------------------------------------");
            var resObj = JSON.parse(req.responseText);
            myCallBack(resObj);
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


  function get_close_button(){

  //return '<br><br><button type="button" onclick="hideTranslate()">close</button>';
  return "";

  };

    function myCallBack(res_obj){

        console.log("in myCallBack(res_obj)");
        //alert(res_obj["translation"]);


        var id = "translate";
    console.log("id1: " + id);

    // translate
    var element = document.getElementById(id);

    element.innerHTML = res_obj["translation"] + get_close_button();
    }


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

    function JsonTranslateVocRequest(l, w) {
  this.language = l;
  this.translationLanguage = "DE";
  this.word = w;
  this.translation = "";
  this.action = "translateRss";

}


    function translateMe(ele, e, l){

          var txt = "translating '" + e + "'...";
        prepareDiv(txt);

        ele.style.backgroundColor = "#ffeeee";

        console.log("start translateThis()");

        var ls = "";
        if(l.includes("ITALIAN")){ls = "IT"};
        if(l.includes("SPANISH")){ls = "ES"};
        if(l.includes("PORTUGUESE")){ls = "PT"};
        if(l.includes("RUSSIAN")){ls = "RU"};
        if(l.includes("FRENCH")){ls = "FR"};
        if(l.includes("ENGLISH")){ls = "EN"};

        var o = new JsonTranslateVocRequest(ls, e);
        console.log("translateThis() - sending data via ajax");
        AjaxTranslate(o);


    }


      function translateThis(e, l){

          var txt = "translating '" + e + "'...";
        prepareDiv(txt);

        //ele.style.backgroundColor = "#ffeeee";

        console.log("start translateThis()");

        var ls = "";
        if(l.includes("ITALIAN")){ls = "IT"};
        if(l.includes("SPANISH")){ls = "ES"};
        if(l.includes("PORTUGUESE")){ls = "PT"};
        if(l.includes("RUSSIAN")){ls = "RU"};
        if(l.includes("FRENCH")){ls = "FR"};
        if(l.includes("ENGLISH")){ls = "EN"};

        var o = new JsonTranslateVocRequest(ls, e);
        console.log("translateThis() - sending data via ajax");
        AjaxTranslate(o);


    }


    function prepareDiv(txt){

    var id = "translate";
    console.log("id1: " + id);

    // translate
    var element = document.getElementById(id);

    console.log("id1: " + id);
    showDiv(id);
    position(id, 100, 100);

    element.innerHTML = txt + get_close_button();

    }


    function position(id, h, v) {

    var s = 10;

    ele = document.getElementById(id)

    ele.style.width = "80%";
    ele.style.height = "50%";

    v = v + document.body.scrollTop;

    ele.style.position = "absolute";
    ele.style.left = h + 'px';
    ele.style.top = v + 'px';

  }


function hideTranslate(){
hideDiv("translate");

}


 function showDiv(id) {
    console.log("showxxx: " + id);
    document.getElementById(id).style.display = "block";
    document.getElementById(id).style.visibility = "visible";
    document.getElementById(id).style.backgroundColor = "#eeeeff";
    document.getElementById(id).style.padding = "30px";
  }

  function hideDiv(id) {
    console.log("hide: " + id);
    document.getElementById(id).style.display = "none";
    document.getElementById(id).style.visibility = "hidden";
  }


function getWidth() {
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


  function getHeight() {
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