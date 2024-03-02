
from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QWidget, QApplication, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, \
    QListWidget, QProgressBar, QSlider,QSpacerItem,QSizePolicy
import rc_icons
from PySide6.QtGui import QIcon, QPixmap,QMovie

class Ui_Form():
    def setupUi(self, Form):
        Form.setWindowTitle('小音虫 v1.0')
        Form.setWindowIcon(QIcon(':/48.png'))
        # Form.resize(700,500)
        self.setFixedSize(700, 500)
        # 创建一个垂直布局
        vl = QVBoxLayout(self)
        # 创建一个横向布局
        hl = QHBoxLayout()

        self.search_btn = QPushButton()
        self.search_btn.setIconSize(QSize(30, 30))
        self.search_btn.setIcon(QIcon(QPixmap(':/search.png')))
        hl.addWidget(self.search_btn)

        self.le = QLineEdit()
        hl.addWidget(self.le)

        self.lb = QLabel('请搜索歌曲')
        # 将标签添加到垂直布局追踪
        hl.addWidget(self.lb)

        spacer = QSpacerItem(100, 20)  # 创建一个水平方向的弹簧
        hl.addSpacerItem(spacer)

        # 将水平布局添加到垂直布局中
        vl.addLayout(hl)
        # 实例化一个列表控件
        self.item_list = QListWidget()
        #将列表添加到垂直布局中
        vl.addWidget(self.item_list)
        # 创建一个底部水平布局
        bottom_hl = QHBoxLayout()
        # 创建一个图片标签
        self.icon_lb = QLabel()
        self.movie = QMovie(':/wave.gif')
        self.icon_lb.setMovie(self.movie)

        self.icon_lb.resize(200,200)
        self.icon_lb.setScaledContents(True)
        bottom_hl.addWidget(self.icon_lb)

        # 创建一个底部垂直布局
        bottom_vl = QVBoxLayout()
        self.music_lb = QLabel('暂无歌曲')
        bottom_vl.addWidget(self.music_lb)

        # 创建一个进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(False)
        # 将进度条添加到底部垂直布局中
        bottom_vl.addWidget(self.progress_bar)

        # 再将底部垂直布局加入到底部水平布局
        bottom_hl.addLayout(bottom_vl)
        # 创建一个显示音乐时间的标签
        self.duration_lb = QLabel('00:00')
        bottom_hl.addWidget(self.duration_lb)

        spacer = QSpacerItem(50, 20)  # 创建一个水平方向的弹簧
        bottom_hl.addSpacerItem(spacer)

        # 创建一个播放上一曲的图标按钮
        self.Previous_btn = QPushButton()
        self.Previous_btn.setIconSize(QSize(30, 30))
        self.Previous_btn.setIcon(QIcon(QPixmap(':/l.png')))
        bottom_hl.addWidget(self.Previous_btn)
        # 创建一个播放按钮
        self.play_btn = QPushButton()
        self.play_btn.setIconSize(QSize(30, 30))
        self.play_btn.setIcon(QIcon(QPixmap(':/play.png')))
        bottom_hl.addWidget(self.play_btn)
        # 创建一个播放下一曲的图标按钮
        self.next_btn = QPushButton()
        self.next_btn.setIconSize(QSize(30, 30))
        self.next_btn.setIcon(QIcon(QPixmap(':/r.png')))
        bottom_hl.addWidget(self.next_btn)

        # 创建一个音量图标
        self.volume_lb = QLabel('音量：50%')
        bottom_hl.addWidget(self.volume_lb)

        # 创建一个水平滑块
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(100)
        bottom_hl.addWidget(self.volume_slider)


        # 将底部水平布局添加到整体垂直布局
        vl.addLayout(bottom_hl)