# 2023年12月20日
    好大夫headers
    :authority: www.haodf.com
    :method:    GET
    :path:  /
    :scheme:    https
    Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
    Accept-Encoding:    gzip, deflate, br
    Accept-Language:    zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6
    Cache-Control:  max-age=0
    Cookie: krandom_a119fcaa84=947981; g=3909_1698570580704; g=HDF.77.653e21073dffb; HMF_CI=3b827a4b3881da007e34c1138709aa2af3b23c844c3591f63d5545b04034d964b5bda328e0a7984393b8f44e260dc14d7ca8d1b6d53c39427b1e82b964d0a02d4f; Hm_lvt_dfa5478034171cc641b1639b2a5b717d=1701959974,1702962066,1703084256; userinfo[id]=10618917764; userinfo[name]=hdfzr4pxwys; userinfo[key]=AXwBMFNhUTdQO1JtU2hTMFU8DTZQZgFmBSwBbldlDWZWeQx%2BBjBWdlR2VSUAe1p7ByVRbVd%2B; userinfo[time]=1703084319; userinfo[ver]=1.0.2; userinfo[hostid]=0; sdmsg=1; Hm_lpvt_dfa5478034171cc641b1639b2a5b717d=1703084451
    Referer:    https://my.haodf.com/
    Sec-Ch-Ua:  "Not_A Brand";v="8", "Chromium";v="120", "Microsoft Edge";v="120"
    Sec-Ch-Ua-Mobile:   ?0
    Sec-Ch-Ua-Platform: "Windows"
    Sec-Fetch-Dest: document
    Sec-Fetch-Mode: navigate
    Sec-Fetch-Site: same-site
    Sec-Fetch-User: ?1
    Upgrade-Insecure-Requests:  1
    User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0

# 2023年12月21日
    好大夫爬取思路：
    网址：https://www.haodf.com/，然后进入到/doctor/list.html
    选择相应的科室医生进行爬取（也不一定是科室医生，也可能是按疾病找医生，这个需要按照毕设整体的思路，还需要考虑）
    /doctor/list-all-shaoshangneike.html?p=1（或者?p=2以此往后）
    在list中/html/body/div[2]/div/div[1]/div[2]/ul/li[1]即为某一个医生的相关资源
    其中包含链接，链接内有医生的专属编号（https://www.haodf.com/doctor/******.html）可以根据专属编号来判断是否爬取过
    还要判断医生是否包含头像（牛：https://n1.hdfimg.com/g2/M03/71/DC/yIYBAFw8OIyAQbw2AAAWC2_R7lQ743_200_200_1.png?8901，其他的要自己识别，应该不是很多）、是否开通在线问诊服务（直接在网页上提取文字“未开通”判断）

# 2023年12月22日
    可以三种方式都使用一遍
    1、requests+xpath
    2、selenium+webdriver
    3、scrapy

# 2023年12月24日
    验证过后：
    fuwu_wenzhen.html部分含有vue.js部分，无法使用requests进行爬取；selenium速度太慢；
    现在的比较好的方法有两个：可以使用requests爬取的用requests，剩下的用selenium；全部使用scrapy

    现在的想法是全部使用scrapy
    scrapy学习地址：https://www.runoob.com/w3cnote/scrapy-detail.html、https://blog.csdn.net/ck784101777/article/details/104468780
    
    注意注释，最好不用中文（2.6.1）
    运行spider时注意scrapy版本，2.6.1时运行会出现openssl的错误，更新到2.11.0时可以正常运行
    运行时返回2023-12-24 15:46:10 [scrapy.core.engine] INFO: Spider closed (finished)代表了执行完成

# 2023年12月25日
    scrapy保存数据四种方式（-o输出指定格式的文件）：
    1、scrapy crawl 爬虫名 -o 文件名.json
    2、scrapy crawl 爬虫名 -o 文件名.jsonl  #json lines 格式，默认为unicode编码
    3、scrapy crawl 爬虫名 -o 文件名.csv    #csv逗号表达式，表格
    4、scrapy crawl 爬虫名 -o 文件名.xml    #xml格式

    若打印的文件乱码，设置FEED_EXPORT_ENCODING = 'UTF-8'即可，具体见scrapy文档

    文件结构（生成内容：医生生成内容、患者生成内容、系统生成内容；虽然是三个部分，但都是围绕医生展开的）图像、文本、数值
    -Hdaof
    --doctor.json(包含doctorID（主键）、)
    --patient.json(包含doctorID（主键）)
    --doctorIMG
    ---****id.jpg

# 2023年12月26日
    估计要使用疾病来查找医生
    -Hdaof
    --doctor.json(包含doctorID（主键）、姓名、职称、医院、医院等级、文字简介、价格、暖心记录次数)
    --patient.json(包含doctorID（主键）、患者评论数、患者礼物数量)
    --system.json(包含doctorID（主键）、年度好大夫次数、病友推荐度、治疗经验（服务星、诊治患者数、随访患者数）、得票数)
    --doctorIMG
    ---****id.jpg
    --comment
    ---doctorID.json(包含日期时间、疗效满意度、治疗方式、态度满意度、目前病情状态、评论内容、序号、是否包含图片保证真实性)