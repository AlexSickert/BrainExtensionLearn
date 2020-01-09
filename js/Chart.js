

function Chart() {

    this.xAxis = 0; // the y value of the x axis
    this.numBars = 0;
    this.maxVal = 0;
    this.w = 0;
    this.h = 0;
    this.space = 0;
    this.widthBar = 0;
    this.widthTotalBar = 0;
    this.topBarSpace = 0;
    this.fontSize = 0;

    this.drawBarChart = function (ele, valArr, labelArr) {

        // minimalistic bar chart
        this.setUp(ele, valArr, labelArr);
        this.drawAxisX(ele);

        for (var i = 0; i < valArr.length; i++) {
            this.drawOneBar(ele, valArr[i], labelArr[i], i);
        }
    };

    this.setUp = function (ele, valArr, labelArr) {
        // some initial work like defining drawing space and location of axis
        this.numBars = valArr.length;
        this.h = ele.clientHeight;
        this.w = ele.clientWidth;
        this.xAxis = Math.floor(this.h * 0.95);
        this.topBarSpace = this.h - this.xAxis;
        // calculate bar width and spaces between bar
        this.widthTotalBar = Math.floor(this.w / this.numBars);
        this.widthBar = Math.floor(this.widthTotalBar * 0.8);
        this.space = Math.floor(this.widthTotalBar * 0.1); // space left and right of bar
        this.fontSize = Math.floor(this.h / 30);

        for (var i = 0; i < valArr.length; i++) {
            if (valArr[i] > this.maxVal) {
                this.maxVal = valArr[i];
            }
        }
    };

    this.drawAxisX = function (ele) {

        e = document.createElementNS('http://www.w3.org/2000/svg', 'line');
        e.setAttributeNS(null, 'x1', 0);
        e.setAttributeNS(null, 'y1', this.xAxis);
        e.setAttributeNS(null, 'x2', this.w);
        e.setAttributeNS(null, 'y2', this.xAxis);
        e.setAttributeNS(null, 'style', "stroke:#3B5998;stroke-width:1");
        ele.appendChild(e);
    };

    this.xShift = function (txt) {
        // this.fontSize
        var l = txt.length;
        var d = 0.6 * this.fontSize;
        if (l > 0) {
            return Math.floor(((l - 1) * d * 0.5) + (d / 2));
        } else {
            return 0;
        }

    };


    this.drawOneBar = function (ele, val, label, index) {
        console.log("--------------------------------");
        var factorHeight = val / this.maxVal;
        var height = Math.floor(factorHeight * (this.h - (this.h - this.xAxis) - this.topBarSpace));
        console.log(this.h);
        console.log(this.xAxis);
        console.log(this.topBarSpace);
        console.log(height);

        var e = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
        e.setAttributeNS(null, 'width', this.widthBar);
        e.setAttributeNS(null, 'height', height);
        e.setAttributeNS(null, 'x', (index * this.widthTotalBar) + this.space);
        e.setAttributeNS(null, 'y', this.xAxis - height);
        e.setAttributeNS(null, 'style', "fill:#3B5998;stroke:#3B5998;stroke-width:1;fill-opacity:1.0;stroke-opacity:1.0");
        ele.appendChild(e);

        // write number above the bar
        e = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        e.setAttributeNS(null, 'x', (index * this.widthTotalBar) + this.space + this.widthBar * 0.5 - this.xShift("" + val));
        e.setAttributeNS(null, 'y', this.xAxis - height - (this.topBarSpace * 0.15));
        e.setAttributeNS(null, 'style', "font-size:" + this.fontSize + "px;font-family:Arial;fill:#777777;");
        var txt = document.createTextNode(val);
        e.appendChild(txt);
        ele.appendChild(e);

        // write tics below bar
        e = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        e.setAttributeNS(null, 'x', (index * this.widthTotalBar) + this.space + this.widthBar * 0.5 - this.xShift("" + label));
        e.setAttributeNS(null, 'y', this.xAxis + 0.9 * (this.h - this.xAxis));
        e.setAttributeNS(null, 'style', "font-size:" + this.fontSize + "px;font-family:Arial;fill:#777777;");
        var txt = document.createTextNode(label);
        e.appendChild(txt);
        ele.appendChild(e);

    };

}