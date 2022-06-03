import os
from TikTok import TikTok
from DouYin import DouYin

def main():
    try:
        # tikTok = TikTok()
        # tikTok.main()

        douyin = DouYin()
        douyin.main()
    except Exception as bug:
        print(bug)
        os.system('pause')

if __name__ == '__main__':
    main()