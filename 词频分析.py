import collections
import jieba
import wordcloud
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import re

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
print(word_counts_top50)
#生成词频图
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

