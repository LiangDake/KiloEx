import requests
import json
import time

# 官方文档地址
# https://doc2.bitbrowser.cn/jiekou/ben-di-fu-wu-zhi-nan.html

# 此demo仅作为参考使用，以下使用的指纹参数仅是部分参数，完整参数请参考文档

url = "http://127.0.0.1:54345"
headers = {'Content-Type': 'application/json'}


def createBrowser():  # 创建或者更新窗口，指纹参数 browserFingerPrint 如没有特定需求，只需要指定下内核即可，如果需要更详细的参数，请参考文档
    json_data = {
        'url': '',  # 打开的url，多个用,分开
        'name': 'google',  # 窗口名称
        'remark': '',  # 备注
        'userName': '',  # 用户账号
        'password': '',  # 用户密码
        'cookie': '',  # Cookie，符合标准的序列化字符串，具体可参考文档
        # IP库，默认ip-api，选项 ip-api | ip123in | luminati，luminati为Luminati专用
        'ipCheckService': 'ip-api',
        'proxyMethod': 2,  # 代理方式 2自定义 3 提取IP
        # 代理类型  ['noproxy', 'http', 'https', 'socks5', '911s5']
        'proxyType': 'noproxy',
        'host': '12.132.234.12',  # 代理主机
        'port': 99999,  # 代理端口
        'proxyUserName': '',  # 代理账号
        'proxyPassword': '',  # 代理密码
        'ip': '',  # ip
        'city': '',  # 城市
        'province': '',  # 州/省
        'country': '',  # 国家地区
        'dynamicIpUrl': '',  # 提取IP url，参考文档
        'dynamicIpChannel': '',  # 提取IP服务商，参考文档
        'isDynamicIpChangeIp': True,  # 提取IP方式，参考文档
        'isGlobalProxyInfo': False,  # 提取IP设置，参考文档
        'isIpv6': False,  # 是否是IP6
        'syncTabs': True,  # 同步标签页
        'syncCookies': True,  # 同步Cookie
        'syncIndexedDb': False,  # 同步IndexedDB
        'syncLocalStorage': False,  # 同步 Local Storage
        'syncBookmarks': True,  # 同步书签
        'credentialsEnableService': False,  # 禁止保存密码弹窗
        'syncHistory': False,  # 保存历史记录
        'clearCacheFilesBeforeLaunch': False,  # 启动前清理缓存文件
        'clearCookiesBeforeLaunch': False,  # 启动前清理cookie
        'clearHistoriesBeforeLaunch': False,  # 启动前清理历史记录
        'randomFingerprint': False,  # 每次启动均随机指纹
        # 浏览器窗口工作台页面，默认 chuhai2345,不展示填 disable 可选 chuhai2345 | localserver | disable
        'workbench': 'chuhai2345',
        'disableGpu': False,  # 关闭GPU硬件加速 False取反 默认 开启
        'enableBackgroundMode': False,  # 关闭浏览器后继续运行应用
        'disableTranslatePopup': False,  # 翻译弹窗
        'syncExtensions': False,  # 同步扩展应用数据
        'syncUserExtensions': False,  # 跨窗口同步扩展应用
        'allowedSignin': False,  # 允许google账号登录浏览器
        'abortImage': False,  # 禁止加载图片
        'abortMedia': False,  # 禁止视频自动播放
        'muteAudio': False,  # 禁止播放声音
        'stopWhileNetError': False,  # 网络不通停止打开
        "browserFingerPrint": {  # 指纹对象
            'coreVersion': '104'  # 内核版本 112 | 104，建议使用112，注意，win7/win8/winserver 2012 已经不支持112内核了，无法打开
        }
    }

    res = requests.post(f"{url}/browser/update",
                        data=json.dumps(json_data), headers=headers).json()
    browserId = res['data']['id']
    print(browserId)
    return browserId


def updateBrowser():  # 更新窗口，支持批量更新和按需更新，ids 传入数组，单独更新只传一个id即可，只传入需要修改的字段即可，比如修改备注，具体字段请参考文档，browserFingerPrint指纹对象不修改，则无需传入
    json_data = {'ids': ['93672cf112a044f08b653cab691216f0'],
                 'remark': '我是一个备注', 'browserFingerPrint': {}}
    res = requests.post(f"{url}/browser/update/partial",
                        data=json.dumps(json_data), headers=headers).json()
    print(res)


def openBrowser(id):  # 直接指定ID打开窗口，也可以使用 createBrowser 方法返回的ID
    json_data = {"id": f'{id}'}
    res = requests.post(f"{url}/browser/open",
                        data=json.dumps(json_data), headers=headers).json()
    print(res)
    print(res['data']['http'])
    return res


def closeBrowser(id):  # 关闭窗口
    json_data = {'id': f'{id}'}
    requests.post(f"{url}/browser/close",
                  data=json.dumps(json_data), headers=headers).json()


def deleteBrowser(id):  # 删除窗口
    json_data = {'id': f'{id}'}
    print(requests.post(f"{url}/browser/delete",
          data=json.dumps(json_data), headers=headers).json())


if __name__ == '__main__':
    browser_id = createBrowser()
    print(browser_id)

