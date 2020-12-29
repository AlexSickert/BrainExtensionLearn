
function UxUi() {

    var parser = new Parser();
    var controller;
    var html;
    var currentScreen = -1;
    var arrLanguageLabels = ['English', 'Russian', 'Spanish', 'Italian', 'French', 'Portuguese', 'German'];

    var plublications = {

        "English": {
            "USA: New York Times": "https://www.nytimes.com",
            "USA: The Atlantic":"https://www.theatlantic.com/",
            "USA: Washington Post": "https://www.washingtonpost.com/",
            "UK: The Guardian":"https://www.theguardian.com/",
            "DAZED":"https://www.dazeddigital.com/"
        },

        "Russian": {
            "Апостроф":"https://apostrophe.ua/",
            "Russia: Forbes": "https://www.forbes.ru/",
            "Russia: Pravda": "https://www.pravda.ru/",
            "UA NEWS": "https://ua.news/ru/",
            "Russia: Kommersant": "https://www.kommersant.ru/",
            "Ukraine: Segodnya": "https://www.segodnya.ua/",
            "Ведомости": "https://www.vedomosti.ru/",
            "РБК - РОСБИЗНЕСКОНСАЛТИНГ": "https://www.rbc.ru/",
            "Obozrevatel":"https://www.obozrevatel.com/",
            "5sfer.com/":"https://5sfer.com/"
        },

        "Spanish": {
            // newspapers in venezuela https://en.wikipedia.org/wiki/List_of_newspapers_in_Venezuela
            "Spain: El Pais": "https://elpais.com/",
            "Venezuela: El Nacional": "https://www.elnacional.com/",
            "Venezuela: Ultimas Noticias": "http://www.ultimasnoticias.com.ve/"
        },

        "Italian": {
            "Open":"https://www.open.online/",
            "Italy: Corriere de la Sera": "https://www.corriere.it/",
            "Italy: La Repubblica": "https://www.repubblica.it/",
            "Ultrarunning Blog": "https://terzoristoro18.blogspot.com/?m=1"
        },

        "French": {
            // 18 french newspapers https://frenchtogether.com/french-newspaper/ 
            // top 100 french blogs  https://blog.feedspot.com/french_blogs/ 
            // "Le Monde Diplomatique": "https://www.monde-diplomatique.fr/",
            "France TV Info":"https://www.francetvinfo.fr/",
            "Capital":"https://www.capital.fr/",
            "France: Le Figaro": "https://www.lefigaro.fr/",
            "France: Le Monde": "https://www.lemonde.fr/",
            "Capital": "https://www.capital.fr/",
            "France: Liberation": "https://www.liberation.fr/"
        },
        "Portuguese": {
            // see https://www.fluentu.com/blog/portuguese/brazilian-bloggers/
            //  https://petiscos.jp/
            "Portugal: Expresso": "https://expresso.pt/",
            "Brazil: El Pais Brasil": "https://brasil.elpais.com/",
            "Brazil: Folha de S.Paulo": "https://www.folha.uol.com.br/",
            "Blog: Petiscos": "https://petiscos.jp/",
            "Blog: MÍRIAM LEITÃO": "https://blogs.oglobo.globo.com/miriam-leitao/",
            "Brazil: Veja": "https://veja.abril.com.br/",
            "Brazil: Jornal GGN": "https://jornalggn.com.br/",
            "Brazil: UOL": "https://www.uol.com.br/"

        },

        "German": {
            "Germany: Die Zeit": "https://www.zeit.de/index",
            "Germany: Der Spiegel": "https://www.spiegel.de/",
            "Switzerland: NZZ":"https://www.nzz.ch/",
            // austria news  https://de.wikipedia.org/wiki/Medien_in_%C3%96sterreich
            "Austria: Kronen Zeitung":"https://www.krone.at/"
            
        }
    };


    this.setController = function (x) {
        this.controller = x;
    };


    this.setHtml = function (x) {
        html = x;
    };


    this.getCurrentScreen = function (x) {
        return currentScreen;
    };


    this.setScreen = function (x, y) {
        /**
         * There are a limited number of screens: 
         * 
         * - login                  0
         * - start                  1
         * - more                   2
         * - choose-language        3
         * - choose-publication     4
         * - browse-copy-paste      5
         * - transfer-and-read      6
         * - saved-texts            7
         * - saved text titles      8
         * 
         */

        console.log("in UxUi() function setScreen values", x, y);

        switch (x) {

            case 0:
                this.makeLoginScreen();
                break;

            case 1:
                this.makeStartScreen();
                break;

            case 2:
                this.makeMoreScreen();
                break;

            case 3:
                this.makeChooseLanguageScreen();
                break;

            case 4:
                this.makeChoosePublicationScreen(y);
                break;

            case 5:
                this.makeBrowseCopyPasteScreen(y);
                break;

            case 6:
                this.makeTransferAndReadScreen(); // ths is not used!
                break;

            case 7:
                this.makeLoginScreen();
                break;
            case 8:
                this.makeTextListScreen(y);
                break;
            case 9:
                this.makeChooseLanguageForPasteTextScreen();
                break;
            default:
                this.makeErrorScreen();

        }
    };


    this.makeLoginScreen = function () {

        var s = "";

        s += "<input type=\"text\" id=\"user\">";
        s += "<input type=\"password\" id=\"pw\">";
        s += "<input type=\"button\" onclick=\"Con.login()\" value=\"submit\">";

        // todo: navigation needed here. 

        this.setBody("float-scrollable", s, null);

    };

    // redirect to the reader App
    this.goToApp = function () {
        window.location.href = "./app";
    };


    this.makeStartScreen = function () {
        console.log("in UxUi() function makeStartScreen()");
        // set navigation
//        var arrLabels = ['Logout', 'More'];
//        var arrFunctions = ['Con.logout()', 'UxUi.setScreen(2, 0)'];

        var arrLabels = ['Start', 'More', '+ Font', '- Font'];
        var arrFunctions = ['UxUi.setScreen(1, 0)', 'UxUi.setScreen(2, 0)', 'UxUi.updateFontSize(true)', 'UxUi.updateFontSize(false)'];
        this.setNavigation(arrLabels, arrFunctions);

        // set content        
        arrLabels = ['Browse News', 'Paste Text', 'Read saved texts'];
        arrFunctions = ['UxUi.setScreen(3, 0)', 'UxUi.setScreen(9, 0)', 'Con.loadTextList()'];
        this.setBody("float-button-list", arrLabels, arrFunctions);

        // set initial font size
        this.setInitialFontSize();

    };

    this.device = function () {
        var d = "d";
        if (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
            d = "m";
        }
        return d;
    };

    this.setInitialFontSize = function () {
        // if there is a cookie value then use it, oterhwise default value
        // depending on device

        // globalFontSize  default is 15
        var s = getCookieValue("readerFontSize");

        if (s.length < 1) {
            // cookie not existing, so we use default value
            if (this.device() === "m") {
                globalFontSize = 25;
            } else {
                globalFontSize = 15;
            }
        } else {
            // use cookie value
            globalFontSize = s;
        }

        var all = document.getElementsByTagName("*");
        for (var i = 0, max = all.length; i < max; i++) {
            try {
                all[i].style.fontSize = globalFontSize + "px";
            } catch (e) {
                // to do; todo
            }
        }

        setCookieValue("readerFontSize", globalFontSize + "");
    };


    this.makeMoreScreen = function () {
        console.log("in UxUi() function makeMoreScreen()");
        // set navigation
        var arrLabels = ['Start'];
        var arrFunctions = ['UxUi.setScreen(1, 0)'];
        this.setNavigation(arrLabels, arrFunctions);

        // set content        
        arrLabels = ['Go to Learner App', 'Logout', 'Privacy', 'Terms and Conditions'];
        arrFunctions = ['UxUi.goToApp()', 'Con.logout()', 'alert(999)', 'alert(999)'];
        this.setBody("float-button-list", arrLabels, arrFunctions);
    };


    this.makeChooseLanguageScreen = function () {
        console.log("in UxUi() function makeChooseLanguageScreen()");
        // set navigation
        var arrLabels = ['Start', 'More', '+ Font', '- Font', 'Go To APP'];
        var arrFunctions = ['UxUi.setScreen(1, 0)', 'UxUi.setScreen(2, 0)', 'UxUi.updateFontSize(true)', 'UxUi.updateFontSize(false)', 'UxUi.goToApp()'];
        this.setNavigation(arrLabels, arrFunctions);

        // set content  
        arrFunctions = ['UxUi.setScreen(4, 0)', 'UxUi.setScreen(4, 1)', 'UxUi.setScreen(4, 2)', 'UxUi.setScreen(4, 3)', 'UxUi.setScreen(4, 4)', 'UxUi.setScreen(4, 5)', 'UxUi.setScreen(4, 6)'];
        this.setBody("float-button-list", arrLanguageLabels, arrFunctions);

    };


    this.makeChoosePublicationScreen = function (indexLanguage) {
        /**
         * given a certain language, lost the publications that can be loaded
         */

        console.log("in UxUi() function makeChoosePublicationScreen()");
        var language = arrLanguageLabels[indexLanguage];
        console.log(language);

        globalChoosenLanguage = language;

        var pubArr = plublications[language];
        var langArr = [];
        var indexPublication = 0;
        var funcStrArr = [];

        for (var key in pubArr) {
            console.log(pubArr[key]);
            langArr.push(key);
            funcStrArr.push("UxUi.setScreen(5, [" + indexLanguage + "," + indexPublication + " ])");
            indexPublication += 1;
        }

        // show list of publications
        this.setBody("float-button-list", langArr, funcStrArr);

    };


    this.makeBrowseCopyPasteScreen = function (x) {

        console.log("in UxUi() function makeBrowseCopyPasteScreen()");

        var langIndex = x[0];
        var pubIndex = x[1];
        var l = arrLanguageLabels[langIndex];
        var pubArr = plublications[l];
        var i = 0;
        var url = "";

        for (var key in pubArr) {
            if (i === pubIndex) {
                url = pubArr[key];
            }
            i += 1;
        }

        // now we set the url into an iframe
        console.log("in UxUi() function makeBrowseCopyPasteScreen()", l);
        console.log("in UxUi() function makeBrowseCopyPasteScreen()", url);
        this.setBody("new-window", l, url);


    };

    this.makeTransferAndReadScreen = function () {
        alert('not used');
    };

    this.makeTextListScreen = function (arr) {

        var arrLabels = [];
        var arrFunctions = [];

        for (var i = 0; i < arr.length; i++) {
            var id = arr[i][0];
            var l = arr[i][1];
            var t = arr[i][2];
            var r = arr[i][3];

            if(r){
                arrLabels.push(html.bold("[READ] " + l + ": ") + t + "...");
            }else{
                arrLabels.push(html.bold(l + ": ") + t + "...");
            }

            arrFunctions.push("Con.loadText(" + id + ", '" + l + "')");
        }

        this.setBody("float-button-list", arrLabels, arrFunctions);


        var arrLabels = ['Start', 'More', '+ Font', '- Font'];
        var arrFunctions = ['UxUi.setScreen(1, 0)', 'UxUi.setScreen(2, 0)', 'UxUi.updateFontSize(true)', 'UxUi.updateFontSize(false)'];
        this.setNavigation(arrLabels, arrFunctions);


    };


    this.makeChooseLanguageForPasteTextScreen = function () {

        var arrLabels = [];
        var arrFunctions = [];

        for (var i = 0; i < arrLanguageLabels.length; i++) {

            var label = arrLanguageLabels[i];
            var func = "UxUi.setLanguageAndPasteScreen('" + arrLanguageLabels[i] + "')";

            arrLabels.push(label);
            arrFunctions.push(func);
        }

        this.setBody("float-button-list", arrLabels, arrFunctions);
    };


    this.setLanguageAndPasteScreen = function (l) {
        globalChoosenLanguage = l;
        this.setBody("text-area-for-paste", l, "");
    };


    this.makeErrorScreen = function (info) {
        console.log("ERROR: " + info);
    };


    this.setNavigation = function (arrLabels, arrFunctions) {
        /**
         *  creates the html for the navigation
         *  For all screens the navigation can get set independent from the rest 
         *  of the page
         */

        var h = html.getNavigationButtons(arrLabels, arrFunctions);
        var e = this.getElement("mainNavi");
        this.setInnerHtml(e, h);
    };


    this.setBody = function (bodyType, x, y) {

        var h = "Error";
        var e = this.getElement("mainBody");

        // this.setBody("float-button-list", arrLabels, arrFunctions);

        switch (bodyType) {

            case "float-button-list":
                h = html.getBodyFloatButtonList(x, y);
                this.makeLoginScreen();
                break;

            case "new-window":
                // open the url in a new tab and show here textarea
                // y is url
                window.open(y, '_blank');
                //h = html.getBodyIframe(x, y);                    
                h = html.getBodyTextAreaForm(x, "Copy text from article and paste it here", y, "UxUi.convertText(true)", "Next");
                break;
            case "text-area-for-paste":
                // function (language, label, url, f, fLabel)
                h = html.getBodyTextAreaForm(x, "Copy text from article and paste it here", y, "UxUi.convertText(true)", "Next");
                break;
            case "float-reader":
                h = html.getBodyFloatContainer(y, x);
                break;
            case "float-scrollable":
                h = html.getBodyFloatContainer("", x);
                break;
            default:
                this.makeErrorScreen();

        }

        this.setInnerHtml(e, h);

    };

    this.convertText = function (save_text) {

        //  textarea
        var s = this.getElement("textarea").value;
        globalCurrentText = s;

        // save text in database on backend
        if (save_text) {
            this.controller.saveText();
        }


        // now we split the text into sentences and then into words
        parser.parse(s);

        var h = html.getNavigationButton("defaultButton", "Set text as read", "Con.setTextRead()");
        h += "<br>";
        h += parser.getHtml();
        this.setBody("float-reader", h, "floatReaderContainer");

        // adjust font of the text
        this.updateFontSize(false);
        this.updateFontSize(true);

    };


    this.convertSavedText = function (s) {
        globalCurrentText = s;
        // now we split the text into sentences and then into words
        parser.parse(s);
        var h = html.getNavigationButton("defaultButton", "Set text as read", "Con.setTextRead()");
        h += "<br>";
        h += parser.getHtml();
        this.setBody("float-reader", h, "floatReaderContainer");

        // adjust font of the text
        this.updateFontSize(false);
        this.updateFontSize(true);
    };


    this.getElement = function (x) {

        return document.getElementById(x);
    };

    this.setInnerHtml = function (ele, html) {
        ele.innerHTML = html;

    };


    this.st = function (sentence, word, element) {
        // shows the translation window
        //alert(parser.getWord(word));
        //alert(parser.getSentence(sentence));  

        // highlight the choosen word
        element.style.backgroundColor = "yellow";

        var h = html.getTranslationForm(globalChoosenLanguage, parser.getSentence(sentence), parser.getWord(word));
        this.setInnerHtml(this.getElement("mainPop"), h);
        this.showTranslation();
    };

    this.getScroll = function () {

        if (window.pageYOffset !== undefined) {
            return [pageXOffset, pageYOffset];
        } else {
            var sx, sy, d = document,
                    r = d.documentElement,
                    b = d.body;
            sx = r.scrollLeft || b.scrollLeft || 0;
            sy = r.scrollTop || b.scrollTop || 0;
            return [sx, sy];
        }
    };

    this.position = function (id, h, v) {

        ele = document.getElementById(id);
        ele.style.width = "80%";
        ele.style.height = "50%";
        console.log("scroll top: " + this.getScroll()[1]);
        v = v + this.getScroll()[1];
        ele.style.position = "absolute";
        ele.style.left = h + 'px';
        ele.style.top = v + 'px';
    };

    this.showTranslation = function () {
        this.showDiv("mainPop");
        this.position("mainPop", 10, 10);

    };

    this.closeTranslation = function () {
        this.hideDiv("mainPop");
    };

    this.showDiv = function (id) {
        console.log("show: " + id);
        document.getElementById(id).style.display = "block";
        document.getElementById(id).style.visibility = "visible";
        document.getElementById(id).style.backgroundColor = "#eeeeff";
        document.getElementById(id).style.padding = "30px";
    };

    this.hideDiv = function (id) {
        console.log("hide: " + id);
        document.getElementById(id).style.display = "none";
        document.getElementById(id).style.visibility = "hidden";
    };

    this.checkTextAreaContent = function (e) {

        var v = e.value;

        if (v === "Copy text here") {
            e.value = "";
        }
    };


    this.updateFontSize = function (bigger) {

        if (bigger) {
            globalFontSize++
        } else {
            globalFontSize--
        }

        var all = document.getElementsByTagName("*");
        for (var i = 0, max = all.length; i < max; i++) {
            try {
                all[i].style.fontSize = globalFontSize + "px";
            } catch (e) {
                // to do;
            }
        }
        setCookieValue("readerFontSize", globalFontSize + "");
    };


    this.getWidth = function () {
        var screenWidth = 0;

        try {
            if (screen.width > window.innerWidth) {
                screenWidth = window.innerWidth;
            } else {
                screenWidth = screen.width;
            }
            ;
        } catch (e) {
            //log("error", "2 getWidth()", "error when positioning id:  error: " + e.description);
        }
        //console.log("screenWidth: " + screenWidth);
        //log("info", "getWidth()", "screenWidth: " + screenWidth);
        return screenWidth;
    };


    this.getHeight = function () {
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
    };

    this.toast = function (x) {

        //alert("Toast in UxUi object: " + x);
        this.makeToast(x, false);
    };


    this.makeToast = function (s, c) {

        // mmainPop

        e = document.getElementById("mainToast");

        if (c) {
            e.className = "toastDiv";
        } else {
            e.className = "toastDiv";
        }

        e.style.display = "block";
        e.innerHTML = s;

        var h = this.getHeight() - 0;
        var w = this.getWidth() - 0;

        var cw = document.getElementById("mainToast").clientWidth;
        var ch = document.getElementById('mainToast').clientHeight;

        var topD = Math.floor(0.5 * (h - ch));
        var leftD = Math.floor(0.5 * (w - cw));

        /*
         * ToDo: here is some unfinished work. div positioned left upper corner
         * insead of properly positioned using math above
         * 
         * 
         */

        e.style.width = "50%";
        e.style.zIndex = "999";
        e.style.left = "0px";
        e.style.top = "0px";
        e.style.padding = "10px";

        setTimeout(function () {
            document.getElementById("mainToast").style.display = "none";
        }, 2000);
    };



}
