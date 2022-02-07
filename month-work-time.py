import requests
import json
import time
from datetime import datetime

# 需要替换的内容
# token
# 月
# 月开始 月结束
token = ""
month = "2022-01"
monthDayStart = 1
monthDayEnd = 31


def _get_request(data: object) -> object:
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36",
        "Content-Type": "application/json;charset=UTF-8",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "X-Requested-With": "XMLHttpRequest",
        "token": token,
        "sec-ch-ua-platform": "Windows",
        "Origin": "https://ics.chinasoftinc.com:18010",
        "Referer": "https://ics.chinasoftinc.com:18010/",
        "Accept-Language": "en,zh-CN;q=0.9,zh;q=0.8",
    }
    response = requests.post("https://ics.chinasoftinc.com:18010/ehr_saas/web/attEmpLog/getAttEmpLogByEmpId2.empweb?",
                             data=data,
                             headers=header)
    return response.json()


def calculate(start, end):
    if start == '' or end == '':
        return 0
    num = 0
    startTime = datetime.strptime(start, "%Y-%m-%d %H:%M:%S")
    sb = datetime(startTime.year, startTime.month, startTime.day, 8)
    if sb > startTime:
        startTime = sb
    endTime = datetime.strptime(end, "%Y-%m-%d %H:%M:%S")

    xb1 = datetime(startTime.year, startTime.month, startTime.day, 17, 30)
    xb2 = datetime(startTime.year, startTime.month, startTime.day, 18, 00)
    if endTime > xb1 and endTime < xb2:
        endTime = xb1

    if endTime > xb2:
        num = -0.5

    work = endTime - startTime
    hour = work.total_seconds() / 3600 + num - 1.5
    return float(hour)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    dayNum = 0
    hourNum = 0

    for i in range(monthDayStart, monthDayEnd):
        response = _get_request(json.dumps({"dt": month + "-" + str(i) + " 00:00:00"}))
        dtDetailList = response['result']['data']['attEmpDetail']['dtDetailList']
        if dtDetailList[0]['sbTitle'] == "上班":
            dayNum += 1
            start = response['result']['data']['attEmpDetail']['checkIn2']
            end = response['result']['data']['attEmpDetail']['checkOut2']
            workTime = calculate(start, end)
            hourNum += workTime
            print("打卡时间" + start + "---" + end + "工作时长:" + str(workTime))
        time.sleep(0.2)
    print("工作天数", dayNum)
    print("工作小时", hourNum)
    print("总需要 day*8", dayNum * 8)
    print("总需要加班 day*9", dayNum * 9)
