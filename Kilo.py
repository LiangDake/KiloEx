import csv
from telnetlib import EC
from selenium.webdriver import ActionChains
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from web3.middleware import geth_poa_middleware
from bit_api import *
import web3


web3 = web3.Web3(web3.HTTPProvider("https://opbnb-mainnet-rpc.bnbchain.org"))
# 连接公共节点需要注入此中间件
web3.middleware_onion.inject(geth_poa_middleware, layer=0)


# 网页元素基本操作
def element_input(path, content):  # 填入您需要操作的元素的路径以及内容
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, path))).send_keys(content)


def element_click(path):  # 填入您需要操作的元素的路径
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, path))).click()


def is_element_displayed(path):
    attempt = 5
    result = False
    while attempt > 0:
        try:
            driver.find_element(By.XPATH, path)
        except Exception:
            attempt -= 1
            time.sleep(1)
        else:
            result = True
            break
    return result


def web_jump_new():
    attempt = 5
    new_window_handle = None
    former_web = driver.current_window_handle
    while not new_window_handle and attempt > 0:
        for handle in driver.window_handles:
            if handle != former_web:
                new_window_handle = handle
        attempt -= 1
        time.sleep(1)
    driver.switch_to.window(new_window_handle)
    print(driver.title)
    return former_web


# 跳转至下一页面
def web_jump_next():
    handles = driver.window_handles
    driver.switch_to.window(handles[-1])


# 跳转至指定页面
def web_jump_to(handle):
    driver.switch_to.window(handle)


def web_scroll(path):  # 滚动到某个元素的位置
    element = driver.find_element(By.XPATH, path)
    driver.execute_script("arguments[0].scrollIntoView();", element)
    time.sleep(2)


def web_scroll_top():  # 滚动到页面顶部
    js = 'window.scrollTo(0,0)'
    driver.execute_script(js)


def import_private_key(file_name):
    with open(file_name, 'r') as file:
        # 从文件中加载JSON数据
        wallet_dictionary = json.load(file)
        wallet_number = 0
        for wallet in wallet_dictionary:
            private_key = wallet['privateKey']
            # Account1
            element_click('//*[@id="app-content"]/div/div[2]/div/button')
            # + Add account or hardware wallet
            element_click('/html/body/div[3]/div[3]/div/section/div[4]/button')
            # 导入账户
            element_click('/html/body/div[3]/div[3]/div/section/div[2]/div[2]/button')
            # 粘贴私钥
            element_input('//*[@id="private-key-box"]', private_key)
            # 导入
            element_click('/html/body/div[3]/div[3]/div/section/div[2]/div/div[2]/button[2]')
            wallet_number += 1
            print(f"{wallet['address']} 已导入至钱包，目前共 {wallet_number} 个钱包")
        print()
        print(f"{wallet_number} 个钱包已导入。")


def choose_wallet(number):
    action_chains = ActionChains(driver)
    # Account Button
    element_click('//*[@id="app-content"]/div/div[2]/div/button')
    # 滚动至第一个使用的账号位置
    path = "//*[contains(text(),'Account " + str(number) + "')]"
    # 点击切换账号
    is_element_displayed(path)
    element_click(path)
    # 账户选项
    element_click('//*[@id="app-content"]/div/div[2]/div/div[2]/div/div/button')
    # 账号详情
    element_click('//*[@id="popover-content"]/div[2]/button[1]')
    # 获取地址
    is_element_displayed('/html/body/div[3]/div[3]/div/section/div[2]/button')
    wallet_address = driver.find_element(By.XPATH, '/html/body/div[3]/div[3]/div/section/div[2]/div[2]/div['
                                                   '2]/div/div/button/span[1]/div').text
    # 显示私钥
    element_click('/html/body/div[3]/div[3]/div/section/div[2]/button')
    # 输入密码
    element_input('//*[@id="account-details-authenticate"]', 'Lkzxxzcsc2020')
    # 确认
    element_click('/html/body/div[3]/div[3]/div/section/div[5]/button[2]')
    # 长按以显示
    is_element_displayed('/html/body/div[3]/div[3]/div/section/div[2]/button')
    path = driver.find_element(By.XPATH, '/html/body/div[3]/div[3]/div/section/div[2]/button')
    action_chains.click_and_hold(path).perform()
    action_chains.release(path)
    # 获取私钥
    is_element_displayed('/html/body/div[3]/div[3]/div/section/div[3]/p')
    wallet_privateKey = driver.find_element(By.XPATH, '/html/body/div[3]/div[3]/div/section/div[3]/p').text
    wallet = {
        "address": wallet_address,
        "privateKey": wallet_privateKey
    }
    print(f'{wallet_address} 的私钥是 {wallet_privateKey}')
    return wallet


def account_upload(csv_file_name, account_list):
    with open(csv_file_name, 'a', newline='') as f:
        # Create a dictionary writer with the dict keys as column fieldnames
        writer = csv.DictWriter(f, fieldnames=account_list.keys())
        # Append single row to CSV
        writer.writerow(account_list)


if __name__ == '__main__':
    # 初始化
    res = openBrowser('fb4694579e4048729d3ea86de12c7b8a')  # 比特浏览器窗口ID
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", res['data']['http'])
    service = Service(executable_path=res['data']['driver'])

    driver = webdriver.Chrome(service=service, options=chrome_options)
    # driver.get('chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html')
    # # 导入所有钱包
    # import_private_key('2024-1-12_mnemonic_address_bot.json')

    # 手动进入KiloEx页面，点击小狐狸登录，全部选择
    # 手动点击设置成100X，完成后即可执行以下代码
    # 每个钱包必须至少有0.006BNB 和 11USDT
    # 每个钱包必须完成USDT_Approve操作

    # 第一个钱包的编号
    wallet_number = 46
    last_wallet_number = 53
    # 共完成任务账号数量
    signed_number = 0
    # 已完成钱包列表
    signed_wallets_list = {'address': '', 'privateKey': ''}
    while wallet_number <= last_wallet_number:
        # 小狐狸钱包切换账号
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get('chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html')
        wallet = choose_wallet(wallet_number)

        # 进入交易界面
        driver.get('https://app.kiloex.io/trade?sCode=3td669vtrk')
        time.sleep(3)
        # USDT Input
        element_input('//*[@id="app"]/div[1]/div/div[2]/div/div/section/div/section/main/div/div[2]/div[2]/div/div[2]/div/div/div[3]/div[2]/div[2]/div[2]/span/input', '1000')
        # 判断Buy/Long按钮是否能够点击
        if is_element_displayed('//*[@id="app"]/div[1]/div/div[2]/div/div/section/div/section/main/div/div[2]/div[2]/div/div[2]/div/div/div[3]/div[4]/div/button'):
            element_click('//*[@id="app"]/div[1]/div/div[2]/div/div/section/div/section/main/div/div[2]/div[2]/div/div[2]/div/div/div[3]/div[4]/div/button')
        # Confirm
        js = (
            "var elementsWithText = Array.from(document.querySelectorAll('*')).filter(function(element) {return element.innerText && element.innerText.includes('Confirm');});"
            "elementsWithText.forEach(function(element) {element.click();});")
        driver.execute_script(js)
        # 跳转小狐狸
        main_web = web_jump_new()
        # 确认
        is_element_displayed('//*[@id="app-content"]/div/div/div/div[3]/div[3]/footer/button[2]')
        element_click('//*[@id="app-content"]/div/div/div/div[3]/div[3]/footer/button[2]')
        # 返回主页面
        time.sleep(1)
        web_jump_to(main_web)
        # 等待下单
        time.sleep(10)
        # Close Market
        js = (
            "var elementsWithText = Array.from(document.querySelectorAll('*')).filter(function(element) {return element.innerText && element.innerText.includes('Market');});"
            "elementsWithText.forEach(function(element) {element.click();});")
        driver.execute_script(js)
        # Confirm
        js = (
            "var elementsWithText = Array.from(document.querySelectorAll('*')).filter(function(element) {return element.innerText && element.innerText.includes('Confirm');});"
            "elementsWithText.forEach(function(element) {element.click();});")
        driver.execute_script(js)
        # 跳转小狐狸
        web_jump_new()
        # 确认
        is_element_displayed('//*[@id="app-content"]/div/div/div/div[3]/div[3]/footer/button[2]')
        element_click('//*[@id="app-content"]/div/div/div/div[3]/div[3]/footer/button[2]')
        # 拒绝
        js = (
            "var elementsWithText = Array.from(document.querySelectorAll('*')).filter(function(element) {return element.innerText && element.innerText.includes('确认');});"
            "elementsWithText.forEach(function(element) {element.click();});")
        driver.execute_script(js)
        # 等待下单
        time.sleep(8)
        # 将完成账户存入csv文件
        signed_wallets_list['address'] = wallet['address']
        signed_wallets_list['privateKey'] = wallet['privateKey']
        account_upload('Signed_Wallets.csv', signed_wallets_list)
        signed_number += 1
        print(f"{signed_number}个钱包已执行完成，即将进行下一个")
        wallet_number += 1






