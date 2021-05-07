import iwaratool
i = iwaratool.iwaratool()
i.proxies = {'http':'http://127.0.0.1:7890','https':'http://127.0.0.1:7890'}
i.jsonp = True
w = open('D:\\code\\python\\iwaraDownload\\user.json', 'w+')
w.write(i.userVideos(url='https://www.iwara.tv/users/%E6%98%AD%E5%92%8C%E6%87%90%E5%8F%A4%E3%81%8A%E3%82%84%E3%81%A2/videos'))