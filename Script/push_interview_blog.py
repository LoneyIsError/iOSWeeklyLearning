# -*- coding: UTF-8 -*-
import os
import sys
import argparse # 参数模块
import shutil
import time

blog_path = "/Users/zhangferry/zhangferry"


# 复制文件到目标路径
def moveFile(source):
    fileName = source.split("/")[-1]
    target = f"{blog_path}/Content/posts/{fileName}"
    dateStr = ""
    if os.path.exists(target):
        print("you had copy file before")
        titleArray = []
        with open(target, "r") as fileHandler:
            for line in fileHandler.readlines():
                # 遇到第二个 --- 符号就结束读取
                titleArray.append(line)
                if "---" in line and len(titleArray) > 1:
                    break
        titleArray.append("\n")
        dateStr = "".join(titleArray)

    shutil.copyfile(source, target)
    print("move file success")
    # print(dateStr)
    return (dateStr, target)

# 拼接标题头
def assemblyHeadText(title):
    topLine = "---"
    theTitle = f"title: {title}"
    date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    today = f"date: {date}"

    cover = "cover: https://gitee.com/zhangferry/Images/raw/master/iOSWeeklyLearning/moyu_weekly_cover.jpeg"
    tags = "tags:\n\t- 人物访谈"
    comments = "comments: true"
    emptyline = "\n"

    listStr = [topLine, theTitle, today, cover, tags, comments, topLine, emptyline]
    totalTitle = "\n".join(listStr)
    return totalTitle


# 修改文件
def modifyFile(filePath, titleStr):
    with open(filePath, "r+") as fileHandler:
        lines = fileHandler.readlines()
        
        newContent = []
        if len(titleStr) == 0:
            print("created new target file")
            title = lines[0].strip("#").strip()
            titleContent = assemblyHeadText(title)
            newContent.append(titleContent)
            print(len(lines))
            # print(lines.count())
        else:
            newContent.append(titleStr)
        # 内容处理
        for index in range(0, len(lines)):
            if index > 3:
                newContent.append(lines[index])
        fileHandler.seek(0)
        for newline in newContent:
            fileHandler.write(newline)

            
# 运行和发布
def runAndPublic(status):
    # os.system的执行每次都是开启一个subshell，导致更新执行目录退出来会复原，所以使用复合语句完成所有任务
    # 还可以使用os提供的os.chdir('/home/data')
    # os.system("python content_category.py")
    os.chdir(f"{blog_path}")
    if status == 1:
        os.system("publish run")
    elif status == 2:
        val = os.system('ls -al')
        # print(val)
        os.system("publish run && publish deploy")
    


parser = argparse.ArgumentParser(description='Input the weekly index')
parser.add_argument('--name', '-i', type=str, help='Please input the weekly index')
parser.add_argument('--status', '-status', type=int, required=False, help='you can asign is public, default is 0')

# main
if __name__ == '__main__':
    args = parser.parse_args()
    index = args.index
    publicStatus = args.status

    sourceFile = getSourceFile(index)
    print(sourceFile)
    targetPath = moveFile(sourceFile)
    # print(targetPath[1])
    modifyFile(targetPath[1], targetPath[0])
    runAndPublic(publicStatus)
    print("run Success!")
