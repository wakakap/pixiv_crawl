# pixiv_crawl
selenium+chromedriver+pyautogui

# 说明：

直接用urllib下载图片，经测试是不能下载这种dns污染的资源的。这里采用chromedriver右键保存策略，基本就是模拟真人操作，虽然下载效率很低，但应该不会被反爬虫。

# 更新记录：

pixiv_search_crawl.py 爬取pixiv搜索页面的所有页所有图片原图，目前只爬取满足定位元素的第一张，动图等其他格式则报错跳过。
