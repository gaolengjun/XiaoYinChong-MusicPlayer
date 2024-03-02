import sqlite3
from PySide6.QtCore import QThread, Signal

class QueryDB(QThread):
    emit_db = Signal(list)

    def __init__(self):
        super().__init__()
        self.conn = sqlite3.connect('musicData.db', check_same_thread=False)
        self.cursor = self.conn.cursor()

    def run(self):
        # 执行查询
        self.cursor.execute('SELECT * FROM users')
        # 读取结果
        rows = self.cursor.fetchall()
        self.emit_db.emit(rows)
        # 关闭游标和连接
        self.cursor.close()
        self.conn.close()
