import os, sys, time, requests
from tkinter import *
from tkinter import filedialog
from threading import Thread
from TikTok import TikTok
from DouYin import DouYin
from GUI import GUI


class APP(GUI):
    def __init__(self):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36 Edg/87.0.664.66'
        }

        self.tiktok = TikTok()
        self.douyin = DouYin()

        self.window = self.windowInit()
    
        # =============== FRAME LAYOUT ==================
        self.folderFrameName = 'folderFrame'
        self.urlFrameName = 'urlFrame'
        self.countMsgFrameName = 'countMsgFrame'
        self.fileMsgFrameName = 'fileMsgFrame'
        self.progressFrameName = 'progressFrame'
        self.frameLayouts = {
            self.folderFrameName: (1, 1),
            self.urlFrameName: (2, 1),
            self.countMsgFrameName: (3, 1),
            self.fileMsgFrameName: (4, 1),
            self.progressFrameName: (5, 1),
        }

        self.folderFrame = self.createFrame(self.window, self.frameLayouts, self.folderFrameName)
        self.urlFrame = self.createFrame(self.window, self.frameLayouts, self.urlFrameName)

        self.countMsgFrame = self.createNoneFrame(self.window)
        self.fileMsgFrame = self.createNoneFrame(self.window)
        self.progressFrame = self.createNoneFrame(self.window)

        # =============== CELLS LAYOUT ==================
        self.folderEntryName = 'folderEntry'; self.folderButtonName = 'Thư mục lưu'
        self.urlEntryName = 'urlEntry'; self.urlButtonName = 'Tải xuống'
        self.countMsgLabelName = 'countMsgLabelName'
        self.fileMsgLabelName = 'fileMsgLabelName'
        self.progressDownloadName = 'progressDownloadName'
        self.cellsLayouts = {
            self.folderEntryName: (1, 1), self.folderButtonName: (1, 2),
            self.urlEntryName: (1, 1), self.urlButtonName: (1, 2),
            self.countMsgLabelName: (1, 1),
            self.fileMsgLabelName: (1, 1),
            self.progressDownloadName: (1, 1),
        }
        
        self.folderEntry = self.createEntry(self.cellsLayouts, self.folderFrame, self.folderEntryName)
        self.insertEntryText(self.folderEntry, self.getRootDir())
        self.folderButton = self.createButton(self.cellsLayouts, self.folderFrame, self.folderButtonName, self.folderButtonCallback)
        
        self.urlEntry = self.createEntry(self.cellsLayouts, self.urlFrame, self.urlEntryName)
        self.urlButton = self.createButton(self.cellsLayouts, self.urlFrame, self.urlButtonName, self.urlButtonCallback)
        self.buttonClickValue = 0

    def download(self, inputUrl):
        self.countMsgFrame = self.createFrame(self.window, self.frameLayouts, self.countMsgFrameName)
        self.fileMsgFrame = self.createFrame(self.window, self.frameLayouts, self.fileMsgFrameName)

        self.createLabel('Đang lấy dữ liệu, đợi một chút...💨', self.cellsLayouts, self.countMsgFrame, self.countMsgLabelName)
        if 'tiktok.com' in inputUrl:
            savePathFolder = '{}\TikTok'.format(self.getEntryText(self.folderEntry))
            videoDataInfo = self.tiktok.getVideoData(inputUrl, savePathFolder)
        elif 'douyin.com' in inputUrl: 
            savePathFolder = '{}\DouYin'.format(self.getEntryText(self.folderEntry))
            videoDataInfo = self.douyin.getVideoData(inputUrl, savePathFolder)

        dataLength = len(videoDataInfo)
        for index in range(dataLength):
            saveFolder = videoDataInfo[index]['saveFolder']
            videoId = videoDataInfo[index]['videoId']
            videoUrlNoWatermark = videoDataInfo[index]['videoUrlNoWatermark']

            filename = f'{videoId}.mp4'
            filePath = f'{saveFolder}\{filename}'
            
            self.createFolder(saveFolder)
            saveFolderListDir = os.listdir(saveFolder)
            
            videoIndex = index + 1
            self.createLabel(f'✖ {videoIndex:>2} -/- {dataLength}  ✖\n\nFile {filename}', self.cellsLayouts, self.countMsgFrame, self.countMsgLabelName)
            
            try:
                if filename in saveFolderListDir:
                    self.createLabel('⛔ Đã tồn tại, bỏ qua tải xuống! ⛔', self.cellsLayouts, self.fileMsgFrame, self.fileMsgLabelName)
                    time.sleep(0.1)
                    continue
            except Exception as bug:
                print(f"Check file Exists: {bug}")
                pass

            self.progressFrame.destroy()
            self.progressFrame = self.createFrame(self.window, self.frameLayouts, self.progressFrameName)
            retryDownloadMax = 3
            for againNumber in range(retryDownloadMax):
                self.progressStyle, self.progressDownload = self.createProgress(self.cellsLayouts, self.progressFrame, self.progressDownloadName)
                self.progressDefault(f'{0:>10}% {0:>10}{"MB":<2}', self.progressStyle)
                try:
                    size = 0; chunkSize = 1024
                    for againNumber in range(3):
                        try:
                            video = requests.get(url=videoUrlNoWatermark, headers=self.headers, timeout=25)
                        except Exception as bug:
                            print(f"Download / video = request: {bug}")
                            continue
                    contentSize = int(video.headers['content-length'])
                    MBSize = round(contentSize / chunkSize / chunkSize, 2)

                    if video.status_code == 200:
                        with open(file=filePath, mode='wb') as file:
                            for data in video.iter_content(chunk_size=chunkSize):
                                file.write(data)
                                size = size + len(data)
                                self.percentage = round(size / contentSize * 100)
                                self.progressBarText = f'{self.percentage:>10}% {MBSize:>10}{"MB":<2}'
                                self.progressPercent(self.percentage, self.progressBarText, self.progressFrame, self.progressStyle, self.progressDownload)
                    break
                except Exception as bug:
                    print(f"Download: {bug}")
                    continue

        self.configActiveButton(self.folderButton, self.folderButtonName)            
        self.configEntryState(self.folderEntry, 1)
        self.configActiveButton(self.urlButton, self.urlButtonName)
        self.configEntryState(self.urlEntry, 1)
        
        self.deleteEntryext(self.urlEntry)
        if dataLength > 1:
            self.msg(msgs='❤❤❤❤ TẢI XUỐNG HOÀN TẤT! ❤❤❤❤', titles='Thông báo')

    def urlButtonCallback(self):
        inputUrl = self.getEntryText(self.urlEntry)
        inputSuccess = self.inputUrlCheck(inputUrl)
        if inputSuccess:
            self.buttonClickValue = self.buttonClickValue + 1

            self.configDisableButton(self.folderButton, self.folderButtonName)
            self.configEntryState(self.folderEntry, 0)
            self.configDisableButton(self.urlButton, 'Đang tải')
            self.configEntryState(self.urlEntry, 0) 
            
            if self.buttonClickValue > 1:
                self.countMsgFrame.destroy()
                self.fileMsgFrame.destroy()
                self.progressFrame.destroy()

            self.downloadThread = Thread(target = lambda: self.download(inputUrl))
            self.downloadThread.start()

    def folderButtonCallback(self):
        try:
            saveFolder = filedialog.askdirectory()
            if saveFolder:
                self.insertEntryText(self.folderEntry, saveFolder)
        except Exception as bug:
            self.insertEntryText(self.folderEntry, self.getRootDir())
            self.msg(f'{bug}')

    def inputUrlCheck(self, inputUrl):
        inputSuccess = False
        if 'tiktok.com' in inputUrl or 'douyin.com' in inputUrl:
            inputSuccess = True
        else:
            self.msg(msgs='Link không đúng, hãy kiểm tra lại!')
        
        return inputSuccess

    def getRootDir(selef):
        rootPath = ''
        if getattr(sys, 'frozen', False):
            rootPath = os.path.dirname(sys.executable)
        else: 
            try:
                rootPath = os.path.dirname(os.path.realpath(__file__))
            except NameError:
                rootPath = os.getcwd()
        return rootPath 

    def createFolder(self, folderPath):
        try: 
            if not os.path.exists(folderPath):
                os.makedirs(folderPath)
        except Exception as bug:
            print(bug)
            return

def main():
    try:
        app = APP()
        app.run()
    except Exception as bug:
        print(f"Main: {bug}")
        os.system('pause')

if __name__ == '__main__':
    main()