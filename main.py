import iwaratool
i = iwaratool.user()
i.proxies = {'http':'http://127.0.0.1:7890','https':'http://127.0.0.1:7890'}
i.json = True
i.down = False
i.debug = True
w = open('D:\\code\\python\\iwaratool\\user.json', 'w+')
w.write(i.userVideos(url='https://www.iwara.tv/videos'))
