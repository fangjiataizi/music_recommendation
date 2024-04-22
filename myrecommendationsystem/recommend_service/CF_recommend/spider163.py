import requests
from bs4 import BeautifulSoup


def get_song_attr(song_id):
    url = 'https://www.9ku.com/play/{}.htm'.format(song_id)
    response = requests.get(url)
    print(response.status_code)
    # 确保请求成功
    if response.status_code == 200:
        html_content = response.text
        # print(html_content)
        soup = BeautifulSoup(html_content, 'html.parser')
        # 提取标题
        title = soup.find('meta', property='og:title')['content']

        # 提取演唱者
        artist = soup.find('meta', property='og:music:artist')['content']

        # 提取评分
        rating_span = soup.find('span', id='rankNum')
        print(rating_span)
        rating_em = rating_span.find('em').text  # 获取<em>标签内的文本
        rating = rating_em + rating_span.text.split(rating_em)[-1]
        print(f"标题: {title}")
        print(f"演唱者: {artist}")
        print(f"评分: {rating}")
        return response.status_code,title, artist, rating,url
    else:
        print("无法获取网页内容，状态码:", response.status_code)
        return response.status_code, None, None, None,None





if __name__ == '__main__':
    url = 'https://www.9ku.com/play/875689.htm'
    response = requests.get(url)
    print(response.status_code)
    # 确保请求成功
    if response.status_code == 200:
        html_content = response.text
        # print(html_content)
        soup = BeautifulSoup(html_content, 'html.parser')
        # 提取标题
        title = soup.find('meta', property='og:title')['content']

        # 提取演唱者
        artist = soup.find('meta', property='og:music:artist')['content']

        # 提取评分
        rating_span = soup.find('span', id='rankNum')
        print(rating_span)
        rating_em = rating_span.find('em').text  # 获取<em>标签内的文本
        rating = rating_em + rating_span.text.split(rating_em)[-1]
        print(f"标题: {title}")
        print(f"演唱者: {artist}")
        print(f"评分: {rating}")
    else:
        print("无法获取网页内容，状态码:", response.status_code)
