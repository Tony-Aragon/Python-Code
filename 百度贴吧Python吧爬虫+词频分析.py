#-*-coding:utf-8-*-
# 第一页：https://tieba.baidu.com/f?kw=%C0%EE%D2%E3&fr=ala0&tpl=5&traceid=也可以将pn=0代入，构造成统一格式
# 第二页：https://tieba.baidu.com/f?kw=%E6%9D%8E%E6%AF%85&ie=utf-8&pn=50
# 第三页：https://tieba.baidu.com/f?kw=%E6%9D%8E%E6%AF%85&ie=utf-8&pn=100
# 第四页：https://tieba.baidu.com/f?kw=%E6%9D%8E%E6%AF%85&ie=utf-8&pn=150
# https://tieba.baidu.com/f?kw=python&ie=utf-8&pn=
import requests
import re
import time
import random
import numpy as np
import collections
import jieba
import wordcloud
from PIL import Image
import matplotlib.pyplot as plt
from multiprocessing.dummy import Pool
url = 'https://tieba.baidu.com/f?kw=python&ie=utf-8&pn='
topic = []
user_agent = [
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
    "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11"]
urls = []
k = 1 		#计数变量
#循环嵌套结构，构造一次url，就读取内容并存入topic列表中
for i in range(50):
	url = 'https://tieba.baidu.com/f?kw=python&ie=utf-8&pn='
	num = 50*i
	url = url + str(num)										#字符串采用+进行连接
	urls.append(url)

def creeper(url):
	headers = {"User-Agent":random.choice(user_agent)}
	time.sleep(1)												#睡眠时间1s，避免由于频繁访问引起服务器拒绝访问
	#print("正在爬取第" + str(i+1) + "页的数据.......................................")
	html = requests.get(url,headers=headers)
	content = html.text
	titles = re.findall('title="(.*?)" target="_blank" class="',content)
	global k
	print("正在爬取第" + str(k) + "页的内容")
	k+=1
	for each in titles:
		topic.append(each)

time1 = time.time()
pool = Pool(4)
result = pool.map(creeper,urls)
pool.close()
pool.join()
time2 = time.time()

# 打印topic中的内容
#k=1
#for every in topic:
	#print("第" + str(k) + "个帖子标题为：" + every)
	#k+=1

print("采用4线程的所花的时间为：" + str(time2-time1))

#将爬取到的数据写入文件
f=open("Python贴吧-前50页标题爬取.txt","w",encoding="utf-8")#电脑打开txt的方式默认为gbk，网络数据编码一般采用utf-8，因此在打开文件时应采用utf-8模式
for each in topic:
	f.write(each)
f.close()



#词频分析模块
#pattern=re.compile(u'\t|\n|\.|-|:|;|\)|\(|\?|"')
#cut_topic=re.sub(pattern,'',str(topic))

#seg_list_exact=jieba.cut(cut_topic,cut_all=False)
#object_list=[]
#remove_words=[u'的', u'，',u'和', u'是', u'随着', u'对于', u'对',u'等',u'能',u'都',u'。',u' ',u'、',u'中',u'在',u'了',u'通常',u'如果',u'我们',u'需要',u'？',u'！',u',',u'我',u'们',u'吧',u'这',u'吗',u"'"]
#for word in seg_list_exact:
	#if word not in remove_words:
		#object_list.append(word)

#word_counts=collections.Counter(object_list)
#word_counts_top50=word_counts.most_common(50)
#print(word_counts_top50)


#绘制词频图模块
f=open("Python贴吧-前50页标题爬取.txt",encoding="utf-8")
data=f.read()
f.close()

pattern=re.compile(u'\t|\n|\.|-|:|;|\)|\(|\?|"')
cut_data=re.sub(pattern,'',data)

slice_word=jieba.cut(cut_data,cut_all=False)
object_list=[]
remove_words=[u'的', u'，',u'和', u'是', u'随着', u'对于', u'对',u'等',u'能',u'都',u'。',u' ',u'、',u'中',u'在',u'了',u'通常',u'如果',u'我们',u'需要',u'？',u'！',u',',u'我',u'们',u'吧',u'这',u'吗',u"'"]
for word in slice_word:
	if word not in remove_words:
		object_list.append(word)

word_counts=collections.Counter(object_list)
word_counts_top50=word_counts.most_common(50)
print(word_counts_top50)           #输出词频排名前50的词语与对应的次数
#词频图的生成
mask=np.array(Image.open('wordcloud1.jpg'))
wc=wordcloud.WordCloud(
	font_path='C:/Windows/Fonts/simhei.ttf',
	mask=mask,
	max_words=200,
	max_font_size=100)
wc.generate_from_frequencies(word_counts)
image_colors=wordcloud.ImageColorGenerator(mask)
wc.recolor(color_func=image_colors)
plt.imshow(wc)
plt.axis('off')
plt.show()