Bilibili爬虫
============================================
--------------------------------------------
文件说明
--------------------------------------------
 1.main.py  开启多线程爬虫，并把数据写入mysql
 
 2.get_ip.py  爬取代理ip，给main.py调用
 
 3.test文件夹:    # 这部分文件没有参与我的爬虫，只是测试使用    

        creat_mysql..py 创建表格，字段
        Download.py  爬虫
        insert_mysql.py  数据插入mysql       
        test.cav  测试过程爬取到的一部分数据
 
 
-------------------------------------------- 
爬虫主要思路
--------------------------------------------
1.分析B站网页：

    B站的网页是动态加载的，用普通的requests.get方法是得不到数据的；
    通过查资料，我找到了一种通过api接口获取信息的方法。
    
2.找到视频信息的api地址：

    先打开B站视频的网站，用抓包工具，或者是浏览器自带的开发者工具对网页进行解析；
    我用的谷歌浏览器的开发者工具，查看Network界面(记得刷新一下);
    在Network我们可以看到网页请求了哪些地址及每个URL的网络相关请求信息：URL，响应状态码，响应数据类型响应时间等等；
    找到XHR(浏览器API)，任选一个http进行查看，我们可以看到响应头信息等等；
    再选择Response(响应)，看看有没有我们要找的信息，一条一条的找；
    然后在一个name为stat?aid=2(我打开的是av号为2的视频)response中看到了：
    
        {"code":0,"message":"0","ttl":1,"data": {"aid":2,"view":519676,"danmaku":28464,"reply":29170,"favorite":14593,"coin":5565,"share":3088,"like":10834,"now_rank":0,"his_rank":0,"no_reprint":0,"copyright":2}}
    
    仔细观察这些这些信息，会发现aid就是av号，view是播放量，danmaku是弹幕量；
    可以确定这个就是我们要找的地址，然后查看它的Headers：
        Request URL: https://api.bilibili.com/x/web-interface/archive/stat?aid=2
        Request Method: GET
        Content-Type: application/json; charset=utf-8
    我们找到了这几个关键信息，可以知道它的api地址，请求方法为GET,响应的格式为json；
    我终于们找到了想要的api地址：https://api.bilibili.com/x/web-interface/archive/stat?aid=2

2.开始写一个简单爬虫：
    
    由第一步的分析，我们可以确定这个api地址的请求方法为get,内容用json来进行解析;
    代码:
            response = requests.get("https://api.bilibili.com/x/web-interface/archive/stat?aid=2").json()
    
    这样子我们就把视频的信息抓了下来，接下来就是对信息进行提取；
    我们看一下响应的内容，用json解析工具可以得到：
    
             {
        "code": 0,
        "message": "0",
        "ttl": 1,
        "data": {
            "aid": 2,               # av号
            "view": 519676,         # 观看量
            "danmaku": 28464,       # 弹幕数
            "reply": 29170,         # 评论数
            "favorite": 14593,      # 收藏数
            "coin": 5565,           # 硬币数
            "share": 3088,          # 转发数
            "like": 10834,          # 好评数
            "now_rank": 0,          # 不清楚是啥
            "his_rank": 0,          # 不清楚是啥
            "no_reprint": 0,        # 同上两个
            "copyright": 2          # 同上三个
            }
        }
        
    有了这个格式，我们就可以对信息进行提取：
    代码：
            video_info = (
                response['data']['aid'], 
                response['data']['view'], 
                response['data']['danmaku'],
                response['data']['reply'], 
                response['data']['favorite'], 
                response['data']['coin'],
                response['data']['share'],
                response['data']['like'])
    可以简化为：
            data = response['data']
            video_info = (
                data['aid'], data['view'], data['danmaku'],
                data['reply'], data['favorite'], data['coin'],
                data['share'], data['like'])
    这样我们就把2号视频的信息爬取出来了；
    
3.爬取全站视频的信息：
    
    刚才爬取了2号视频的信息，现在开始爬取全站的视频的信息；
    观察刚才的api地址：https://api.bilibili.com/x/web-interface/archive/stat?aid=2
    发现最后有一个aid=2，aid是号，所以猜测api地址的构成是：
    'https://api.bilibili.com/x/web-interface/archive/stat?aid=' + 'av号'
    经过验证，确认没错，所以可以开始构造全站的api地址：
    代码：     
            api = 'https://api.bilibili.com/x/web-interface/archive/stat?aid='
            for av in range(1,100)：   # 根据要爬取的视频自己设置
                url = api + str(av)
                
    这样就把全站视频的api地址构造好了，然后对它进行第二步的处理就好了；
    
 4.让爬虫更健壮：
 
    我们已经写好了一个具备爬取全站视频的爬虫了，接下来就是让爬虫更加健壮了；
    主要讲讲ip代理池的设置：
        B站是使用https协议的网页，所以我们需要设置https的ip
        找到一个提供免费ip代理的网站：http://www.xicidaili.com/wn/
        写一个爬虫从它的页面上爬取ip；
        然后连接Telnet服务器测试ip是否可用；
        最后得到一些可用的ip代理
        代码：见get_ip.py文件
    
 5.把数据写入mysql：
 
    先在mysql中建一个表：
        代码:
        sql = """CREATE TABLE video (
                     aid  VARCHAR(11),
                     view  VARCHAR(11),
                     danmaku VARCHAR(11),  
                     reply VARCHAR(11),
                     favorite VARCHAR(11),
                     coin VARCHAR(11),
                     share VARCHAR(11),
                     awesome VARCHAR(11)  )"""  
        # 特别注意like是关键字，不能建立一个字段为like的字段，会报错....
    然后把数据插入:
        代码：
        sql = """insert into video 
                        (aid, view, danmaku, reply, favorite, coin, share) 
                        values(%s, %s, %s, %s, %s, %s, %s)"""
        # 注意要execute完后还要使用commit方法才能把数据写入到mysql里面
        
 6.多线程爬虫：
 
    可以开适量的线程来提升爬虫的速度；
    不过多线程写入数据库得开一个互斥锁，不然会报错.