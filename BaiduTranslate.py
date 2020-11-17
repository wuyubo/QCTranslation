import requests
import os
import json
import random
import hashlib
import urllib

baidu_languages =  \
{"Afrikaans":"af",
"Albanian":"sq",
"Amharic":"am",
"Arabic":"ara",
"Armenian":"hy",
"Azeerbaijani":"az",
"Basque":"eu",
"Belarusian":"be",
"Bengali":"bn",
"Bosnian":"bs",
"Bulgarian":"bg",
"Catalan":"ca",
"Cebuano":"ceb",
"Simplified_Chinese":"zh",
"Chinese":"zh",
"Traditional_Chinese":"zh-TW",
"Corsican":"co",
"Croatian":"hr",
"Czech":"cs",
"Danish":"da",
"Dutch":"de",
"English":"en",
"Esperanto":"eo",
"Estonian":"et",
"Finnish":"fi",
"French":"fra",
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
"Japanese":"jp",
"Javanese":"jw",
"Kannada":"kn",
"Kazakh":"kk",
"Khmer":"km",
"Korean":"kor",
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
"Spanish":"spa",
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


url = "https://fanyi.baidu.com/v2transapi?"
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
    "Referer": "https://fanyi.baidu.com/v2transapi?"  # 从这个 url 请求过来的
}
# 最基本的只需要保留 i 和 doctype 就行了
formData = {
    'from': 'AUTO',
    'to': 'AUTO',
    'query': "word",
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


def create_sign(q, appid, salt, key):
    '''
    制造签名
    '''
    sign = str(appid) + str(q) + str(salt) + str(key)
    md5 = hashlib.md5()
    md5.update(sign.encode('utf-8'))
    return md5.hexdigest()


def create_url(q, url, to_language, from_language):
    '''
    根据参数构造query字典
    '''
    fro = from_language
    to = to_language
    salt = random.randint(32768, 65536)
    appid = 20200922000570936  # 百度翻译开放平台的APP ID
    key = 'P0wfzlboXuM_rm0Gj1Nm'  # 百度翻译开放平台的密钥
    sign = create_sign(q, appid, salt, key)
    url = url + '?appid=' + str(appid) + '&q=' + urllib.parse.quote(q) + '&from=' + str(fro) + '&to=' + str(
        to) + '&salt=' + str(salt) + '&sign=' + str(sign)
    return url


def translate(q, to_language = "auto", from_language="zh"):
    url = 'http://api.fanyi.baidu.com/api/trans/vip/translate'

    tmp_language = baidu_languages[to_language]
    if tmp_language == "":
        to_language = "zh"
    else:
        to_language = tmp_language
    tmp_language = baidu_languages[from_language]
    if tmp_language == "":
        from_language = "auto"
    else:
        from_language = tmp_language
    print(from_language)
    print(to_language)
    url = create_url(q, url, to_language, from_language)
    print(url)
    r = requests.get(url)
    txt = r.json()
    if txt.get('trans_result', -1) == -1:
        print('程序已经出错，请查看报错信息：\n{}'.format(txt))
        return '翻译错误\n'

    trans_result = txt['trans_result'][0]['dst']

    print('原文:' + q)
    print('翻译:' + trans_result)

    content = q + '\n' + trans_result

    return trans_result



