from datetime import datetime

def is_year_month_in_range(year, month, start_date, end_date):
    # 构造datetime对象
    date_to_check = datetime(year, month, 1)

    # 检查日期是否在给定范围内
    return start_date <= date_to_check <= end_date

# 输入时间范围的开始和结束年月
start_year = int(input("请输入开始年份："))
start_month = input("请输入开始月份（英文缩写）：")
end_year = int(input("请输入结束年份："))
end_month = input("请输入结束月份（英文缩写）：")

# 转换输入的月份缩写为对应数字
month_dict = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}
start_month_num = month_dict.get(start_month.capitalize())
end_month_num = month_dict.get(end_month.capitalize())

if start_month_num is None or end_month_num is None:
    print("月份输入有误，请使用英文缩写，如 'Jan'、'Feb' 等。")
    exit()

# 构造开始和结束时间的datetime对象
start_date = datetime(start_year, start_month_num, 1)
end_date = datetime(end_year, end_month_num, 1)

# 输入的年份和月份
year_to_check = int(input("请输入要检查的年份："))
month_to_check = input("请输入要检查的月份（英文缩写）：")

# 转换输入的月份缩写为对应数字
month_to_check_num = month_dict.get(month_to_check.capitalize())

if month_to_check_num is None:
    print("月份输入有误，请使用英文缩写，如 'Jan'、'Feb' 等。")
    exit()

# 调用函数判断年份和月份是否在范围内
result = is_year_month_in_range(year_to_check, month_to_check_num, start_date, end_date)

if result:
    print(f"{year_to_check} {month_to_check} 在指定的时间范围内。")
else:
    print(f"{year_to_check} {month_to_check} 不在指定的时间范围内。")
