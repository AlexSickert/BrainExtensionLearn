

def get_report(url):

    template = """
    
    
    
    <!DOCTYPE html>
    <html>
        <head>
            <meta charset="UTF-8">
            <title>Title of the document</title>
        </head>
        
        <body>
            
            A simple Report example for Julia
            <br>
            
            your url is #url#
            
            <br>
            
            <b>This is a table where the first cell has a green border:</b> 
            <br>
            <table border=1>
                <tr>
                    <td style="border: 5px solid green;">a</td><td>b</td>
                </tr>
                <tr>
                    <td>c</td><td>d</td>
                </tr>            
            
            </table>   
            <br>
            and this is an image
            <br>
            <img src="/top-image-1.jpg" alt="hello" style="width: 30%; border: 2px solid red">
            <br>
            and another image
            <br>
            <img src="/mobile-screenshot.png" alt="hello" style="width: 30%; border: 2px solid blue">
            <br>
        </body>

    </html>
    
    
    
    """

    template = template.replace("#url#", url)


    ret = bytearray()
    ret.extend(map(ord, template))

    return ret
