import requests
import re
import json

def regular(self, r):
    videos = re.findall(self.expression['videos']['Url-Title'], r.text)
    videosID = re.findall(self.expression['videos']['VideosID'], r.text)
    like = re.findall(self.expression['videos']['like'], r.text)
    look = re.findall(self.expression['videos']['look'], r.text)
    covers = re.findall(self.expression['videos']['covers'], r.text)
    name = re.findall(self.expression['videos']['name'], r.text)
    Title = []
    url = []
    download = []
    status_code = {
        'code':r.status_code,
        'data_code':[]
        }
    
    if self.debug:
        print('目前已执行到获取下载地址的地方')

    for i in range(len(videosID)):    
        Title.append(videos[i][1])
        url.append('https://www.iwara.tv' + videos[i][0])
        if self.down == True:
            try:
                r = requests.get(self.downApi + videosID[i], headers=self.headers, proxies=self.proxies, verify=self.verify)
            except requests.exceptions.ProxyError:
                if self.debug:
                    raise requests.exceptions.ProxyError('远程主机强迫关闭了一个连接')
                r.status_code = 404
            else:
                if r.status_code == 200:
                    download.append(r.json())
            status_code['data_code'].append(r.status_code)
            if self.debug:
                print('目前正在获取第{}条下载地址'.format(i+1))
    # self.user['videos']['title'] = Title 
    # self.user['videos']['url'] = url
    # self.user['videos']['id'] = videosID
    # self.user['videos']['like'] = like
    # self.user['videos']['look'] = look
    # self.user['videos']['pages'] = 1
    # self.user['videos']['down'] = download
    # self.user['videos']['covers'] = covers
    # self.user['videos']['name'] = name


    self.user['videos'].update({'pages':0})
    for i in range(len(videosID)):
        try:
            if self.down:
                self.user['videos']['data'].append({
                    'code':status_code['code'],
                    'name':name[i],
                    'title':Title[i],
                    'id':videosID[i],
                    'like':like[i],
                    'look':look[i],
                    'url':url[i],
                    'covers':covers[i],
                    'down':{
                        'code':status_code['data_code'][i],
                        'data':download[i]
                    }
                })
            else:
                self.user['videos']['data'].append({
                    'code':status_code['code'],
                    'name':name[i],
                    'title':Title[i],
                    'id':videosID[i],
                    'like':like[i],
                    'look':look[i],
                    'url':url[i],
                    'covers':covers[i],
                    'down':{}
                })
        except IndexError:
            if len(like) == 35:
                like.append('缺少了一条数组')
            if self.debug:
                # 这里大多情况是like这里出了问题
                # 建议用设置好的正则测试一下要爬取的url
                # 如果是35个的话那就是i站的问题 0收藏是不会显示的 除非获取视频地址的源码获取like收藏才会不出错
                raise IndexError('这里报了一个IndexError错误 请自行判断')
    if self.debug:
        print('有惊无险，成功执行')
    return self


def get(self, videoall=False):
    if videoall == True:
        r = requests.get(self.url, headers=self.headers, proxies=self.proxies, verify=self.verify)
        if r.status_code == 200:
            pages = range(0, re.findall(self.expression['videos']['pages'],r.text)['0'])
            for i in ranges:
                if i == 0:
                    self = regular(self=self, r=r) # 未完工 留个坑
    else:
        try:
            r = requests.get(self.url + '?page={}'.format(self.page),headers=self.headers, proxies=self.proxies, verify=self.verify)
        except requests.exceptions.ProxyError:
            self.user['videos']['code'] = 'Error:requests.exceptions.ProxyError'
        else:
            if r.status_code == 200:
                self = regular(self=self, r=r)
    return self

class user():
    def __init__(self):
        r'''
        down 是否获取下载地址（注意，设置了代理的下载也需要设置一样的代理 否则会下载失败）
        title_all 是否获取全部标题 会导致返回速度更慢
        page  不填默认为0 则第一页
        '''
        self.downApi = 'https://www.iwara.tv/api/video/'
        self.url = ''
        self.json = False #False:直接返回字典类型 True:直接返回json文本
        self.verify = True # ssl证书
        self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'} # 请求头
        self.proxies = {} # 设置代理
        self.other = False # 获取其他信息（如简介，标签等）；默认为False不获取 未完成，进度：做到获取简介的正则 但未完成
        self.page = 0
        self.down = True
        self.title_all  = False
        self.debug = False

        self.indent = 4
        self.separators=(',',': ')
        # 这两个选项是json格式返回是否格式化的变量 默认格式化

        self.expression = {
            'user':{
            'about':'<div class=".* views-field-field-about">.*>(.*?)\n', #关于 也是用户简介
            'name':'<span.*><h2>(.*?)</h2>',#用户名称
            'JoinDate':'Join date.*<span.*>(.*?)</span>', #加入时间
            'LastSeen':'Last seen.*<span.*><.*">(.*?)</em>(.*?)</span>', #最后一次上线，这里列表有2个
            'Url-Title':'<h3.*<a href="(.*)">(.*)</a></h3>',#包含视频图片标题和地址 单数标题，双数地址（包括0）
            'VideosID':'/videos/(\w.*)"><img' #视频ID
        },
        'videos':{
            'name':'<.*class="username">(.*?)</a>',
            'Url-Title':'<h3.*<a href="(.*)">(.*)</a></h3>',#包含视频图片标题和地址 单数标题，双数地址（包括0）
            'VideosID':'/videos/(\w.*)"><img', #视频ID  
            'like':'class="glyphicon glyphicon-heart"></i> (.*?)\t*</div>',
            'look':'class="glyphicon glyphicon-eye-open"></i> (.*?)\t*</div>',
            'covers':'img src="//(.*?)."',
            'pages':'pager-last last.*page=(.*)"' # 获取最大页数 使用方法：获取最大页数，取0-最大页数的数值 比如用range(0,最大页数)         
        }
        } #如无特别情况请勿修改这些正则表达式

        self.user = {
            'videos':{
                'pages':-1,
                'data':[]
            }
        }
        # self.user = {
        #     'videos':{
        #         'name':'?',
        #         'pages':0,
        #         'code': 200,
        #         'id':[],
        #         'title':[],
        #         'url':[],
        #         'look':[],
        #         'like':[],
        #         'down':[],
        #         'covers':[]
        #     }
        # } #json
    def userVideos(self,url=''):
        r'''直接获取视频，不获取其他多余数据
        '''
        if url:
            self.url = url
        elif self.url == '':
            raise ValueError('url参数为空！')
        if self.page >= 0:
            get(self,videoall=False)        
        
        if self.json:
            return json.dumps(self.user,separators=self.separators, indent=self.indent)
        else:
            return self.user
    def userImages(self,url='', page=0):
        r'''直接获取图片地址，不获取其他多余数据
        如果page = -1 将获取全部 不填默认为0 则第一页
        '''
        if url != '':
            self.url = url
        elif self.url == '':
            raise ValueError('url参数为空！')
        pass
    def userHome(self,url=''):
        r'''这里会获取作者主页全部内容
        包括但不限于：图片 视频 简介 名称
        url参数清输入作者主页
        '''
        if url != '':
            self.url = url
        elif self.url == '':
            raise ValueError('url参数为空！')
        pass