# pixiv_crawl
selenium+chromedriver

# 说明：

本代码的环境是通过修改hosts文件，并在校园网（能使用google.hk）情况下登录pixiv，尚未尝试vpn代理的情况。

直接用urllib下载图片，经测试是不能下载这种dns污染的资源的。所以这里采用chromedriver右键保存策略，基本就是模拟真人操作，虽然下载效率很低。

# 目录：

pixiv_search_crawl.py 爬取pixiv搜索页面的所有页所有图片原图。

收藏夹爬取等其他页面待补全，exe化待后续完善。
