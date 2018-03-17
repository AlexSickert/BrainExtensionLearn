function DataAccess() {

  var cookieMap;


  /*
   * get the list of files and its download links for a specific id
   */
  this.ajaxPost = function(controller, request) {
    console.log("in ajax post");
    try {
      var r = request;
      var req = new AjaxRequest();
      req.onreadystatechange = function() {
        if (req.readyState === 4) {
          try {
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


  this.ajaxPostJson = function(con, endpoint, json) {


    var req = new AjaxRequest();


    req.onreadystatechange = function() {
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

  }

  this.getCookieValue = function(cname) {

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



  this.setCookieValue = function(cname, cvalue) {

    console.log("setCookieValue cname = " + cname);
    console.log("setCookieValue cvalue = " + cvalue);

    var d = new Date();
    d.setTime(d.getTime() + (999 * 24 * 60 * 60 * 1000));
    var expires = "expires=" + d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
  }


}  // end of class


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
function JsonAddVocRequest(l, u, w, t, a, tl, tw) {
  this.language = l; // module
  this.url = u;
  this.word = w;
  this.text = t;
  this.action = a;
  this.translationLanguage = tl;
  this.translationWord = tw
}
