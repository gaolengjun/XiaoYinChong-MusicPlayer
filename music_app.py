import sys,work,play,sqlite3,querydb,datetime,re
from PySide6.QtMultimedia import QMediaPlayer,QAudioOutput
from PySide6.QtWidgets import QApplication,QWidget,QLabel,QSlider
from PySide6.QtGui import QIcon,QPixmap
from PySide6.QtCore import QUrl,QTimer
from ui import Ui_Form

class MyWindow(QWidget,Ui_Form):
    def __init__(self):
        super().__init__()
        self.player = QMediaPlayer()
        self.out_put = QAudioOutput(self)
        self.player.setAudioOutput(self.out_put)
        self.slider_value = 0
        self.count = 1
        self.songName = None
        self.songUrl = None
        self.index = 0
        self.nextIndex = 1
        self.previousIndex = 1
        self.songDuration = 0
        self.currentPosition = 0
        self.min = 0
        self.sec = 0
        self.setupUi(self)
        self.show()
        self.volume_slider.setValue(50)
        self.search_btn.clicked.connect(self.on_search_btn)
        self.le.textChanged.connect(self.on_text_changed)
        self.volume_slider.valueChanged.connect(self.on_volume_changed)
        # 播放按钮初始状态
        self.play_btn.setIcon(QIcon(QPixmap(':/pause.png')))
        self.play_btn.clicked.connect(self.on_play_btn)
        self.play_btn.setCheckable(True)
        self.item_list.itemDoubleClicked.connect(self.query_db)
        self.timer = QTimer()
        self.timer.timeout.connect(self.on_timeout)
        self.next_btn.clicked.connect(self.next_player)
        self.Previous_btn.clicked.connect(self.previous_player)


    def on_text_changed(self,data):
        self.lb.setText(f'当前搜索：{data}')

    def on_volume_changed(self,data):
        self.volume_lb.setText(f'音量：{data}%')

    def on_play_btn(self,Checka):
        if Checka == True:
            self.play_btn.setIcon(QIcon(QPixmap(':/pause.png')))
            if self.player.playbackState() == QMediaPlayer.PlayingState:
                self.player.pause()
                self.timer.stop()
                self.currentPosition = self.player.position()
                self.movie.stop()
        else:
            self.play_btn.setIcon(QIcon(QPixmap(':/play.png')))
            self.player.play()
            self.movie.start()
            self.timer.start()

    def on_search_btn(self):
        self.search_btn.setEnabled(False)
        self.work = work.WorkThread(self.le.text())
        self.work.start()
        self.work.finished.connect(self.init_query_db)

    def init_query_db(self):
        self.queryDB = querydb.QueryDB()
        self.queryDB.start()
        self.queryDB.emit_db.connect(self.uptate_ui)

    def query_db(self,v):
        self.queryDB = querydb.QueryDB()
        self.queryDB.start()
        self.queryDB.emit_db.connect(self.change_music)
        string = v.text()
        match = re.search(r'歌曲：(.*?) 歌手',string)
        self.songName = match.group(1)



    #更新界面
    def uptate_ui(self,data):
        # 每次获取新的数据先清除旧列表数据
        self.item_list.clear()
        for item in data:
            self.item_list.addItem(f'歌曲：{item[1]} 歌手：{item[2]} 专辑：{item[3]}')
        self.search_btn.setEnabled(True)

    def on_mediaStatus(self,status):
        self.progress_bar.setValue(0)

        if status == QMediaPlayer.MediaStatus.BufferedMedia:
            self.songDuration = round(self.player.duration() / 1000)
            self.progress_bar.setMaximum(self.songDuration)
            # 开启定时器
            self.timer.start(1000)
        else:
            self.min = 0
            self.sec = 0
            self.count = 0
            self.progress_bar.setValue(0)

    def on_timeout(self):
        if self.player.isPlaying():
           if self.count != self.songDuration:
               self.progress_bar.setValue(self.count)
               if self.sec < 10:
                  self.duration_lb.setText(f"0{self.min}:0{self.sec}")
               if self.sec >= 10:
                  self.duration_lb.setText(f"0{self.min}:{self.sec}")
               if self.sec == 60:
                  self.sec = 00
                  self.min += 1
                  self.duration_lb.setText(f"0{self.min}:0{self.sec}")
               # else:
               #    self.duration_lb.setText(f"00:{self.sec}")
           else:
               self.timer.stop()
               self.count = 0
               self.progress_bar.setValue(0)
        else:
            self.duration_lb.setText('00:00')
            self.movie.stop()
        self.count += 1
        self.sec += 1

    def change_music(self,data):
        self.songUrl = data
        self.index = self.item_list.currentRow()
        self.music_lb.setText(self.songName)
        self.play_btn.setIcon(QIcon(QPixmap(':/play.png')))
        self.flag = True
        self.player.deleteLater()
        self.player = QMediaPlayer()
        self.out_put = QAudioOutput(self)
        self.player.setAudioOutput(self.out_put)
        self.player.setSource(data[self.index][4])
        self.player.play()
        self.movie.start()
        self.player.mediaStatusChanged.connect(self.on_mediaStatus)

    def on_volume_changed(self,value):
        self.volume_lb.setText(f'音量：{str(value)}%')
        self.slider_value = value
        self.out_put.setVolume(value*0.01)

    def next_player(self):
        self.player.deleteLater()
        self.player = QMediaPlayer()
        self.out_put = QAudioOutput(self)
        self.player.setAudioOutput(self.out_put)
        try:
            self.music_lb.setText(self.songUrl[self.index + self.nextIndex][1])
            self.player.setSource(self.songUrl[self.index + self.nextIndex][4])
        except IndexError:
            self.music_lb.setText(self.songUrl[self.index][1])
            self.player.setSource(self.songUrl[self.index][4])
        self.player.play()

        self.movie.start()
        self.nextIndex += 1

    def previous_player(self):
        self.player.deleteLater()
        self.player = QMediaPlayer()
        self.out_put = QAudioOutput(self)
        self.player.setAudioOutput(self.out_put)
        try:
            self.music_lb.setText(self.songUrl[self.index + self.previousIndex][1])
            self.player.setSource(self.songUrl[self.index + self.previousIndex][4])
        except IndexError:
            self.music_lb.setText(self.songUrl[self.index][1])
            self.player.setSource(self.songUrl[self.index][4])
        self.player.play()

        self.movie.start()
        self.previousIndex -= 1

if __name__=="__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    with open('styles.qss','r') as file:
        app.setStyleSheet(file.read())
    app.exec()