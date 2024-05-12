s = 'Showing metabocard for 4-Hydroxy-6-nonadecanone (HMDB0035674)'
result = s[len('Showing metabocard for '):]
print(result)
import re

# 示例字符串
s = "TG(8:0/i-13:0/i-16:0) (HMDB0072475)"

# 使用正则表达式提取HMDB后面的数字
match = re.search(r'HMDB\d{7}', s)

if match:
    hmdb_string = match.group()

# 打印提取的字符串
print(hmdb_string)  # 输出 HMDB0072475



