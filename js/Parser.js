/**
 * The purpose of the parser is to convert a text into three parts: 
 * 1. split into word
 * 2. split into sentences
 * 3. creat a text where all words are clickable
 */


function Parser() {

    var textHtml = [];
    var arrWords;
    var arrSentences = [];
    var wordPos = 0;

    this.parse = function (inputString) {

        this.wordPos = 0;
        this.textHtml = "";
        this.arrWords = [];
        this.arrSentences = [];

        var paragraphs = this.parseParagraphs(inputString);

        for (var i = 0; i < paragraphs.length; i++) {
            this.parseParagraph(paragraphs[i]);
            // after each paragraph we make a line break
            this.arrSentences.push("---new-line-break---");
        }

        for (var x = 0; x < this.arrSentences.length; x++) {
            this.parseSentence(this.arrSentences[x], x);
        }

        //console.log(this.textHtml);

    };

    this.getHtml = function () {
        return this.textHtml;
    };

    this.getWord = function (i) {
        return this.arrWords[i];
    };


    this.getSentence = function (i) {
        return this.arrSentences[i];
    };

    this.addMakeWordHtml = function (txt, sentence, word) {
        if (txt.length > 0) {
            if (txt.includes("---new-line-break---")) {
                console.log("adding line break");
                this.textHtml += "<div class=\"clear\"></div><br>";
            } else {
                var s = "<div class=\"textWord\" ";
                s += "onclick=\"UxUi.st(" + sentence + "," + word + ", this)\" ";
                s += ">" + txt + "</div>";
                this.textHtml += s;
            }
        }
    };

    this.parseSentence = function (inputString, i) {

        console.log("------------- sentence ------------");
        console.log("|" + inputString + "|" + inputString.length);

        inputString = inputString.trim();

        if (inputString.length > 0) {

            if (inputString.includes(" ")) {
                // split the string
                var tmp = inputString.split(" ");
                for (var x = 0; x < tmp.length; x++) {

                    this.addMakeWordHtml(tmp[x], i, this.wordPos);
                    this.arrWords.push(tmp[x]);
                    this.wordPos += 1;
                }

            } else {
                this.addMakeWordHtml(inputString, i, this.wordPos);
                this.arrWords.push(inputString);
                this.wordPos += 1;
            }
        } else {
            //this.addMakeWordHtml("---new-line-break---", i, 0);
//            this.arrWords.push("---new-line-break---");
//            this.wordPos += 1;
        }

    };


    this.parseParagraph = function (inputString) {
        // split a paragraph into sentences by scanning for !?.
        var nextChunk = 1;
        var startPos = 0;
        var endPos = inputString.length;
        var fragment = "";
        var sentences = [];
        var tmp;
        var lc = 0;

        fragment = inputString.slice(startPos, endPos);

        while (nextChunk > 0 && lc < 500) {
            //console.log("------------- paragraph ------------");

            nextChunk = this.findSencenceEnd(fragment);
            //console.log("nextChunk = " + nextChunk);
            //console.log("fragment = " + fragment);

            if (nextChunk > 0) {
                //sentences.push(inputString.slice(startPos, nextChunk));
                tmp = fragment.slice(startPos, nextChunk);
                fragment = fragment.slice(nextChunk + 1, inputString.length);
                //console.log(tmp);
                this.arrSentences.push(tmp);

            } else {
                // it can happen that at the end of text is no sign.
                // we still add it so that we do not lose text
                //sentences.push(fragment);
                //console.log(fragment);
                this.arrSentences.push(fragment);
                nextChunk = -1;
            }

            lc += 1;

        }
        return sentences;
    };

    this.findSencenceEnd = function (s) {

        var endings = ["\\.", "!", ":", "\\?"];
        var tmp = -1;
        var lowest = s.length;

        for (var i = 0; i < endings.length; i++) {
            //console.log("searching for " + endings[i]);
            tmp = s.search(endings[i]);
            if (tmp > 0 && tmp < lowest) {
                lowest = tmp;
            }
        }

        if (lowest < s.length) {
            return lowest + 1;
        } else {
            return s.length;
        }
    };


    this.parseParagraphs = function (inputString) {

        var res = new Array();

        inputString = inputString.replace(/\r/g, "\n");
        inputString = inputString.replace(/\n\n\n\n/g, "\n");
        inputString = inputString.replace(/\n\n\n/g, "\n");
        inputString = inputString.replace(/\n\n/g, "\n");
        inputString = inputString.replace(/\n\n/g, "\n");

        console.log(inputString);

        // split by new line
        if (inputString.includes("\n")) {
            var resArr = inputString.split("\n");
            for (var i = 0; i < resArr.length; i++) {
                console.log("--------paragraph----------");
                console.log(resArr[i]);
                res.push(resArr[i]);
                //res.push("---new-line-break---");
            }

        } else {
            res.push(inputString);
        }

        return res;

    };





}



