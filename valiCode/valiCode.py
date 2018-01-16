from PIL import Image
import os
import time
import re  
import math
import urllib  
import urllib.request  
import http.cookiejar  
import string
from html.parser import HTMLParser  
from urllib.parse import urlparse 
from time import sleep
from config import Config

class ValiCode:
	#def __init__() 
	#print %
	def __init__(self):
		self.valiCodeUrl = Config.valiCodeUrl
		self.postUrl = Config.postUrl
		self.hostUrl = Config.hostUrl
		self.noiseRange = Config.noiseRange
		self.noiseClear = Config.noiseClear
		self.unNoiseIm = Config.unNoiseIm
		self.valiCodeIm = Config.valiCodeIm
		self.iconset = Config.iconset
		self.letters = Config.letters
		self.isTrain = Config.isTrain
		self.qualified = Config.qualified
		self.initCode = Config.initCode
	
	#计算阈值，用以将普通图形转化为黑白
	def thresholds(self,im):
		x,y=im.size
		n=x*y
		max=0
		for i in range(256):
			n1=0
			n2=0
			h2=0
			h1=0
			for m in im.getdata():
				if m>= i:
					n2+=1
					h2+=m
				else:
					n1+=1
					h1+=m
			if n1==0 or n2== 0:
				continue
			w1=n1/n
			w2=n2/n
			u1=h1/n1
			u2=h2/n2
			mile=w1*w2*(u1-u2)**2
			if mile >max:
				max=mile
				treshold=i
			else:
				continue
		return treshold
	
	#计算指定大小范围内点的密度，如计算5*5大小类 白色以外点的个数
	def numpoint(self,im):
		w,h = im.size
		data = list( im.getdata() )
		mumpoint=0
		for x in range(w):
			for y in range(h):
				if data[ y*w + x ] !=255:#255是白色
					mumpoint+=1
		return mumpoint
	
	#把指定范围类非白色的点的个数少于指定数目的点全部变成白色，用以去除噪声
	def pointmidu(self,im):
		w,h = im.size
		noiseRange = self.noiseRange
		noiseClear = self.noiseClear
		p=[]
		for y in range(0,h,noiseRange):
			if(y+noiseRange>h):
				d=h
			else:
				d=y+noiseRange
			for x in range(0,w,noiseRange):
				if(x+noiseRange>w):
					m=w
				else:
					m=x+noiseRange
				box = (x,y, m,d)
				im1=im.crop(box)
				a=self.numpoint(im1)
				if a<noiseClear:##如果5*5范围内小于11个点，那么将该部分全部换为白色。
					for i in range(x,m):
						for j in range(y,d):
							im.putpixel((i,j), 255)
							
		im.save(self.unNoiseIm)
		
	#计算向量间求cos值的分母，形如 根号下a^2+b^+c^
	def magnitude(self,concordance):
		total = 0
		for word,count in concordance.items():
			total += count ** 2
		return math.sqrt(total)

    #计算矢量之间的 cos 值
	def relation(self,concordance1, concordance2):
		relevance = 0
		topvalue = 0
		for word,count in concordance1.items():
			if word in concordance2:
				topvalue += count * concordance2[word]
		return topvalue / (self.magnitude(concordance1) * self.magnitude(concordance2))
	
	#把图片转化为向量
	def buildvector(self,im):
		d1 = {}
		count = 0
		for i in im.getdata():
			d1[count] = i
			count += 1
		return d1
		
	#从网上获取验证码图片，保存在本地
	def getValiCode(self):
		yzmurl = self.valiCodeUrl
		hosturl = self.hostUrl
		postUrl = self.postUrl
		cj = http.cookiejar.LWPCookieJar()  
		cookie_support = urllib.request.HTTPCookieProcessor(cj)  
		opener = urllib.request.build_opener(cookie_support, urllib.request.HTTPHandler)  
		urllib.request.install_opener(opener)  
		#打开登录主页面（他的目的是从页面下载cookie，这样我们在再送post数据时就有cookie了，否则发送不成功）  
		h = urllib.request.urlopen(hosturl)
		picture = opener.open(yzmurl).read()
		local = open(self.valiCodeIm,'wb')
		local.write(picture)
		local.close()
		
	#加载训练集
	def loadTrain(self):
		iconset = self.iconset
		imageset = []
		for letter in iconset:
			temp = []
			if not os.listdir('./yzm/%s/'%(letter)):
				print('初始样本为空，请先添加初始样本')
				exit()
			for img in os.listdir('./yzm/%s/'%(letter)):
				temp.append(self.buildvector(Image.open("./yzm/%s/%s"%(letter,img))))
			imageset.append({letter:temp})
		return imageset

	#把验证码转化为向量，并与训练集进行比较
	def compare(self):
		self.getValiCode()
		#print(imageset)
		im=Image.open(self.valiCodeIm)
		imgry = im.convert("L")
		threshold=self.thresholds(imgry)
		table = []
		for i in range(256):
			if i < threshold:
				table.append(0)
			else:
				table.append(1)
		out = imgry.point(table,'1')
		change=out.convert("P")
		self.pointmidu(change)
		im2=Image.open(self.unNoiseIm)
		imageset = self.loadTrain()
		letters = self.letters
		ocr=[]
		for letter in letters:
			im3 = im2.crop(( letter[0] , 0, letter[1],im2.size[1] ))
			if self.initCode:
				im3.save('./%s.gif'%time.time())
				continue
			guess = []
			for image in imageset:
				for x,y in image.items():
					if len(y) != 0:
				#print(len(y))
						for i in range(len(y)):
							#print(y[i])
							guess.append( (self.relation(y[i],self.buildvector(im3)),x) )
			guess.sort(reverse=True)
			if self.isTrain:
				if guess[0][0]< self.qualified:
					print(guess[0])
					im3.save("./yzm/%s.gif"%time.time())
				continue
			else:
				print(guess[0])
				ocr.append(guess[0][1])
		if self.initCode:
			return
		if self.isTrain:
			return
			
			
		yzm=''
		for i in range(len(ocr)):
			yzm+=ocr[i]	
		print(yzm.strip())	
		return yzm.strip()
			
			
			
if __name__ == "__main__":
	a = ValiCode() 
	a.compare()
	