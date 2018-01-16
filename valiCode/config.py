class Config:
		#验证码的url
	valiCodeUrl = 'http://login4.coobar.com/Index/verify/1516003805045'
	#'http://run.hbut.edu.cn/Account/GetValidateCode?time=1488614613244'
		#验证码提交地址url
	postUrl = 'http://login4.coobar.com/Login/dologin' 
	#'http://run.hbut.edu.cn/Account/LogOn'
		#登录页面的url
	hostUrl = 'http://login4.coobar.com/Login/index' 
	#'http://run.hbut.edu.cn/Account/LogOn?ReturnUrl=%2f'
		#搜索噪声的范围,如以3*3的大小来搜索整张图
	noiseRange = 3
		#消除噪声的标准，如在3*3大小内，若非白色的点小于2个就清除
	noiseClear = 2		#去噪后的图像保存地址，观察图片调整上面参数
	unNoiseIm = './unNoiseIm.png'
		#获取到的验证码图片，便于比对正确性
	valiCodeIm = './image.jpg'
		#验证码包含的字符
	iconset = ['0','1','2','3','4','5','6','7','8','9']
		#需要识别的验证码的每个内容的横坐标,使用画图工具判断
	letters = [(4,13),(14,22),(23,33),(34,44)] 
	#[(7,15),(16,24),(25,33),(35,43)]
		#是否训练样本
	isTrain = False 
		#相似度需要达到多少才算合格
	qualified = 0.94
	#训练集是否初始化
	initCode = False