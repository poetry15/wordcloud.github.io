from datetime import datetime
dt_string = "2024/8/1 上午8:58:42"
dt_string = dt_string.replace("上午", "AM").replace("下午", "PM")
dt_object1 = datetime.strptime(dt_string, "%Y/%m/%d %p%I:%M:%S")
today = datetime.now().date()
print(today, dt_object1.date())