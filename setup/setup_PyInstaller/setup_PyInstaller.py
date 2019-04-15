# -*- coding: utf-8 -*-

"""
打包成 exe 可执行文件
需要先安装 PyInstaller
目录结构为:
WFACat\setup\setup_PyInstaller\setup_PyInstaller.py
WFACat\WFACatPro\main.py
打包好的文件会生成在 WFACat\setup\setup_PyInstaller\dist 文件夹下
命令行直接运行的命令：
pyinstaller --icon="../../asset/icon_128.ico" --name="WFACatPro" -F -c "../../WFACatPro/main.py"
"""


import os


if __name__ == '__main__':
    os.system(" pyinstaller --icon=\"../../asset/icon_128.ico\" --name=\"WFACatPro\" -F -c \"../../WFACatPro/main.py\" ")
