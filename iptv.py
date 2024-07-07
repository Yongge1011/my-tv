import requests
import requests
from lxml import etree
import pandas as pd
cookies = {
    'REFERER': '20251163',
    'REFERER2': 'MzzbEr3aNbzcYO0O0O',
    'REFERER1': 'NzzbUr0aObTckO0O0O',
    'ASPSESSIONIDASRQQCCR': 'CFNNPJBAFJEOPOHELFJKFIDP',
    '_ga': 'GA1.1.489028414.1720270596',
    'HstCfa4835840': '1720270608054',
    'HstCmu4835840': '1720270608054',
    'HstCnv4835840': '1',
    'HstCns4835840': '1',
    'HstCla4835840': '1720271288572',
    'HstPn4835840': '5',
    'HstPt4835840': '5',
    '_ga_8KY4MGK2FJ': 'GS1.1.1720270596.1.1.1720271374.0.0.0',
}

headers = {
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    # 'Cookie': 'REFERER=20251163; REFERER2=MzzbEr3aNbzcYO0O0O; REFERER1=NzzbUr0aObTckO0O0O; ASPSESSIONIDASRQQCCR=CFNNPJBAFJEOPOHELFJKFIDP; _ga=GA1.1.489028414.1720270596; HstCfa4835840=1720270608054; HstCmu4835840=1720270608054; HstCnv4835840=1; HstCns4835840=1; HstCla4835840=1720271288572; HstPn4835840=5; HstPt4835840=5; _ga_8KY4MGK2FJ=GS1.1.1720270596.1.1.1720271374.0.0.0',
    'Referer': 'http://foodieguide.com/iptvsearch/hotellist.html?s=125.36.76.224:8888',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}

ip = input('请输入ip :')
if not ip:
    ip ="125.36.76.224:8888"
response = requests.get(
    f'http://foodieguide.com/iptvsearch/alllist.php?s={ip}&y=false',
    cookies=cookies,
    headers=headers,
    verify=False,
)
result = response.text
# print(result)

html = etree.HTML(result)
station_names =html.xpath('//div[@class = "result"]/div/a/div[1]/text()')
stream_urls =html.xpath('//div[@class = "m3u8"]/table/td[2]/text()')
# print(channel_name_date,channel_url_date)

# 确保两个列表长度相同
assert len(station_names) == len(stream_urls), "电视台名称和直播URL地址的数量必须相同"

m3u_content = "#EXTM3U\n"  # 文件开始的声明

for name, url in zip(station_names, stream_urls):
    if "天津" in name:
        group_title = "天津本地"
    elif "CCTV" in name:
        group_title = "CCTV央视"
    elif "卫视" in name:
        group_title = "地方卫视"
    else:
        group_title = "其他"

    m3u_content += "#EXTINF:-1,tvg-id=\"{}\" tvg-name=\"{}\" tvg-logo=\"http://example.com/logo/{}.png\" group-title=\"{}\",{}\n{}\n".format(
        name.replace(" ", ""),  # 频道ID，假设没有空格
        name,  # 频道名称
        name.replace(" ", ""),  # 频道logo，假设logo文件名与频道名称相同且没有空格
        group_title,  # 分组名称
        name,  # 显示的频道名称
        url  # 直播URL
    )

print(m3u_content)
with open('stations.m3u', 'w', encoding='utf-8') as f:
    f.write(m3u_content)