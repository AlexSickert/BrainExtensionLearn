import re


def remove_from_text(txt, start_string, end_string):
    continue_loop = True
    pos_start = 0
    pos_end = 0

    while continue_loop:
        pos_start = txt.find(start_string, pos_start)
        if pos_start != -1:
            pos_end = txt.find(end_string, pos_start + len(start_string))
            if pos_end != -1:
                txt_1 = txt[0:pos_start]
                txt_2 = txt[pos_end + len(end_string):len(txt)]
                txt = txt_1 + txt_2
            else:
                continue_loop = False
        else:
            continue_loop = False
    return txt


def get_inner(txt, start_string, end_string):
    continue_loop = True
    pos_start = 0
    pos_end = 0
    ret = []

    while continue_loop:
        pos_start = txt.find(start_string, pos_start)
        print("A", pos_start)
        if pos_start != -1:
            pos_end = txt.find(end_string, pos_start + len(start_string))
            print(pos_end)

            if pos_end != -1:
                txt_found = txt[pos_start + len(start_string): pos_end]
                ret.append(txt_found)
            else:
                continue_loop = False
            pos_start = pos_end + len(end_string)
            print(pos_start)
            print("----")
        else:
            continue_loop = False
    return ret


def contains(t, c):
    # print("-----------------------------------")
    # print(t)

    if c in t:
        return True
    else:
        return False


def clean(txt):
    txt = txt.replace("\n", " ")
    txt = txt.replace("\t", " ")
    txt = txt.replace("\r", " ")
    txt = txt.replace("<", " ")
    txt = txt.replace(">", " ")
    txt = txt.replace("  ", " ")
    txt_arr = txt.split(" ")
    txt = ""
    for ele in txt_arr:
        txt += str(ele).strip() + " "
    return txt


def is_repubblica_1(txt, ele):
    t1 = contains(txt, 'class="detail_title"')
    t2 = contains(txt, 'class="detail_body">')
    t3 = contains(txt, '<div class="detail_body">')
    t4 = contains(txt, 'https://www.repubblica.it')
    if t1 and t2 and t3 and t4:
        return True
    else:
        return False


def is_el_pais_1(txt, ele):
    t1 = contains(txt, 'itemprop="articleBody"')
    t2 = contains(txt, 'class="articulo-titulo')
    t3 = contains(txt, 'articulo-subtitulo')
    t4 = contains(txt, '<html lang="es">')
    if t1 and t2 and t3 and t4:
        return True
    else:
        return False


def process_repubblica_1(txt):
    print("is republia!")
    title = get_inner(txt, '<h1 class="detail_title">', '</h1')
    # print(title[0])
    summary = get_inner(txt, '<div class="detail_summary">', '</div')
    # print(summary[0])
    txt = remove_from_text(txt, '<div id="adv-Bottom">', '</div>')
    txt = remove_from_text(txt, '<a href', '</a>')
    txt = txt.replace("<br />", " ")
    content = get_inner(txt, '<div class="detail_body">', '</div')
    # print(content[0])
    full_text = ""
    if len(title) > 0:
        full_text += title[0] + " || "
    if len(summary) > 0:
        full_text += summary[0] + " || "
    if len(content) > 0:
        full_text += content[0] + " || "

    full_text = clean(full_text)
    print(full_text)


def el_pais_cleaner(txt):
    txt = txt.replace("<h3>", " ")
    txt = txt.replace("</h3>", " ")
    txt = txt.replace("<strong>", " ")
    txt = txt.replace("</strong>", " ")
    txt = remove_from_text(txt, '<section class="sumario', '</section>')
    txt = txt.replace("<em>", " ")
    txt = txt.replace("</em>", " ")
    txt = remove_from_text(txt, '<', '>')
    return txt


def process_el_pais_1(txt):
    print("is_el_pais_1")
    title = get_inner(txt, '<h1 class="articulo-titulo " id="articulo-titulo" itemprop="headline">', '</h1')
    summary = get_inner(txt, '<h2  itemprop="alternativeHeadline"  class="articulo-subtitulo">', '</h2')
    txt = remove_from_text(txt, '<div class="apoyos">', '</div>')
    txt = remove_from_text(txt, '<div class="sumario-texto">', '</div>')
    txt = remove_from_text(txt, '<div class="sumario__interior">', '</div>')
    txt = remove_from_text(txt, '<section class="sumario_apoyos', '</section>')
    #  <div class="articulo-cuerpo" id="cuerpo_noticia" itemprop="articleBody">
    # <div class="apoyos">
    content = get_inner(txt, '<div class="articulo-cuerpo" id="cuerpo_noticia" itemprop="articleBody">', '</div')
    content = remove_from_text(content[0], '<a href', '>')
    content = content.replace("</a>", " ")
    content = content.replace("<p>", "\n\n")
    content = content.replace("</p>", "\n\n")
    content = el_pais_cleaner(content)
    # print(content[0])
    full_text = ""
    if len(title) > 0:
        full_text += title[0] + " || "
    if len(summary) > 0:
        full_text += summary[0] + " || "
    if len(content) > 0:
        full_text += content[0] + " || "
    full_text = clean(full_text)
    print(full_text)


def is_el_pais_brazil_1(txt, ele):
    # https://brasil.elpais.com
    t1 = contains(txt, 'itemprop="articleBody"')
    t2 = contains(txt, 'class="articulo-titulo')
    t3 = contains(txt, 'articulo-subtitulo')
    t4 = contains(txt, '<html lang="pt-br">')
    if t1 and t2 and t3 and t4:
        return True  # https://www.programcreek.com/python/example/54068/html5lib.parse
    else:
        return False


def process_el_pais_brazil_1(txt):
    print("is_el_pais_brazil_1")
    title = get_inner(txt, '<h1 class="articulo-titulo " id="articulo-titulo" itemprop="headline">', '</h1')
    summary = get_inner(txt, '<h2  itemprop="alternativeHeadline"  class="articulo-subtitulo">', '</h2')
    txt = remove_from_text(txt, '<div class="apoyos">', '</div>')
    txt = remove_from_text(txt, '<div class="sumario-texto">', '</div>')
    txt = remove_from_text(txt, '<div class="sumario__interior">', '</div>')
    txt = remove_from_text(txt, '<section class="sumario_apoyos', '</section>')
    #  <div class="articulo-cuerpo" id="cuerpo_noticia" itemprop="articleBody">
    # <div class="apoyos">
    content = get_inner(txt, '<div class="articulo-cuerpo" id="cuerpo_noticia" itemprop="articleBody">', '</div')
    content = remove_from_text(content[0], '<a href', '>')
    content = content.replace("</a>", " ")
    content = content.replace("<p>", "\n\n")
    content = content.replace("</p>", "\n\n")
    content = el_pais_cleaner(content)
    # print(content[0])
    full_text = ""
    if len(title) > 0:
        full_text += title[0] + " || "
    if len(summary) > 0:
        full_text += summary[0] + " || "
    if len(content) > 0:
        full_text += content[0] + " || "
    full_text = clean(full_text)
    print(full_text)


def is_folha_portuguese_1(txt):
    # https://brasil.elpais.com
    t1 = contains(txt, 'lass="news__title"')
    t2 = contains(txt, 'class="news__subtitle"')
    t3 = contains(txt, 'lang="pt-BR"')

    if t1 and t2 and t3:
        return True  # https://www.programcreek.com/python/example/54068/html5lib.parse
    else:
        return False


def get_folha_portuguese_1(t):
    t = remove_from_text(t, '<ul class="horoscope-aside__list">', '</ul>')
    t = remove_from_text(t, '<a', '>')
    t = t.replace("</a>", "")
    arr = get_inner(t, "<p>", "</p>")
    cont = " ".join(arr)

    tit = get_inner(t, '<h1 class="news__title">', '</h1>')
    sub_tit = get_inner(t, '<p class="news__subtitle">', '</p>')

    full_text = ""
    if len(tit) > 0:
        full_text += tit[0] + " || "
    if len(sub_tit) > 0:
        full_text += sub_tit[0] + " || "

    print(full_text)

    return tit, sub_tit, cont




def parse(txt, language, source):


    if "ital" in str(language).lower():

        if is_repubblica_1(txt, source):
            print(source, "is republica " )
            process_repubblica_1(txt)
        else:
            print("error in ital "  + source)
            #exit(0)

    elif "span" in str(language).lower():

        if is_el_pais_1(txt, source):
            print(source, "is el pais spanish "  + source)
            process_el_pais_1(txt)
        else:
            print("error in span")
            #exit(0)

    elif "port" in str(language).lower():

        if is_el_pais_brazil_1(txt, source):
            print(source, "is el pais brazil")
            process_el_pais_brazil_1(txt)
        elif is_folha_portuguese_1(txt):
            print(source, "is folha")
            get_folha_portuguese_1(txt)
        else:
            print("ERROR in bras " + source)
            #exit(0)

    else:
        print("not implemented yet "  + source)
        #exit(0)



#
# def remove_from_text(txt, start_string, end_string):
#     continue_loop = True
#     pos_start = 0
#     pos_end = 0
#
#     while continue_loop:
#
#         pos_start = txt.find(start_string, pos_start)
#
#         if pos_start != -1:
#
#             pos_end = txt.find(end_string, pos_start + len(start_string))
#
#             if pos_end != -1:
#
#                 txt_1 = txt[0:pos_start]
#                 txt_2 = txt[pos_end + len(end_string):len(txt)]
#
#                 txt = txt_1 + txt_2
#             else:
#                 continue_loop = False
#         else:
#             continue_loop = False
#
#     return txt
#
#
# def check(t, c):
#     print("-----------------------------------")
#     print(t)
#     return
#     if c in t:
#         print("OK")
#     else:
#
#         print("ERROR")
#
#
# def parse_kommersant(txt):
#     txt = txt.replace(">>>", " ")
#     txt = txt.replace(">", "> ")
#     txt = txt.replace("<", " <")
#     txt = txt.replace("< ", "<")
#     txt = txt.replace(" >", ">")
#     txt = remove_from_text(txt, "<script", "</script>")
#     txt = remove_from_text(txt, "<iframe", "</iframe>")
#     # print(txt)
#
#     check(txt, "альбомов")
#     txt = remove_from_text(txt, 'class="', '"')
#     check(txt, "альбомов")
#     txt = remove_from_text(txt, 'style="', '"')
#     txt = remove_from_text(txt, 'rel="', '"')
#     check(txt, "альбомов")
#     txt = remove_from_text(txt, 'href="', '"')
#     check(txt, "альбомов")
#     txt = remove_from_text(txt, 'src="', '"')
#     check(txt, "альбомов")
#     txt = remove_from_text(txt, 'id="', '"')
#     txt = remove_from_text(txt, 'target="', '"')
#     check(txt, "альбомов")
#     txt = remove_from_text(txt, '<!--', '-->')
#     check(txt, "альбомов")
#     txt = remove_from_text(txt, '<svg', '</svg>')
#     check(txt, "альбомов")
#     # print(txt)
#     # txt = remove_from_text(txt, '<li', '</li>')
#     check(txt, "альбомов")
#     # txt = remove_from_text(txt, '<ul', '</ul>')
#     txt = remove_from_text(txt, '<footer', '</footer>')
#     txt = remove_from_text(txt, '<img', '>')
#     txt = remove_from_text(txt, '<button', '>')
#     txt = remove_from_text(txt, '<input', '>')
#     txt = remove_from_text(txt, '</button', '>')
#     #
#     # txt = remove_from_text(txt, '<li', '</li>')
#     #    txt = remove_from_text(txt, '</li', '>')
#     #    check(txt, "альбомов")
#     #
#     #    txt = remove_from_text(txt, '//', '\n')
#     #
#     txt = remove_from_text(txt, '<', '>')
#     txt = txt.replace("\n", " ")
#     txt = txt.replace("     ", "\n")
#
#     txt = txt.replace("{", " {")
#     txt = txt.replace("}", "}")
#     txt = txt.replace(";", "; ")
#     txt = txt.replace(":", ": ")
#
#     check(txt, "одиннадцать уже сочинял")
#
#     return txt
#
#
# def parse_el_pais(txt):
#
#     txt = txt.replace(">>>", " ")
#     txt = txt.replace(">", "> ")
#     txt = txt.replace("<", " <")
#     txt = txt.replace("< ", "<")
#     txt = txt.replace(" >", ">")
#     txt = remove_from_text(txt, "<script", "</script>")
#     # print(txt)
#
#     #check(txt, "альбомов")
#     txt = remove_from_text(txt, 'class="', '"')
#     #check(txt, "альбомов")
#     txt = remove_from_text(txt, 'style="', '"')
#     txt = remove_from_text(txt, 'rel="', '"')
#     #check(txt, "альбомов")
#     txt = remove_from_text(txt, 'href="', '"')
#     #check(txt, "альбомов")
#     txt = remove_from_text(txt, 'src="', '"')
#     #check(txt, "альбомов")
#     txt = remove_from_text(txt, 'id="', '"')
#     #check(txt, "альбомов")
#     txt = remove_from_text(txt, '<!--', '-->')
#     #check(txt, "альбомов")
#     txt = remove_from_text(txt, '<svg', '</svg>')
#     #check(txt, "альбомов")
#     # print(txt)
#     txt = remove_from_text(txt, '<li', '</li>')
#     #check(txt, "альбомов")
#     txt = remove_from_text(txt, '<ul', '</ul>')
#     txt = remove_from_text(txt, '<footer', '</footer>')
#     txt = remove_from_text(txt, '<img', '>')
#     txt = remove_from_text(txt, '<button', '>')
#     txt = remove_from_text(txt, '</button', '>')
#
#     txt = remove_from_text(txt, '<li', '>')
#     txt = remove_from_text(txt, '</li', '>')
#     #check(txt, "альбомов")
#
#     txt = remove_from_text(txt, '//', '\n')
#
#     txt = remove_from_text(txt, '<', '>')
#     txt = txt.replace("\n", " ")
#     txt = txt.replace("     ", "\n")
#
#     txt = txt.replace("{", " {")
#     txt = txt.replace("}", "}")
#     txt = txt.replace(";", "; ")
#     txt = txt.replace(":", ": ")
#
#     #check(txt, "одиннадцать уже сочинял")
#
#     return txt
#
# def parse_default(txt):
#
#     txt = html_2_text_for_reading(txt)
#
#     # txt = txt.replace(">>>", " ")
#     # txt = txt.replace(">", "> ")
#     # txt = txt.replace("<", " <")
#     # txt = txt.replace("< ", "<")
#     # txt = txt.replace(" >", ">")
#     # txt = remove_from_text(txt, "<script", "</script>")
#     #
#     #
#     # txt = remove_from_text(txt, 'class="', '"')
#     #
#     # txt = remove_from_text(txt, 'style="', '"')
#     # txt = remove_from_text(txt, 'rel="', '"')
#     #
#     # txt = remove_from_text(txt, 'href="', '"')
#     #
#     # txt = remove_from_text(txt, 'src="', '"')
#     #
#     # txt = remove_from_text(txt, 'id="', '"')
#     #
#     # txt = remove_from_text(txt, '<!--', '-->')
#     #
#     # txt = remove_from_text(txt, '<svg', '</svg>')
#     #
#     # txt = remove_from_text(txt, '<li', '</li>')
#     # #check(txt, "альбомов")
#     # txt = remove_from_text(txt, '<ul', '</ul>')
#     # txt = remove_from_text(txt, '<footer', '</footer>')
#     # txt = remove_from_text(txt, '<img', '>')
#     # txt = remove_from_text(txt, '<button', '>')
#     # txt = remove_from_text(txt, '</button', '>')
#     #
#     # txt = remove_from_text(txt, '<li', '>')
#     # txt = remove_from_text(txt, '</li', '>')
#     #
#     # txt = remove_from_text(txt, '//', '\n')
#     #
#     # txt = remove_from_text(txt, '<', '>')
#     # txt = txt.replace("\n", " ")
#     # txt = txt.replace("\r", " ")
#     # txt = txt.replace("\t", " ")
#     # txt = txt.replace("     ", "\n")
#     #
#     # txt = txt.replace("{", " {")
#     # txt = txt.replace("}", "}")
#     # txt = txt.replace(";", "; ")
#     # txt = txt.replace(":", ": ")
#     #
#     # txt = re.sub(' +', '@', txt, re.UNICODE|re.MULTILINE)
#     # txt = re.sub(u'\n', '@', txt, re.UNICODE | re.MULTILINE)
#     # txt = re.sub(u'\t', '@', txt, re.UNICODE | re.MULTILINE)
#     # txt = re.sub(u'\r', '@', txt, re.UNICODE | re.MULTILINE)
#     # txt = re.sub(u' +', '@', txt, re.UNICODE | re.MULTILINE)
#     # txt = re.sub(' +', '@', txt, re.UNICODE | re.MULTILINE)
#
#     txt = txt.replace(u"\u0020", " ")
#     txt = txt.replace(u"\u2001", " ")
#     txt = txt.replace(u"\u2002", " ")
#     txt = txt.replace(u"\u2003", " ")
#     txt = txt.replace(u"\u2004", " ")
#     txt = txt.replace(u"\u2005", " ")
#     txt = txt.replace(u"\u2006", " ")
#     txt = txt.replace(u"\u2007", " ")
#     txt = txt.replace(u"\u2008", " ")
#     txt = txt.replace(u"\u2009", " ")
#     txt = txt.replace(u"\u2006", " ")
#     txt = txt.replace(u"\u200A", " ")
#     txt = txt.replace(u"\u200B", " ")
#     txt = txt.replace(u"\u202F", " ")
#     txt = txt.replace(u"\u205F", " ")
#     txt = txt.replace(u"\u2000", " ")
#     txt = txt.replace(u"\u3000", " ")
#     txt = txt.replace(u"\uFEFF", " ")
#
#     txt = txt.replace(u"\u00A0", " ")
#     txt = txt.replace(u"\u1680", " ")
#     txt = txt.replace(u"\u180E", " ")
#
#     arr = txt.split(" ")
#
#     s = ""
#     for ele in arr:
#         if len(str(ele)) > 0:
#             s += " " + str(ele).strip()
#
#     txt = s
#
#     f = open("trash_default.txt", "r")
#     trash = f.read()
#     f.close()
#     #trash = re.sub(' +', ' ', trash)
#
#     arr = trash.split(" ")
#
#     s = ""
#     for ele in arr:
#         if len(str(ele)) > 0:
#             s += " " + str(ele).strip()
#
#     trash = [s]
#
#     bigrams = [b for l in trash for b in zip(l.split(" ")[:-1], l.split(" ")[1:])]
#
#     for bigram in bigrams:
#         print(bigram)
#         x = " ".join(bigram)
#         print(x)
#         txt = txt.replace(x, "")
#
#     return txt.strip()
#
# def html_2_text_for_reading(html):
#
#     spacer = "8Sh6Sw5Wb4Ee9Mi2Rd2R"
#
#     txt = str(html) + " "
#
#     txt = txt.replace("<p", spacer + "<p")
#     txt = txt.replace("<div", spacer + "<div")
#
#     txt = re.sub(r"<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>", "", txt)
#     txt = re.sub(r"<style\b[^<]*(?:(?!<\/style>)<[^<]*)*<\/style>", "", txt)
#     txt = re.sub(r"<.+?>", " ", txt)
#
#     #txt = re.sub(r",", " ", txt)
#     # txt = re.sub(r""", " ", txt)
#     #txt = re.sub(r"»", " ", txt)
#     #txt = re.sub(r"«", " ", txt)
#     #txt = re.sub(r"\.", " ", txt)
#     #txt = re.sub(r":", " ", txt)
#     #txt = re.sub(r"#", " ", txt)
#     #txt = re.sub(r"=", " ", txt)
#     #txt = re.sub(r"\(", " ", txt)
#     #txt = re.sub(r"\)", " ", txt)
#     #txt = re.sub(r"\[", " ", txt)
#     #txt = re.sub(r"\]", " ", txt)
#     txt = re.sub(r"\n", " ", txt)
#     #txt = re.sub(r""", " ", txt)
#     txt = re.sub(r"&rsquo;", "'", txt)
#     txt = re.sub(r"&raquo;", " ", txt)
#     txt = re.sub(r"&laquo;", " ", txt)
#     txt = re.sub(r"&Agrave;", "À", txt)
#     txt = re.sub(r"&Aacute;", "Á", txt)
#     txt = re.sub(r"&Acirc;", "Â", txt)
#     txt = re.sub(r"&Atilde;", "Ã", txt)
#     txt = re.sub(r"&Auml;", "Ä", txt)
#     txt = re.sub(r"&Aring;", "Å", txt)
#     txt = re.sub(r"&AElig;", "Æ", txt)
#     txt = re.sub(r"&Ccedil;", "Ç", txt)
#     txt = re.sub(r"&Egrave;", "È", txt)
#     txt = re.sub(r"&Eacute;", "É", txt)
#     txt = re.sub(r"&Ecirc;", "Ê", txt)
#     txt = re.sub(r"&Euml;", "Ë", txt)
#     txt = re.sub(r"&Igrave;", "Ì", txt)
#     txt = re.sub(r"&Iacute;", "Í", txt)
#     txt = re.sub(r"&Icirc;", "Î", txt)
#     txt = re.sub(r"&Iuml;", "Ï", txt)
#     txt = re.sub(r"&ETH;", "Ð", txt)
#     txt = re.sub(r"&Ntilde;", "Ñ", txt)
#     txt = re.sub(r"&Ograve;", "Ò", txt)
#     txt = re.sub(r"&Oacute;", "Ó", txt)
#     txt = re.sub(r"&Ocirc;", "Ô", txt)
#     txt = re.sub(r"&Otilde;", "Õ", txt)
#     txt = re.sub(r"&Ouml;", "Ö", txt)
#     txt = re.sub(r"&times;", "×", txt)
#     txt = re.sub(r"&Oslash;", "Ø", txt)
#     txt = re.sub(r"&Ugrave;", "Ù", txt)
#     txt = re.sub(r"&Uacute;", "Ú", txt)
#     txt = re.sub(r"&Ucirc;", "Û", txt)
#     txt = re.sub(r"&Uuml;", "Ü", txt)
#     txt = re.sub(r"&Yacute;", "Ý", txt)
#     txt = re.sub(r"&THORN;", "Þ", txt)
#     txt = re.sub(r"&szlig;", "ß", txt)
#     txt = re.sub(r"&agrave;", "à", txt)
#     txt = re.sub(r"&aacute;", "á", txt)
#     txt = re.sub(r"&acirc;", "â", txt)
#     txt = re.sub(r"&atilde;", "ã", txt)
#     txt = re.sub(r"&auml;", "ä", txt)
#     txt = re.sub(r"&aring;", "å", txt)
#     txt = re.sub(r"&aelig;", "æ", txt)
#     txt = re.sub(r"&ccedil;", "ç", txt)
#     txt = re.sub(r"&egrave;", "è", txt)
#     txt = re.sub(r"&eacute;", "é", txt)
#     txt = re.sub(r"&ecirc;", "ê", txt)
#     txt = re.sub(r"&euml;", "ë", txt)
#     txt = re.sub(r"&igrave;", "ì", txt)
#     txt = re.sub(r"&iacute;", "í", txt)
#     txt = re.sub(r"&icirc;", "î", txt)
#     txt = re.sub(r"&iuml;", "ï", txt)
#     txt = re.sub(r"&eth;", "ð", txt)
#     txt = re.sub(r"&ntilde;", "ñ", txt)
#     txt = re.sub(r"&ograve;", "ò", txt)
#     txt = re.sub(r"&oacute;", "ó", txt)
#     txt = re.sub(r"&ocirc;", "ô", txt)
#     txt = re.sub(r"&otilde;", "õ", txt)
#     txt = re.sub(r"&ouml;", "ö", txt)
#     txt = re.sub(r"&divide;", "÷", txt)
#     txt = re.sub(r"&oslash;", "ø", txt)
#     txt = re.sub(r"&ugrave;", "ù", txt)
#     txt = re.sub(r"&uacute;", "ú", txt)
#     txt = re.sub(r"&ucirc;", "û", txt)
#     txt = re.sub(r"&uuml;", "ü", txt)
#     txt = re.sub(r"&yacute;", "ý", txt)
#     txt = re.sub(r"&thorn;", "þ", txt)
#     txt = re.sub(r"&yuml;", "ÿ", txt)
#     txt = re.sub(r"&nbsp;", " ", txt)
#     txt = re.sub(r"&#9642;", "", txt)  # black small square
#
#     #txt = txt.replace("!", " ")
#     #txt = txt.replace("?", " ")
#     txt = txt.replace("<", " ")
#     txt = txt.replace(">", " ")
#     txt = txt.replace("\\", " ")
#     txt = txt.replace("/", " ")
#     txt = txt.replace("+", " ")
#     #txt = txt.replace(";", " ")  # deactivated because we need it for the url encoded special character liek &quot;
#     txt = txt.replace(",", " ")
#     txt = txt.replace('"', " ")
#
#     txt = txt.replace(spacer, " ")
#
#     return txt
#


def html_2_text(html):

    spacer = "8Sh6Sw5Wb4Ee9Mi2Rd2R"

    txt = str(html) + " "

    txt = txt.replace("<p", spacer + "<p")
    txt = txt.replace("<div", spacer + "<div")

    txt = re.sub(r"<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>", "", txt)
    txt = re.sub(r"<style\b[^<]*(?:(?!<\/style>)<[^<]*)*<\/style>", "", txt)
    txt = re.sub(r"<.+?>", " ", txt)

    txt = re.sub(r",", " ", txt)
    # txt = re.sub(r""", " ", txt)
    txt = re.sub(r"»", " ", txt)
    txt = re.sub(r"«", " ", txt)
    txt = re.sub(r"\.", " ", txt)
    txt = re.sub(r":", " ", txt)
    txt = re.sub(r"#", " ", txt)
    txt = re.sub(r"=", " ", txt)
    txt = re.sub(r"\(", " ", txt)
    txt = re.sub(r"\)", " ", txt)
    txt = re.sub(r"\[", " ", txt)
    txt = re.sub(r"\]", " ", txt)
    txt = re.sub(r"\n", " ", txt)
    #txt = re.sub(r""", " ", txt)
    txt = re.sub(r"&rsquo;", "'", txt)
    txt = re.sub(r"&raquo;", " ", txt)
    txt = re.sub(r"&laquo;", " ", txt)
    txt = re.sub(r"&Agrave;", "À", txt)
    txt = re.sub(r"&Aacute;", "Á", txt)
    txt = re.sub(r"&Acirc;", "Â", txt)
    txt = re.sub(r"&Atilde;", "Ã", txt)
    txt = re.sub(r"&Auml;", "Ä", txt)
    txt = re.sub(r"&Aring;", "Å", txt)
    txt = re.sub(r"&AElig;", "Æ", txt)
    txt = re.sub(r"&Ccedil;", "Ç", txt)
    txt = re.sub(r"&Egrave;", "È", txt)
    txt = re.sub(r"&Eacute;", "É", txt)
    txt = re.sub(r"&Ecirc;", "Ê", txt)
    txt = re.sub(r"&Euml;", "Ë", txt)
    txt = re.sub(r"&Igrave;", "Ì", txt)
    txt = re.sub(r"&Iacute;", "Í", txt)
    txt = re.sub(r"&Icirc;", "Î", txt)
    txt = re.sub(r"&Iuml;", "Ï", txt)
    txt = re.sub(r"&ETH;", "Ð", txt)
    txt = re.sub(r"&Ntilde;", "Ñ", txt)
    txt = re.sub(r"&Ograve;", "Ò", txt)
    txt = re.sub(r"&Oacute;", "Ó", txt)
    txt = re.sub(r"&Ocirc;", "Ô", txt)
    txt = re.sub(r"&Otilde;", "Õ", txt)
    txt = re.sub(r"&Ouml;", "Ö", txt)
    txt = re.sub(r"&times;", "×", txt)
    txt = re.sub(r"&Oslash;", "Ø", txt)
    txt = re.sub(r"&Ugrave;", "Ù", txt)
    txt = re.sub(r"&Uacute;", "Ú", txt)
    txt = re.sub(r"&Ucirc;", "Û", txt)
    txt = re.sub(r"&Uuml;", "Ü", txt)
    txt = re.sub(r"&Yacute;", "Ý", txt)
    txt = re.sub(r"&THORN;", "Þ", txt)
    txt = re.sub(r"&szlig;", "ß", txt)
    txt = re.sub(r"&agrave;", "à", txt)
    txt = re.sub(r"&aacute;", "á", txt)
    txt = re.sub(r"&acirc;", "â", txt)
    txt = re.sub(r"&atilde;", "ã", txt)
    txt = re.sub(r"&auml;", "ä", txt)
    txt = re.sub(r"&aring;", "å", txt)
    txt = re.sub(r"&aelig;", "æ", txt)
    txt = re.sub(r"&ccedil;", "ç", txt)
    txt = re.sub(r"&egrave;", "è", txt)
    txt = re.sub(r"&eacute;", "é", txt)
    txt = re.sub(r"&ecirc;", "ê", txt)
    txt = re.sub(r"&euml;", "ë", txt)
    txt = re.sub(r"&igrave;", "ì", txt)
    txt = re.sub(r"&iacute;", "í", txt)
    txt = re.sub(r"&icirc;", "î", txt)
    txt = re.sub(r"&iuml;", "ï", txt)
    txt = re.sub(r"&eth;", "ð", txt)
    txt = re.sub(r"&ntilde;", "ñ", txt)
    txt = re.sub(r"&ograve;", "ò", txt)
    txt = re.sub(r"&oacute;", "ó", txt)
    txt = re.sub(r"&ocirc;", "ô", txt)
    txt = re.sub(r"&otilde;", "õ", txt)
    txt = re.sub(r"&ouml;", "ö", txt)
    txt = re.sub(r"&divide;", "÷", txt)
    txt = re.sub(r"&oslash;", "ø", txt)
    txt = re.sub(r"&ugrave;", "ù", txt)
    txt = re.sub(r"&uacute;", "ú", txt)
    txt = re.sub(r"&ucirc;", "û", txt)
    txt = re.sub(r"&uuml;", "ü", txt)
    txt = re.sub(r"&yacute;", "ý", txt)
    txt = re.sub(r"&thorn;", "þ", txt)
    txt = re.sub(r"&yuml;", "ÿ", txt)
    txt = re.sub(r"&nbsp;", " ", txt)
    txt = re.sub(r"&#9642;", "", txt)  # black small square

    txt = txt.replace("!", " ")
    txt = txt.replace("?", " ")
    txt = txt.replace("<", " ")
    txt = txt.replace(">", " ")
    txt = txt.replace("\\", " ")
    txt = txt.replace("/", " ")
    txt = txt.replace("+", " ")
    #txt = txt.replace(";", " ")  # deactivated because we need it for the url encoded special character liek &quot;
    txt = txt.replace(",", " ")
    txt = txt.replace('"', " ")

    txt = txt.replace(spacer, " ")

    return txt
