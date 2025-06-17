"""
需求：每小时查询一次官网信息，如果2025年9月计算机二级报名相关通知被发布了，提醒用户
三大任务：
1.爬取网站数据并完成判定           （√）
2.关机状态下每小时运行一次爬虫程序   （ ）
【方案：借助  Github 平台资源】
3.判定通过后通知用户              （√）
"""

import requests
from bs4 import BeautifulSoup

# 通过微信通知用户（个人）

def send(title, inform, key):
    # 通过Server酱发送微信通知
    api_url = f"https://sctapi.ftqq.com/{key}.send"
    payload = {"title": title, "desp": inform}  # 构建了一个请求参数，用于向 Server 酱的 API 发送具体通知内容
    r2 = requests.post(api_url, data=payload)  # 请求并检查响应状态
    if r2.ok:
        print(r2, "\n通知发送成功")
    else:
        print(r2, "\n通知请求失败")


#爬虫完成 2025年9月计算机二级报名工作 是否启动的判定

head = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (HTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0"}#request会自动生成请求头
#手动更改请求头，使User-Agent中带上浏览器信息，将爬虫程序伪装成正常浏览器
r1 = requests.get("https://ncre.neea.edu.cn/html1/category/1507/872-1.htm", headers=head)#中国教育考试网
r1.encoding = "utf-8"#强制指定文件编码，避免汉字乱码
content = r1.text #获得html源码信息
if r1.ok:
    print(r1)
else:
    print(r1, "\n网站请求失败")
soup = BeautifulSoup(content, "html.parser")#获得解析后的对象
all_titles = soup.find_all("a", attrs={"target":"_self"})#将返回一个可迭代对象
register = 1
for a in all_titles:
    title_string = a.string#只保留内容string,不要标签
    if title_string and "2025年9月全国计算机等级考试报名" in title_string:#增加title_string and会自动检查 title_string 是否为 None 或空字符串
        print("报名开始啦！\n报名通知文件：" + title_string)
        register = 0
        send(title="计算机二级报名通知", inform=title_string, key="SCT282903Tm8T7OVkEk87EWz3kX8uc5RHr")#调用发送通知的函数
if register:
        print("2025年9月全国计算机等级考试报名工作【尚未】启动")


#每小时运行一次（要求关机实现）
