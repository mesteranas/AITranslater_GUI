import sys
from custome_errors import *
sys.excepthook = my_excepthook
from llamaapi import LlamaAPI
import requests
import update
import gui
import guiTools
from settings import *
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
import PyQt6.QtCore as qt2
language.init_translation()
import google.generativeai as genai
genai.configure(api_key="")
llama = LlamaAPI("")
TextModel=genai.GenerativeModel('gemini-pro')
class AITranslaterObjects(qt2.QObject):
    Finnish=qt2.pyqtSignal(str)
class AITranslaterMainThread(qt2.QRunnable):
    def __init__(self,text:str,translateTo:str,option:int,model:int):
        super().__init__()
        self.text=text
        self.model=model
        self.translateTo=translateTo
        self.option=option
        self.object=AITranslaterObjects()
        self.finish=self.object.Finnish
    def run(self):
        prompt=""
        if self.option==0:
            prompt=f"""translate: 
            {self.text}
            to {self.translateTo}
            give me the translated text only don't type any things except the text"""
        elif self.option==1:
            prompt = f"""
Summarize the following text and translate the summary into {self.translateTo}:
Text:
{self.text}

Please provide only the summarized text in the specified language. Ensure the summary is concise and captures the main points accurately.
and don't type any thing in the message except the text
"""

        result=""
        if self.model==0:
            prompt.replace(" ","%22")
            try:
                r=requests.get("https://chatgpt.apinepdev.workers.dev/?question=" + prompt)
                result=r.json()["answer"]
            except Exception as error:
                print(error)
                result="error"
        elif self.model==1:
            try:
                response = TextModel.generate_content(prompt)
                result=response.text
            except:
                result=_("error")
        elif self.model==2:
            api_request_json = {
  "model": "llama3.1-405b",
"max_tokens":3000,
  "messages": [
    {"role": "user", "content": prompt},
  ]
  }
            try:
                response = llama.run(api_request_json)
                result=response.json()["choices"][0]["message"]["content"]
            except:
                result=_("error")

        self.finish.emit(result)
class main (qt.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(app.name + _("version : ") + str(app.version))
        layout=qt.QVBoxLayout()
        self.text=qt.QLineEdit()
        layout.addWidget(qt.QLabel(_("text to translate")))
        layout.addWidget(self.text)
        self.model=qt.QComboBox()
        self.model.addItems(["chatgpt","gemini","lama"])
        layout.addWidget(qt.QLabel(_("select the model")))
        layout.addWidget(self.model)
        self.translateTo=qt.QComboBox()
        languages = [
    "English United States",
    "English United Kingdom",
    "English Australia",
    "English Canada",
    "English India",
    "Spanish Spain",
    "Spanish Mexico",
    "Spanish Argentina",
    "Spanish Colombia",
    "Spanish United States",
    "French France",
    "French Canada",
    "French Belgium",
    "French Switzerland",
    "Portuguese Portugal",
    "Portuguese Brazil",
    "German Germany",
    "German Austria",
    "German Switzerland",
    "Arabic Standard",
    "Arabic Egypt",
    "Arabic Saudi Arabia",
    "Arabic Levantine",
    "Chinese Mandarin (Simplified)",
    "Chinese Mandarin (Traditional)",
    "Chinese Cantonese",
    "Dutch Netherlands",
    "Dutch Belgium",
    "Russian Russia",
    "Italian Italy",
    "Italian Switzerland",
    "Japanese Japan",
    "Korean South Korea",
    "Hindi India",
    "Swedish Sweden",
    "Norwegian Norway",
    "Danish Denmark",
    "Finnish Finland",
    "Greek Greece",
    "Turkish Turkey",
    "Polish Poland",
    "Hebrew Israel",
    "Indonesian Indonesia",
    "Malay Malaysia",
    "Malay Brunei",
    "Thai Thailand",
    "Vietnamese Vietnam",
    "Bengali Bangladesh",
    "Bengali India",
    "Punjabi India",
    "Punjabi Pakistan",
    "Tamil India",
    "Tamil Sri Lanka",
    "Telugu India",
    "Marathi India",
    "Urdu Pakistan",
    "Urdu India"
]
        languages.sort()
        self.translateTo.addItems(languages)
        layout.addWidget(qt.QLabel(_("Translate to :")))
        layout.addWidget(self.translateTo)
        self.translate=guiTools.QPushButton(_("translate"))
        self.translate.clicked.connect(self.runMainThread)
        layout.addWidget(self.translate)
        self.Summarize =guiTools.QPushButton(_("Summarize and translate"))
        self.Summarize .clicked.connect(lambda:self.runMainThread(option=1))
        layout.addWidget(self.Summarize)

        self.result=guiTools.QReadOnlyTextEdit()
        layout.addWidget(self.result)
        self.setting=guiTools.QPushButton(_("settings"))
        self.setting.clicked.connect(lambda: settings(self).exec())
        layout.addWidget(self.setting)
        w=qt.QWidget()
        w.setLayout(layout)
        self.setCentralWidget(w)

        mb=self.menuBar()
        help=mb.addMenu(_("help"))
        helpFile=qt1.QAction(_("help file"),self)
        help.addAction(helpFile)
        helpFile.triggered.connect(lambda:guiTools.HelpFile())
        helpFile.setShortcut("f1")
        cus=help.addMenu(_("contact us"))
        telegram=qt1.QAction("telegram",self)
        cus.addAction(telegram)
        telegram.triggered.connect(lambda:guiTools.OpenLink(self,"https://t.me/mesteranasm"))
        telegramc=qt1.QAction(_("telegram channel"),self)
        cus.addAction(telegramc)
        telegramc.triggered.connect(lambda:guiTools.OpenLink(self,"https://t.me/tprogrammers"))
        githup=qt1.QAction(_("Github"),self)
        cus.addAction(githup)
        githup.triggered.connect(lambda: guiTools.OpenLink(self,"https://Github.com/mesteranas"))
        X=qt1.QAction(_("x"),self)
        cus.addAction(X)
        X.triggered.connect(lambda:guiTools.OpenLink(self,"https://x.com/mesteranasm"))
        email=qt1.QAction(_("email"),self)
        cus.addAction(email)
        email.triggered.connect(lambda: guiTools.sendEmail("anasformohammed@gmail.com","project_type=GUI app={} version={}".format(app.name,app.version),""))
        Github_project=qt1.QAction(_("visite project on Github"),self)
        help.addAction(Github_project)
        Github_project.triggered.connect(lambda:guiTools.OpenLink(self,"https://Github.com/mesteranas/{}".format(settings_handler.appName)))
        Checkupdate=qt1.QAction(_("check for update"),self)
        help.addAction(Checkupdate)
        Checkupdate.triggered.connect(lambda:update.check(self))
        licence=qt1.QAction(_("license"),self)
        help.addAction(licence)
        licence.triggered.connect(lambda: Licence(self))
        donate=qt1.QAction(_("donate"),self)
        help.addAction(donate)
        donate.triggered.connect(lambda:guiTools.OpenLink(self,"https://www.paypal.me/AMohammed231"))
        about=qt1.QAction(_("about"),self)
        help.addAction(about)
        about.triggered.connect(lambda:qt.QMessageBox.information(self,_("about"),_("{} version: {} description: {} developer: {}").format(app.name,str(app.version),app.description,app.creater)))
        self.setMenuBar(mb)
        if settings_handler.get("update","autoCheck")=="True":
            update.check(self,message=False)
    def closeEvent(self, event):
        if settings_handler.get("g","exitDialog")=="True":
            m=guiTools.ExitApp(self)
            m.exec()
            if m:
                event.ignore()
        else:
            self.close()
    def runMainThread(self,option:int=0):
        thread=AITranslaterMainThread(self.text.text(),self.translateTo.currentText(),option,self.model.currentIndex())
        self.result.setText(_("loading ... please wait."))
        thread.finish.connect(self.onMainThreadFinished)
        qt2.QThreadPool(self).start(thread)
    def onMainThreadFinished(self,result:str):
        self.result.setText(result)
        self.result.setFocus()
App=qt.QApplication([])
w=main()
w.show()
App.setStyle('fusion')
App.exec()