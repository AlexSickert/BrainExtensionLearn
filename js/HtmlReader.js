

function Html() {
    /**
     * Creates plain text html elements that get set into the dom tree
     */


    this.getInnerHtml = function (ele) {

    };

    this.setInnerHtml = function (ele, html) {

    };


    this.getNavigationButtons = function (arrLabels, arrFunctions) {
        var txt = "";
        var i;
        for (i = 0; i < arrLabels.length; i++) {
            txt += this.getNavigationButton("navigationButton", arrLabels[i], arrFunctions[i]);
        }
        txt += "<div class=\"clear\"></div>";
        return txt + "<hr>";
    };


    this.getButtons = function (arrLabels, arrFunctions) {
        var txt = "";
        var i;
        for (i = 0; i < arrLabels.length; i++) {
            txt += this.getNavigationButton("defaultButton", arrLabels[i], arrFunctions[i]);
        }
        return txt;
    };


    this.getList = function (arrLabels, arrFunctions) {
        var txt = "<ul>";
        var i;
        for (i = 0; i < arrLabels.length; i++) {
            txt += this.getListitem("defaultListItem", arrLabels[i], arrFunctions[i]);
        }

        txt += "</ul>";
        return txt;
    };



    this.getListitem = function (style, label, functionStr) {

        return "<li class=\"" + style + "\" onclick=\"" + functionStr + "\">" + label + "</li>";

    };

    this.getNavigationButton = function (style, label, functionStr) {

        return "<div class=\"" + style + "\" onclick=\"" + functionStr + "\">" + label + "</div>";

    };


    this.getBodyFloatButtonList = function (arrLabels, arrFunctions) {
        return this.getList(arrLabels, arrFunctions);
    };

    this.getBodyFloatContainer = function (style, html) {
        return "<div class=\"" + style + "\" >" + html + "</div>";
    };


    this.getBodyIframe = function (label, url) {
        var s = '<iframe  width="300" height="200" src="' + url + '"></iframe>';
        return s;
    };

    this.getBodyTextAreaForm = function (language, label, url, f, fLabel) {

        var s = language;
        s += "<br>" + label;
        s += "<br>" + url;
        s += "<br><input type=\"button\" onclick=\"" + f + "\" value=\"" + fLabel + "\">";
        s += "<br><textarea id=\"textarea\" onclick=\"UxUi.checkTextAreaContent(this)\" rows=\"20\" cols=\"50\">Copy text here</textarea>";
        return s;
    };


    this.getTranslationForm = function (language, sentence, word) {

        var s = language;
        s += "<br>";
        s += "<textarea id=\"sentence\" rows=\"4\" cols=\"50\">" + sentence + "</textarea>";
        s += "<br><input type=\"button\" onclick=\"Con.translateSentence()\" value=\"Translate sentence\">";
        s += "<br>";
        s += "<textarea id=\"word\" rows=\"4\" cols=\"50\">" + word + "</textarea>";
        s += "<br><input type=\"button\" onclick=\"Con.translateWord()\" value=\"Translate word\">";
        s += "<br><textarea id=\"result\" rows=\"4\" cols=\"50\"></textarea>";
        s += "<br><input type=\"button\" onclick=\"UxUi.closeTranslation()\" value=\"CLOSE\">";
        s += "<input type=\"button\" onclick=\"Con.saveTranslation()\" value=\"SAVE\">";

        return s;
    };

    this.bold = function (s) {
        return "<b>" + s + "</b>";
    };

    this.italic = function (s) {
        return "<i>" + s + "</i>";
    };

    this.underline = function (s) {
        return "<u>" + s + "</u>";
    };






}