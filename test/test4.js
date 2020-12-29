
   window.onresize = init;



            function init() {

            // hide all 
            hide("mobileLandscape");
            hide("mobilePortrait");
            hide("desktop");

            

            

            // detect if mobile device
            var device = "d";

            if( /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ) {
              device = "m";
            }


            // detect if landscape or portrait
            var h = getHeight() - 0;
            var w = getWidth() - 0;
            var orientation = "l";

            if(h < w){
              orientation = "l";
            }else{
              orientation = "p";
            }

            console.log("orientation: " + orientation);
            console.log("device: " + device);


            if(device === "m"){
              if(orientation === "p"){
                show("mobilePortrait");
                fitMobilePortrait();
            }else{
              show("mobileLandscape");
              fitMobileLandscape();
            }

            }else{
            // Desktop
              show("desktop");
              fitDesktop();
              //show("mobileLandscape");
              //fitMobileLandscape()

              //show("mobilePortrait");
              //fitMobilePortrait();
            }


          


            };

            function fitDesktop(){
              document.body.style.overflow = "hidden";

              var h = getHeight() - 0;
              var w = getWidth() - 0;

              

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

            function fitMobileLandscape(){

              // disable scroll bars
              document.body.style.overflow = "hidden";

              var h = getHeight() - 0;
              var w = getWidth() - 0;

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

            function fitMobilePortrait() {

            // disable scroll bars
            document.body.style.overflow = "hidden";

            var h = getHeight() - 0;
            var w = getWidth() - 0;

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

            positionTest("test1", h, w, true, true);
            positionTest("test2", h, w, true, false);
            positionTest("test3", h, w, false, true);
            positionTest("test4", h, w, false, false);


            var ratio = window.devicePixelRatio || 1; 
            var sw = screen.width ; 
            var sh = screen.height ; 


            var txt = " window.innerWidth = " + w + "; innerh= " + h + "; ";
            txt += " screen.width = " + w + "; ";
            txt += " window.devicePixelRatio = " + ratio ;

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



            var s1 = getFontSize(space, "Word1");
            var s2 = getFontSize(space, content);


            document.getElementById("word2").innerHTML = content ;

            document.getElementById("topbuttons1").style.fontSize = Math.floor(h * 0.1 * 0.5)  + "px";
            document.getElementById("topbuttons2").style.fontSize = Math.floor(h * 0.1 * 0.5)  + "px";
            document.getElementById("topbuttons3").style.fontSize = Math.floor(h * 0.1 * 0.5)  + "px";

            document.getElementById("language1").style.fontSize = Math.floor(h * 0.1 * 0.5)  + "px";
            document.getElementById("word1").style.fontSize = Math.floor(s1)  + "px";
            document.getElementById("language2").style.fontSize = Math.floor(h * 0.1 * 0.5)  + "px";
            document.getElementById("word2").style.fontSize = Math.floor(s2)  + "px";

            document.getElementById("bottombuttons1").style.fontSize = Math.floor(h * 0.2 * 0.5)  + "px";
            document.getElementById("bottombuttons2").style.fontSize = Math.floor(h * 0.2 * 0.5)  + "px";
            document.getElementById("bottombuttons3").style.fontSize = Math.floor(h * 0.2 * 0.5) + "px";


            };

            function getFontSize(space, t){

            var c = Math.sqrt(t.length);

            var s = 0.7 * space / c;

            return s;
            }

            function positionTest(id, h, w, top, left){

            var s = 10;

            ele = document.getElementById(id)

            ele.style.width = "10px";
            ele.style.height = "10px";

            var vertical = 0;
            var horizontal = 0;


            if (top){

            vertical =  0
            }else{

            vertical = h - s;

            }

            if(left){
            horizontal = 0;
            }else{
            horizontal = w - s;
            }

            ele.style.position = "absolute";
            ele.style.left = horizontal +'px';
            ele.style.top = vertical +'px';



            }




            function getWidth() {
            var screenWidth = 0;

            try {
            if (screen.width > window.innerWidth) {
            screenWidth = window.innerWidth;
            }else{
            screenWidth = screen.width;
            }
            ;
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
            }else{
            screenHeight = screen.height;
            }

            } catch (e) {
            //log("error", "2 getHeight()", "error when positioning id:  error: " + e.description);
            }

            //console.log("screenHeight: " + screenHeight);
            //log("info", "getHeight()", "screenHeight: " + screenHeight);
            return screenHeight;

            }






            function full_screen()
            {
            // check if user allows full screen of elements. This can be enabled or disabled in browser config. By default its enabled.
            //its also used to check if browser supports full screen api.
            if("fullscreenEnabled" in document || "webkitFullscreenEnabled" in document || "mozFullScreenEnabled" in document || "msFullscreenEnabled" in document) 
            {
            if(document.fullscreenEnabled || document.webkitFullscreenEnabled || document.mozFullScreenEnabled || document.msFullscreenEnabled)
            {
            console.log("User allows fullscreen");

            var element = document.getElementById("story");
            //requestFullscreen is used to display an element in full screen mode.
            if("requestFullscreen" in element) 
            {
            element.requestFullscreen();
            } 
            else if ("webkitRequestFullscreen" in element) 
            {
            element.webkitRequestFullscreen();
            } 
            else if ("mozRequestFullScreen" in element) 
            {
            element.mozRequestFullScreen();
            } 
            else if ("msRequestFullscreen" in element) 
            {
            element.msRequestFullscreen();
            }

            }
            }
            else
            {
            console.log("User doesn't allow full screen");
            }
            }

            function screen_change()
            {
            //fullscreenElement is assigned to html element if any element is in full screen mode.
            if(document.fullscreenElement || document.webkitFullscreenElement || document.mozFullScreenElement || document.msFullscreenElement) 
            {
            console.log("Current full screen element is : " + (document.fullscreenElement || document.webkitFullscreenElement || document.mozFullScreenElement || document.msFullscreenElement))
            }
            else
            {
            // exitFullscreen us used to exit full screen manually
            if ("exitFullscreen" in document) 
            {
            document.exitFullscreen();
            } 
            else if ("webkitExitFullscreen" in document) 
            {
            document.webkitExitFullscreen();
            } 
            else if ("mozCancelFullScreen" in document) 
            {
            document.mozCancelFullScreen();
            } 
            else if ("msExitFullscreen" in document) 
            {
            document.msExitFullscreen();
            }
            }
            }

            //called when an event goes full screen and vice-versa.
            document.addEventListener("fullscreenchange", screen_change);
            document.addEventListener("webkitfullscreenchange", screen_change);
            document.addEventListener("mozfullscreenchange", screen_change);
            document.addEventListener("MSFullscreenChange", screen_change);

            //called when requestFullscreen(); fails. it may fail if iframe don't have allowfullscreen attribute enabled or for something else. 
            document.addEventListener("fullscreenerror", function(){console.log("Full screen failed");});
            document.addEventListener("webkitfullscreenerror", function(){console.log("Full screen failed");});
            document.addEventListener("mozfullscreenerror", function(){console.log("Full screen failed");});
            document.addEventListener("MSFullscreenError", function(){console.log("Full screen failed");});


            function show(id) {
                console.log("show: " + id);
                document.getElementById(id).style.display = "block";
                document.getElementById(id).style.visibility = "visible";
            }

            function hide(id) {
                console.log("hide: " + id);
                document.getElementById(id).style.display = "none";
                document.getElementById(id).style.visibility = "hidden";
            }

