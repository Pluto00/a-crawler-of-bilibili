Bilibili爬虫
============================================
主要思路
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

2.开始写一个简单爬虫
    
    由第一步的分析，我们可以确定这个zpi地址的请求方法为get,内容用json来进行解析;
    代码:response = requests.get("https://api.bilibili.com/x/web-interface/archive/stat?aid=2").json()
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
            "like": 10834,          # 点赞数
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
    
             
    
    
    
    
    
    
    
    
    
    
    
    
    
    
