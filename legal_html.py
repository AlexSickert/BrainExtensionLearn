

def get_legal():

    template = """
    
    
    
    <!DOCTYPE html>
    <html>
        <head>
            <meta charset="UTF-8">
            <title>Privacy Politc and GDPR</title>
        </head>
        
        <body>
            
            
            <br>
            
            <b>This is just a dummy text to test if all works fine</b> 
           
            <br>
            <br>
           
           
            Lorem ipsum dolor sit amet, vim tota illum aeque et. Ocurreret assueverit eam et, vix id laudem qualisque accommodare. Suscipit inciderint in vis. Ne eros singulis intellegebat eos, ut reque integre electram mei, at sed dicit nominavi neglegentur. Nostrum ullamcorper vis ne.
            <br><br>
            Ignota facilisi ei sed, eam ea meis consulatu. Falli iudicabit ea vis, ne quidam commodo inimicus vix, pro id amet commune. Habemus pertinax aliquando ne eum. Te eum alii posse, cu cum nibh expetenda prodesset, ex esse euismod vix. Ex has officiis signiferumque, aliquam nostrum an eum.
            <br><br>
            
            <b>This is a table where the first cell has a green border:</b> 
            <br><br>
            <table border=1>
                <tr>
                    <td style="border: 5px solid green;">a</td><td>b</td>
                </tr>
                <tr>
                    <td>c</td><td>d</td>
                </tr>            
            
            </table>   
            <br><br>
            
            Eam case audiam detracto ea, regione elaboraret no vim, ne has magna facete. Volumus singulis vis id, mazim fabellas indoctum te mel, pro admodum facilisi ei. Sale delicatissimi in vel, legere persius placerat ut has, vel cu sumo sint adipiscing. Choro scriptorem te his, qui veri accusamus consectetuer at. Nam omnesque deleniti at. Appareat placerat volutpat sit id. Vix ad etiam mediocritatem.
            <br><br>
            Per omnis regione disputando eu, dolore eirmod diceret cu quo, vim in meis veritus senserit. Hinc intellegat constituam id duo, vix soluta insolens no. His falli graeco abhorreant ea, duo minim disputando in, mei ei magna vitae. Nec nibh cibo deterruisset no, cum et simul dicunt noluisse.
            <br><br>
            Eos ad convenire euripidis, eum partem vocent facilis te. Per intellegebat conclusionemque te, erat recusabo disputa...
            Ignota facilisi ei sed, eam ea meis consulatu. Falli iudicabit ea vis, ne quidam commodo inimicus vix, pro id amet commune. Habemus pertinax aliquando ne eum. Te eum alii posse, cu cum nibh expetenda prodesset, ex esse euismod vix. Ex has officiis signiferumque, aliquam nostrum an eum.
            <br><br>
            Ignota facilisi ei sed, eam ea meis consulatu. Falli iudicabit ea vis, ne quidam commodo inimicus vix, pro id amet commune. Habemus pertinax aliquando ne eum. Te eum alii posse, cu cum nibh expetenda prodesset, ex esse euismod vix. Ex has officiis signiferumque, aliquam nostrum an eum.
            <br>
           
           
            <br>
        </body>

    </html>
    
    
    
    """


    ret = bytearray()
    ret.extend(map(ord, template))

    return ret
