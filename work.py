import asyncio,re,requests,sqlite3
from concurrent.futures import ThreadPoolExecutor
from PySide6.QtCore import QThread
class WorkThread(QThread):
    def __init__(self,le_text):
        self.le_text = le_text
        self.base_data = []
        super().__init__()
        self.pool = ThreadPoolExecutor(10)
        self.base_url = f'https://fm.liuzhijin.cn/api.php?types=search&count=100&source=netease&pages=1&name={self.le_text}'

    def req(self,data):
        music_name = data['name']
        music_artist = data['artist'][0]
        music_album = data['album']
        mp3_url = f'https://fm.liuzhijin.cn/api.php?types=url&id={data["id"]}'
        response = requests.get(mp3_url)
        music = response.json()['url']
        data_dict = {'music_name':music_name,'music_artist':music_artist,'music_album':music_album,'music_url':music}
        return data_dict

    def base_req(self):
        req = requests.post(self.base_url)
        res = req.json()
        return res

    def run(self):
        for json_text in self.base_req():
            future = self.pool.submit(self.req, json_text)
            future.add_done_callback(self.done)
        self.pool.shutdown(True)
        conn = sqlite3.connect('musicData.db')
        # 创建一个Cursor对象并通过它执行SQL命令
        cursor = conn.cursor()
        # 清除旧表
        cursor.execute(
            '''
            DELETE FROM users
            '''
        )
        # 创建一个新表
        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                music_name TEXT NOT NULL,
                music_artist TEXT NOT NULL,
                music_album TEXT NOT NULL,
                music_url TEXT NOT NULL
            )
            '''
        )
        for dict_data in self.base_data:
            cursor.execute('''
            INSERT INTO users (music_name, music_artist, music_album,music_url) VALUES (?, ?, ?,?)
            ''', (dict_data['music_name'], dict_data['music_artist'], dict_data['music_album'],dict_data['music_url']))
        # 提交事务
        conn.commit()

        # 关闭Cursor
        cursor.close()

        # 关闭连接
        conn.close()

    def done(self,response):
        content = response.result()
        self.base_data.append(content)


