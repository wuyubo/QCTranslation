# This is a sample Python script.
import sys
import requests
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QTreeWidgetItem, QTreeWidgetItemIterator
from PyQt5.QtCore  import Qt
import main_window

import threading
import xlrd
import xlwt

from tool import covert
from PyQt5.QtCore import QThread ,  pyqtSignal , QObject
import time
import images
import re

import googleTranslate
import YouDaoTranslate
import BaiduTranslate
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

path_langfile_name = 0
input_xls = 0
input_customr_xls = 0
output_xls = 0
languagesList = []
engCol = 0
chCol = 0

DB_CVTE = 0
DB_NEWOLDTRAN = 1
DB_CNPD = 2
DB_FAEPV = 3
DB_HISENSE = 4
DB_TCL = 5
DB_CAIXUN = 6
gl_tran_dbs = []

tips_string = ""

TRAN_NONE = 0
TRAN_GOING = 1
TRAN_FINISHED = 2
TRAN_FAILED = 3
translating_flag = TRAN_NONE
progress = 0
tran_task_cout = 0
mutex = threading.Lock()

MODE_CNPD = 0
MODE_CUSTOMER = 1
MODE_GOOGLE = 2
tran_Mode = MODE_CNPD

output_file = ""

tran_success_cout = 0
tran_failed_cout = 0

ext_strings = {"4:3", "14:9", "16:9", "PCM", "120 HZ", "300 HZ", "500 HZ", "1.2K HZ", "3.0K HZ", "7.5K HZ","10K HZ",\
               "BG","DK", "I","L", "L'", "PAL", "SECAM", "NTSC","1.", "2.", "3.", "xxxxxxxx", "MHL", "HDMI(MHL)",\
               "DVI","HDMI","DVI1","DVI2","DVI3","YPBPR","YPBPR1","DVD","D","AT View","TChinese","SChinese",\
               "1.0","2.0","3.0", "14+", "18+", "-->", "_", "8 ans+", "13 ans+", "16 ans+", "18 ans+", "TV-Y",\
               "TV-Y", "TV-Y7", "TV-G", "TV-PG", "TV-14", "TV-MA","Dual I","Dual II", "Dual I+II", "Sap","Nicam Dual I",\
               "Nicam Dual II","Nicam Dual I+II","OSD Game","NES Game", "JapaneseShiftJIS","YPbPr","YPbPr1", "Multi",\
               "Eeprom","0","1","2","3","4","5","6","7","8","9","0~9:", " - CI Key Update Failed - "," - HDCP Key Update Failed - ",\
               "....","TruBass","TruSurround","Eeprom","*","Uyghur","Zoom","Zoom1","Zoom2"}

id_strings = {"IDS_String_OSDGame", "IDS_String_NESGAME", "IDS_String_No_Nes_File", "IDS_String_Nes", "IDS_String_BT", "IDS_String_JS",\
              "IDS_String_Bluetooth", "IDS_String_OsdGame", "IDS_Game", "IDS_String_Bluetooth", "IDS_String_Game"}

export_count = 0

def checkIsNeedTraslation(sheet, row, col):
    value = sheet.cell_value(row, col)
    en = sheet.cell_value(row, engCol)
    style = getCellStyle(sheet, row, col)
    id = sheet.cell_value(row, 0)
    for idstr in id_strings:
        if idstr in id:
            return False
    if value == "":
        return False
    if value == " ":
        return False
    if value != en:
        return False

    if value.isupper() :
        return False
    for tr in ext_strings:
        if value == tr:
            return False
    if style == normal_style:
        return False

    if style == green_style and value == en:
        language = str(parseLanguage(sheet.cell_value(0, col)))
        google_ch_tr = translate_google(value, language, "English")
        print(value)
        if google_ch_tr == value:
            return False

    return True

class BackendThread(QThread):
    # 通过类成员对象定义信号
    update = pyqtSignal()

    # 处理业务逻辑
    def run(self):
        while True:
            #self.update.emit()
            print("update...")
            time.sleep(1)

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

def parseLanguage(cell_value):
    return cell_value[cell_value.find("-")+1:]


def createXlsStyle(color):
    pattern = xlwt.Pattern()
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    pattern.pattern_fore_colour = color  # 5 背景颜色为黄色
    # 1 = White, 2 = Red, 3 = Green, 4 = Blue, 5 = Yellow, 6 = Magenta, 7 = Cyan, 16 = Maroon,
    # 17 = Dark Green, 18 = Dark Blue, 19 = Dark Yellow , almost brown), 20 = Dark Magenta, 21 = Teal, 22 = Light Gray, 23 = Dark Gray
    style = xlwt.XFStyle()
    style.pattern = pattern
    return style

rgb_style_map = {None:1,(255, 255, 255):1, (255, 0, 0):2, (0, 255, 0):3, (0, 0 ,255):4, (255, 255, 0):5}
normal_style = createXlsStyle(1)
red_style = createXlsStyle(2)
green_style = createXlsStyle(3)
blue_style = createXlsStyle(4)
yellow_style = createXlsStyle(5)

color_style_map = {1:normal_style, 2:red_style, 3:green_style, 4:blue_style, 5:yellow_style}
def getStyleColor(color):
    return color_style_map[color]

def getStyleColorRgb(rgb):
    try:
        color = rgb_style_map[rgb]
    except Exception as e:
        print(e)
        color = 1
    #print(color)
    return color_style_map[color]

def getCellStyle(sheet, row, col):
    rgb = getbackgroundColor(sheet, row, col)
    cellStyle = getStyleColorRgb(rgb)
    return cellStyle

def isCheckLang(language):
    if language == "English":
        return False
    item = QTreeWidgetItemIterator(ui.treeWidget_language)
    while item.value():
        if item.value().checkState(0) == Qt.Checked and item.value().text(0) == language:
            print(item.value().text(0))
            return True
        item = item.__iadd__(1)
    return False

def getTranslationFromDb(en, ch, language, db):
    language2 = "#" + language
    str = covert.query(en, ch, language2, db)
    if str == "":
        str = covert.query(en, ch, language, db)
    if str == "" and language == "Portugese":
        str = covert.query(en, ch, "#Portuguese", db)
    if str == "" and language == "Portugese":
        str = covert.query(en, ch, "Portuguese", db)
    if str == "" and language == "Persian":
        str = covert.query(en, ch, "#Farsi", db)
    if str == "" and language == "Farsi":
        str = covert.query(en, ch, "Persian", db)
    return str

def getTranslationFromCustomer(en, language):
    global input_customr_xls
    if input_customr_xls == 0:
        return
    en_col = 0
    lang_col = 0
    new_str = ""
    for sheet in input_customr_xls.sheets():
        for col in range(0, sheet.ncols):
            lang = parseLanguage(sheet.cell_value(0, col))
            if lang == "English" or lang == "en" or lang == "#English":
                en_col = col
            #google_gl = googleTranslate.google_languages[language]

            if lang == language:
                lang_col = col
            #elif google_gl != "" and lang == googleTranslate.google_languages[language]:
            #    lang_col = col
        if lang_col == 0 or en_col == 0:
            break;
        for row in range(0, sheet.nrows):
            if sheet.cell_value(row, en_col) == en:
                new_str = sheet.cell_value(row, lang_col)
                break
    return new_str


def translate_googleEnglish(content, target_language):
    try:
        ret = googleTranslate.translate(content, target_language, "English")
    except Exception as e:
        ret = ""
        print(e)
    return ret

def translate_google(content, target_language, src_langauage):
    try:
        ret = googleTranslate.translate(content, target_language, src_langauage)
    except Exception as e:
        ret = ""
        print(e)
    return ret

def translate_youdao(content, target_language, src_langauage):
    try:
        ret = YouDaoTranslate.youDaoTranslate(content, target_language, src_langauage)
    except Exception as e:
        ret = ""
        print(e)
    return ret

def translate_baidu(content, target_language, src_langauage):
    try:
        ret = BaiduTranslate.translate(content, target_language, src_langauage)
    except Exception as e:
        ret = ""
        print(e)
    return ret


def getTranslationString(sheet, row, col, language):
    global engCol
    global chCol
    global gl_tran_dbs
    global MODE_CNPD
    global MODE_CUSTOMER
    global MODE_GOOGLE
    global tran_Mode

    if len(gl_tran_dbs) == 0:
        return sheet.cell_value(row, col)
    en = sheet.cell_value(row, engCol)
    zh = sheet.cell_value(row, chCol)


    if tran_Mode == MODE_CNPD:
        for db in gl_tran_dbs:
            str = getTranslationFromDb(en, zh, language, db)
            if str != "":
                break
    elif tran_Mode == MODE_CUSTOMER:
        str = getTranslationFromCustomer(en, language)
    elif tran_Mode == MODE_GOOGLE:
        str = translate_googleEnglish(en, language)

    return str

def translationOneStringTask(sheet, output_sheet, row, col, language):
    global mutex
    global tran_task_cout
    global progress
    global tran_success_cout
    global tran_failed_cout
    mutex.acquire()
    tran_task_cout = tran_task_cout + 1
    mutex.release()

    str = sheet.cell_value(row, col)
    tr = getTranslationString(sheet, row, col, language)

    if tr != "":
        str = tr
        style = green_style
        tran_success_cout = tran_success_cout + 1
    else:
        style = getCellStyle(sheet, row, col)
        tran_failed_cout = tran_failed_cout + 1
        if style == normal_style:
            style = yellow_style

    mutex.acquire()
    output_sheet.write(row, col, str, style)
    tran_task_cout = tran_task_cout - 1
    print(tran_task_cout)
    progress = progress + 1
    mutex.release()

def is_oneWordString(string):
    """判断是否包含空格"""
    if re.search("\s",string):
        return False
    else:
        return True

def translationOneStringGoogle(sheet, output_sheet, row, col, language):
    global mutex
    global tran_task_cout
    global progress

    #print("tranlating Google...")
    str = sheet.cell_value(row, col)
    style = getCellStyle(sheet, row, col)
    tr = ""
    if is_oneWordString(str) and style != green_style and str.isupper() == False:
        print(str)
        tr = translate_googleEnglish(str, language)

    if tr != "" and tr != str:
        str = tr
        style = blue_style
    else:
        style = getCellStyle(sheet, row, col)
        if style == normal_style:
            style = yellow_style

    output_sheet.write(row, col, str, style)


def createTranslationTask(tran_args):
    t1 = threading.Thread(target=translationOneStringTask, args=tran_args)
    t1.start()

def getbackgroundColor(sheet, row, col):
    global input_xls

    xf_idx = sheet.cell_xf_index(row, col)
    xf_list = input_xls.xf_list[xf_idx]
    color = input_xls.colour_map[xf_list.background.pattern_colour_index]
    #print(color)
    return color

def TranslationOneCol(sheet, output_sheet, col, language):
    global mutex
    global input_xls

    for row in range(0, sheet.nrows):
        str = sheet.cell_value(row, col)
        en = sheet.cell_value(row, engCol)
        #print("tranlating...")
        style = getCellStyle(sheet, row, col)
        if str != "" and str == en:
            if tran_Mode == MODE_GOOGLE:
                translationOneStringGoogle(sheet, output_sheet, row, col, language)
            else:
                createTranslationTask((sheet, output_sheet, row, col, language))
        #elif style == green_style or style == blue_style or style == red_style:
        #    tr = getTranslationString(sheet, row, col, language)
        #    if tr != "" and tr != en and tr != str:
        #        mutex.acquire()
        #        style = red_style
        #        output_sheet.write(row, col, tr, style)
        #        mutex.release()
        #    else:
        #        mutex.acquire()
        #        style = normal_style
        #        output_sheet.write(row, col, str, style)
        #        mutex.release()
        else:
            style = getCellStyle(sheet, row, col)
            mutex.acquire()
            output_sheet.write(row, col, str, style)
            mutex.release()

def wait_tran_task_finish():
    global mutex
    global tran_task_cout
    while True:
        mutex.acquire()
        if tran_task_cout == 0:
            break;
        mutex.release()

def open_xls(file):
    id_xls = 0
    try:
        id_xls = xlrd.open_workbook(file)
    except Exception as e:
        print(e)
    return id_xls

def getOuputFileName(name):
    output_file_name = name
    output_file = output_file_name + ".xls"
    temp_xls = open_xls(output_file)
    print(temp_xls)
    index = 0
    while temp_xls != 0:
        index = index + 1
        output_file = output_file_name + "_" + str(index) + ".xls"
        temp_xls = open_xls(output_file)
    return output_file

def getOutputSheet(name):
    global output_xls
    if output_xls == 0:
        return 0
    try:
        output_sheet = output_xls.sheet_index(name)
    except Exception as e:
        output_sheet = output_xls.add_sheet(name)

    return output_sheet

def TranslationExcel():
    global input_xls
    global output_xls
    global progress
    global TRAN_NONE
    global TRAN_GOING
    global TRAN_FINISHED
    global TRAN_FAILED
    global translating_flag
    global mutex
    global tran_success_cout
    global tran_failed_cout

    tran_success_cout = 0
    tran_failed_cout = 0

    if input_xls == 0 or output_xls == 0:
        translating_flag = TRAN_FAILED
        return
    translating_flag = TRAN_GOING
    progress = 0
    print("start translation")
    for sheet in input_xls.sheets():
        output_sheet = getOutputSheet(sheet.name)
        for col in range(0, sheet.ncols):
            language = parseLanguage(sheet.cell_value(0, col))
            if col != 0 and col != engCol and isCheckLang(language):
                TranslationOneCol(sheet, output_sheet, col, language)
            else:
                for row in range(0, sheet.nrows):
                    tr = sheet.cell_value(row, col)
                    style = getCellStyle(sheet, row, col)
                    mutex.acquire()
                    output_sheet.write(row, col, tr, style)
                    mutex.release()

    wait_tran_task_finish()
    click_outputFile()
    translating_flag = TRAN_FINISHED
    print("save "+output_file)

def getLanguages():
    global languagesList
    global input_xls
    global engCol
    global chCol
    ui.treeWidget_language.clear()
    languagesList.clear()
    for sheet in input_xls.sheets():
        for col in range(1, sheet.ncols):
            lang = str(parseLanguage(sheet.cell_value(0, col)))
            item = QTreeWidgetItem(ui.treeWidget_language)
            item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            item.setCheckState(0, Qt.Unchecked)
            item.setText(0, str(lang))
            if str(lang) == "English":
                engCol = col
            if str(lang) == "Simplified_Chinese":
                chCol = col
            languagesList.append(str(lang))

    return languagesList

def createTask():
    t1 = threading.Thread(target=TranslationExcel, args=())
    t1.start()

def set_Tran_db():
    global gl_tran_dbs
    gl_tran_dbs.clear()
    if ui.checkBox_shield_0.isChecked():
        gl_tran_dbs.append(DB_CVTE)
    if ui.checkBox_shield_1.isChecked():
        gl_tran_dbs.append(DB_NEWOLDTRAN)
    if ui.checkBox_shield_2.isChecked():
        gl_tran_dbs.append(DB_CNPD)
    if ui.checkBox_shield_3.isChecked():
        gl_tran_dbs.append(DB_FAEPV)
    if ui.checkBox_shield_4.isChecked():
        gl_tran_dbs.append(DB_HISENSE)
    if ui.checkBox_shield_5.isChecked():
        gl_tran_dbs.append(DB_TCL)
    if ui.checkBox_shield_6.isChecked():
        gl_tran_dbs.append(DB_CAIXUN)

def translationWithNetwork(en, ch, language):
    result = ""
    # google
    google_tr = translate_googleEnglish(en, language)
    result = result + "google翻译：\n"
    result = result + language + ": " + google_tr + " ( from English)\n"
    if ch != "":
        google_ch_tr = translate_google(ch, language, "Chinese")
        result = result + language + ": " + google_ch_tr + " (from Chinese)\n\n"

    # baidu
    result = result + "百度翻译：\n"
    baidu_tr = translate_baidu(en, language, "English")
    result = result + language + ": " + baidu_tr + " (from English)\n"
    if ch != "":
        baidu_ch_tr = translate_baidu(ch, language, "Chinese")
        result = result + language + ": " + baidu_ch_tr + "( from Chinese)\n\n"

    # youdao
    result = result + "有道翻译：\n"
    youdao_tr = translate_youdao(en, language, "English")
    result = result + language + ": " + youdao_tr + " (from English)\n"

    if ch != "":
        youdao_ch_tr = translate_youdao(ch, language, "Chinese")
        result = result + language + ": " + youdao_ch_tr + " (from Chinese)\n\n"

    result = result + "翻译逆检查：\n"
    result = result + "google->baidu：\n"
    #google -> baidu
    r_tr = translate_baidu(google_tr, "English", language)
    result = result + google_tr + ": " + r_tr + " (from google)\n"
    r_tr = translate_baidu(google_ch_tr, "Chinese", language)
    result = result + google_ch_tr + ": " + r_tr + " (from google Chinese)\n\n"
    # google -> youdao
    result = result + "google->youdao：\n"
    r_tr = translate_youdao(google_tr, "English", language)
    result = result + google_tr + ": " + r_tr + " (from google)\n"
    r_tr = translate_youdao(google_ch_tr, "Chinese", language)
    result = result + google_ch_tr + ": " + r_tr + " (from google Chinese)\n\n"
    return result

def translationString(en, ch, language):
    global gl_tran_dbs
    result = ""

    if ui.radioButton_shield.isChecked() == 1:
        for db in gl_tran_dbs:
            tr = getTranslationFromDb(en, ch, language, db)
            if tr != "":
                result = result + language +":"+tr +"\n"
    elif ui.radioButton_customer.isChecked() == 1:
        tr = getTranslationFromCustomer(en, language)
        result = result + language + ":" + tr + "\n"
    elif ui.radioButton_google.isChecked() == 1:
        tr = translate_googleEnglish(en, language)
        ch_tr = translate_google(ch, language, "Chinese")
        result = result + language + ": " + tr + " (English)\n"
        result = result + language + ": " + ch_tr + " (Chinese)\n"
    elif ui.radioButton_google_youdao.isChecked() == 1:
        result = result + translationWithNetwork(en, ch, language)



    return result

def translation_word():
    global gl_tran_dbs
    global languagesList
    set_Tran_db()
    en = ui.lineEdit_word.text()
    if en == "":
        ui.textEdit_ouput.setText("请输入需要翻译的英文")
    ch = ui.lineEdit_word_ch.text()
    langauge = ui.lineEdit_language.text()
    output = "en:" + en + "\n"
    output = output + "ch:" + ch + "\n\n"

    if len(languagesList) > 0:
        for lang in languagesList:
            if isCheckLang(lang):
                ret = translationString(en, ch, lang)
                output = output + ret + "\n"
    else:
        ret = translationString(en, ch, langauge)
        output = output + ret

    ui.textEdit_ouput.setText(output)

def create_updateUI():
    # 创建线程
    backend = BackendThread()
    backend.start()
    # 连接信号
    # backend.update.connect(click_check_status)
    #thread = QThread()
    #backend.moveToThread(thread)
    # 开始线程
    #thread.connectNotify(backend.run)
    #thread.started.connect(backend.run)
    #thread.start()

def translatonXlsAllString():
    global tips_string
    set_Tran_db()
    # create_updateUI()
    createTask()
    tips_string = tips_string + "> 开始翻译，了解进度请点击刷新进度\n"
    ui.textEdit_ouput.setText(tips_string)

def click_outputFile():
    global output_xls
    global output_file
    if output_xls == 0:
        return

    output_file = getOuputFileName("output")
    output_xls.save(output_file)



def click_Translation():
    global input_customr_xls
    global tips_string
    global MODE_CNPD
    global MODE_CUSTOMER
    global MODE_GOOGLE
    global tran_Mode

    if input_customr_xls == 0 and ui.radioButton_customer.isChecked() == 1:
        tips_string = tips_string + "> 请导入客户翻译\n"
        ui.textEdit_ouput.setText(tips_string)
        return

    if ui.radioButton_shield.isChecked() == 1:
        tran_Mode = MODE_CNPD
    elif ui.radioButton_customer.isChecked() == 1:
        tran_Mode = MODE_CUSTOMER
    elif ui.radioButton_google.isChecked() == 1:
        tran_Mode = MODE_GOOGLE

    if ui.radioButton_word.isChecked() == 1:
        translation_word()
    elif ui.radioButton_all.isChecked() == 1:
        ui.ptn_translation.setEnabled(False)
        translatonXlsAllString()

def click_openCustomerFile():
    global input_customr_xls
    global tips_string
    file = QFileDialog.getOpenFileName(MainWindow,'选择文件','','Excel files(*.xlsx , *.xls)')
    file_name = file[0]
    input_customr_xls = xlrd.open_workbook(str(file_name))
    tips_string = tips_string + "> 打开" + file_name + "\n"
    ui.textEdit_ouput.setText(tips_string)

def click_openFile():
    global path_langfile_name
    global input_xls
    global output_xls
    global tips_string
    lang_file = QFileDialog.getOpenFileName(MainWindow,'选择文件','','Excel files(*.xlsx , *.xls)')
    path_langfile_name = lang_file[0]
    print(path_langfile_name)
    input_xls = xlrd.open_workbook(str(path_langfile_name),formatting_info=True)
    getLanguages()
    tips_string = tips_string + "> 打开" + path_langfile_name + "\n"
    ui.textEdit_ouput.setText(tips_string)
    output_xls = xlwt.Workbook(encoding="utf-8")

def click_check_status():
    global TRAN_NONE
    global TRAN_GOING
    global TRAN_FINISHED
    global TRAN_FAILED
    global translating_flag
    global tips_string
    global progress
    global output_file
    global tran_success_cout
    global tran_failed_cout
    status_tips = ""
    if translating_flag == TRAN_NONE:
        return
    elif translating_flag == TRAN_GOING:
        status_tips = tips_string + "> 正在翻译中,请耐心等待\n"
        status_tips = tips_string + "> 正在翻译有" + str(tran_task_cout)+"个字符串, 已翻译" + str(progress) + "个\n"
    elif translating_flag == TRAN_FINISHED:
        status_tips = tips_string + "> 翻译完成，请查看" + output_file + "\n"
        translating_flag = TRAN_NONE
        ui.ptn_translation.setEnabled(True)
    elif translating_flag == TRAN_FAILED:
        status_tips = tips_string + "> 翻译失败，请重试\n"
        translating_flag = TRAN_NONE
        ui.ptn_translation.setEnabled(True)

    status_tips = status_tips + "> 其中翻译成功 "+str(tran_success_cout)+"个， 失败 "+str(tran_failed_cout)+"个\n"
    ui.textEdit_ouput.setText(status_tips)





def export_xls_oneCol(sheet, col, export_sheet):
    global engCol
    global export_count

    export_row = 1
    for row in range(1, sheet.nrows):
        if checkIsNeedTraslation(sheet, row, col):
            tr = sheet.cell_value(row, 0)
            export_sheet.write(export_row, 0, tr)
            tr = "RDA:6710:application"
            export_sheet.write(export_row, 1, tr)
            en = sheet.cell_value(row, engCol)
            style = getCellStyle(sheet, row, col)
            if style == green_style:
                export_sheet.write(export_row, 2, en, style)
            else:
                export_sheet.write(export_row, 2, en)
            tr = sheet.cell_value(row, chCol)
            export_sheet.write(export_row, 3, tr)
            export_row = export_row + 1
            export_count = export_count + 1

def click_export():
    global input_xls
    global engCol
    global chCol
    global tips_string
    global export_count
    export_xls = xlwt.Workbook(encoding="utf-8")
    if input_xls == 0:
        return
    isset = 0
    export_count = 0
    print("start export")
    for sheet in input_xls.sheets():
        for col in range(0, sheet.ncols):
            language = str(parseLanguage(sheet.cell_value(0, col)))
            if col != 0 and col != engCol and isCheckLang(language):
                export_sheet = export_xls.add_sheet(language)
                isset = 1
                export_sheet.write(0, 0, "id")
                export_sheet.write(0, 1, "project")
                export_sheet.write(0, 2, "values-en")
                export_sheet.write(0, 3, "values-zh")

                tr = "values-" + str(language)
                export_sheet.write(0, 4, tr)

                export_xls_oneCol(sheet, col, export_sheet)


    if isset == 1:
        export_file = getOuputFileName("export")
        export_xls.save(export_file)
        print("export finish")
        tips_string = tips_string + "> 导出"+export_file+"\n"
        tips_string = tips_string + "> 共导出" + str(export_count) + "个需要翻译的词条\n"
        ui.textEdit_ouput.setText(tips_string)



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = main_window.Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    # set title and icon
    MainWindow.setWindowTitle("QCTranslation V1.0")
    MainWindow.setWindowIcon(QIcon(':/icon.png'))
    ui.ptn_open.clicked.connect(click_openFile)
    ui.ptn_translation.clicked.connect(click_Translation)
    ui.ptn_open_customer.clicked.connect(click_openCustomerFile)
    ui.ptn_check.clicked.connect(click_check_status)
    ui.ptn_export.clicked.connect(click_export)
    sys.exit(app.exec_())


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
