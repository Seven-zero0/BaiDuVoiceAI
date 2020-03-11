"""
文字转语言
1. 建立连接
2. 打开文件
3. 转换成音频文件
4. 保存文件
"""

from aip import AipSpeech

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QMessageBox
from PyQt5.QtGui import QIcon
from MusicUi import Ui_Form


class VoiceType(object):
    def __init__(self):
        self.APP_ID = "输入ID"
        self.API_KEY = "输入key"
        self.SECRET_KET = "输入secret_Ket"
        self.client = self.voice_content()

    def voice_content(self):
        """ 1. 建立连接 """
        return AipSpeech(self.APP_ID, self.API_KEY, self.SECRET_KET)

    def read_file(self, name):
        """ 2. 读取文件 """
        try:
            with open(name, 'r', encoding='gbk') as f:
                file = f.read()
            return file
        except Exception as e:
            with open(name, 'r', encoding='utf-8') as f:
                file = f.read()
            return file

    def switch_voice(self, file, vol=5, spd=5, pit=5, per=0):
        """ 3. 合成音频 """
        result = self.client.synthesis(file, 'zh', 1, {
            'vol': vol, 'spd': spd, 'pit': pit, 'per': per})
        """
        发音人选择, 
        0为女声，
        1为男声，
        3为情感合成-度逍遥，
        4为情感合成-度丫丫，
        默认为普通女
        """
        return result

    def save_mp3(self, result, name):
        """ 4. 保存文件 """
        if not isinstance(result, dict):
            # name = name[:-4]
            with open('{}.mp3'.format(name), 'wb') as f:
                f.write(result)

            return 1

    def run(self, name):
        """ 主要逻辑 """
        # 2. 读取需要转语音文件
        file = self.read_file(name)
        return file


class VoiceUi(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.dia_log = QFileDialog()
        self.vte = VoiceType()
        self.show_UI()

    def show_UI(self):
        """ 附加UI """
        self.setWindowTitle("百度文字转语音")
        self.setWindowIcon(QIcon("images/voice.png"))
        self.resize(382, 210)   # 设置尺寸表
        self.setFixedSize(382, 210)     # 设置固定尺寸

    def show_dialog(self):
        """ 完成的时候弹出 """
        QMessageBox.information(self, "提示：", "合成完成", QMessageBox.Ok)    # 合成完成弹出

    def info_dialog(self):
        """ 未选择保存路径弹出 """
        QMessageBox.information(self, '提示', '当前未选择保存路径', QMessageBox.Ok)

    def open_files(self):
        """ 打开txt文件 """
        global file
        #方法1
        # self.dia_log.setFileMode(QFileDialog.AnyFile)
        # self.dia_log.setFilter(QDir.Files)
        # if self.dia_log.exec():
        #     filenames = self.dia_log.selectedFiles()
        # 方法2
        # if self.dia_log.exec():
        try:
            filenames = self.dia_log.getOpenFileName(self, 'open file', '../', 'txt(*.txt , *.text)')
            name = filenames[0]
            file = self.vte.run(name)
        except FileNotFoundError as e:
            pass

    def save_file(self):
        """ 选择保存文件及路径 """
        global fileName
        try:
            fileName, ok2 = QFileDialog.getSaveFileName(self, 'save', "../", "mp3(*mp3)")
        except Exception as e:
            pass

    def start_compound(self):
        """ 开始合成 """
        try:
            # 获取音频设置
            per = self.voice_people()
            pit = self.tone_num()
            spd = self.speed_num()
            vol = self.volume_num()
            result = self.vte.switch_voice(file=file, vol=vol, spd=spd, pit=pit, per=per)
            num = self.vte.save_mp3(result, name=fileName)
            if num == 1:
                self.show_dialog()
        except NameError as e:
            self.info_dialog()

    def voice_people(self):
        """ 人声选择 """
        voicepeople = self.ui.comboBox_select.currentText()
        per_num = voicepeople[0]
        return per_num

    def tone_num(self):
        """ 音调选择：pit """
        pit_num = int(self.ui.Box_tone.value())
        return pit_num

    def speed_num(self):
        """ 语速选择：spd """
        spd_num = int(self.ui.Box_speed.value())
        return spd_num

    def volume_num(self):
        """ 音量选择:vol """
        vol_num = int(self.ui.Box_volume.value())
        return vol_num


if __name__ == '__main__':
    app = QApplication(sys.argv)
    vt = VoiceUi()
    vt.show()
    sys.exit(app.exec_())
