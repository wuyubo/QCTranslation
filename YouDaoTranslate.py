import requests
import os
import json
import random

youdao_languages =  \
{"Afrikaans":"af",
"Albanian":"sq",
"Amharic":"am",
"Arabic":"ar",
"Armenian":"hy",
"Azeerbaijani":"az",
"Basque":"eu",
"Belarusian":"be",
"Bengali":"bn",
"Bosnian":"bs",
"Bulgarian":"bg",
"Catalan":"ca",
"Cebuano":"ceb",
"Simplified_Chinese":"zh-CHS",
"Chinese":"zh-CHS",
"Traditional_Chinese":"zh-TW",
"Corsican":"co",
"Croatian":"hr",
"Czech":"cs",
"Danish":"da",
"Dutch":"nl",
"English":"en",
"Esperanto":"eo",
"Estonian":"et",
"Finnish":"fi",
"French":"fr",
"Frisian":"fy",
"Galician":"gl",
"Georgian":"ka",
"German":"de",
"Greek":"el",
"Gujarati":"gu",
"Haitian Creole":"ht",
"Hausa":"ha",
"Hawaiian":"haw",
"Hebrew":"iw",
"Hindi":"hi",
"Hmong":"hmn",
"Hungarian":"hu",
"Icelandic":"is",
"Igbo":"ig",
"Indonesian":"id",
"Irish":"ga",
"Italian":"it",
"Japanese":"ja",
"Javanese":"jw",
"Kannada":"kn",
"Kazakh":"kk",
"Khmer":"km",
"Korean":"ko",
"Kurdish":"ku",
"Kyrgyz":"ky",
"Lao":"lo",
"Latin":"la",
"Latvian":"lv",
"Lithuanian":"lt",
"Luxembourgish":"lb",
"Macedonian":"mk",
"Malagasy":"mg",
"Malay":"ms",
"Malayalam":"ml",
"Maltese":"mt",
"Maori":"mi",
"Marathi":"mr",
"Mongolian":"mn",
"Myanmar (Burmese)":"my",
"Nepali":"ne",
"Norwegian":"no",
"Nyanja (Chichewa)":"ny",
"Pashto":"ps",
"Persian":"fa",
"Polish":"pl",
"Portuguese":"pt",
"Portugese":"pt",
"Punjabi":"pa",
"Romanian":"ro",
"Russian":"ru",
"Samoan":"sm",
"Scots Gaelic":"gd",
"Serbian":"sr",
"Sesotho":"st",
"Shona":"sn",
"Sindhi":"sd",
"Sinhala (Sinhalese)":"si",
"Slovak":"sk",
"Slovenian":"sl",
"Somali":"so",
"Spanish":"es",
"Sundanese":"su",
"Swahili":"sw",
"Swedish":"sv",
"Tagalog (Filipino)":"tl",
"Tajik":"tg",
"Tamil":"ta",
"Telugu":"te",
"Thai":"th",
"Turkish":"tr",
"Ukrainian":"uk",
"Urdu":"ur",
"Uzbek":"uz",
"Vietnamese":"vi",
"Welsh":"cy",
"Xhosa":"xh",
"Yiddish":"yi",
"Yoruba":"yo",
"Zulu":"zu",
}


url = "http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule"
#这里的问号前面有一个 _o 要删掉

agent_list = [
     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
     "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0 Safari/537.36 OPR/15.0",
     "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.1 (KHTML, like Gecko) Safari/535.1 Chrome/14.0.835.202 360EE"
]
user_agent = random.choice(agent_list)
#这个爬虫用不到 header ，但可以加深练习，而且这里的 referer 放第 4 行那个 url 也行好像
header = {
    "User-Agent": user_agent,
    "Referer": "http://fanyi.youdao.com/?keyfrom=fanyi.logo"  # 从这个 url 请求过来的
}
# 最基本的只需要保留 i 和 doctype 就行了
formData = {
    'i': "translate",
    'from': 'AUTO',
    'to': 'AUTO',
    'smartresult': 'dict',
    'client': 'fanyideskweb',
    'salt': '15552145285567',
    'sign': '1bb13722dda908dda3d8738eb30fc844',
    'ts': '1555214528556',
    'bv': 'd6c3cd962e29b66abe48fcb8f4dd7f7d',
    'version': '2.1',
    'keyfrom': 'fanyi.web',
    'action': 'FY_BY_CLICKBUTTION',
    'doctype': 'json'
}

def youDaoTranslate(to_translate, to_language="AUTO", from_language="AUTO"):
    global formData
    global url
    global header

    tmp_language = youdao_languages[to_language]
    if tmp_language == "":
        to_language = "AUTO"
    else:
        to_language = tmp_language
    tmp_language = youdao_languages[from_language]
    if tmp_language == "":
        from_language = "AUTO"
    else:
        from_language = tmp_language

    formData['i'] = to_translate
    formData['from'] = from_language
    formData['to'] = to_language
    print("有道")
    print(formData['from'])
    print(formData['to'])

    response = requests.post(url,formData,header)
    content = response.text
    result = json.loads(content)  #将字符串转换成一个字典对象
    result = result.get('translateResult')[0]
    print(result)
    for i in result:
        # file_name = "翻译结果"+i['src'][0]+".txt"
        print("原文：%s" % i['src'])
        print("译文：%s" % i['tgt'])
        # with open(file_name,"wb") as f:
        # f.write(i['tgt'])   # TypeError: a bytes-like object is required, not 'str'
        # f.write(i['tgt'].content)     # AttributeError: 'str' object has no attribute 'content'
        print("---------------------------------分割线----------------------------------")
    return result[0]['tgt']



