# coding: utf-8
from selenium import webdriver
from time import sleep, strftime
from random import randint
import os
from selenium.webdriver.common.keys import Keys


class Instgram:
    def __init__(self, driver_path=r'C:\Users\nomoj\Desktop\chromedriver.exe'):
        self.webdriver = webdriver.Chrome(executable_path=driver_path)
        self.prev_user_list = []
        self.followd = 0

    def login(self, username, password, login_url='https://www.instagram.com/accounts/login/?source=auth_switcher'):
        self.webdriver.get(login_url)
        sleep(5)
        usr = self.webdriver.find_element_by_name('username')
        usr.send_keys(username)
        pwd = self.webdriver.find_element_by_name('password')
        pwd.send_keys(password)
        sleep(3)
        try:
            button_login = self.webdriver.find_element_by_css_selector('#react-root > section > main > div > article > div > div:nth-child(1) > div > form > div:nth-child(4) > button > div')
        except:
            button_login = self.webdriver.find_element_by_css_selector('#loginForm > div > div:nth-child(3) > button > div')
        button_login.click()
        print(f'登录用户[{username}]')
        sleep(5)
        # 点击暂不需要按钮
        notnow = self.webdriver.find_element_by_css_selector('#react-root > section > main > div > div > div > div > button')
        notnow.click()
        sleep(5)
        # 点击稍后按钮
        self.webdriver.find_element_by_css_selector('body > div.RnEpo.Yx5HN > div > div > div > div.mt3GC > button.aOOlW.HoLwm').click()
        sleep(5)

    def open_tag(self, tag, is_first=True):
        if is_first:
            # 打开搜索tag页面
            self.webdriver.get(f'https://www.instagram.com/explore/tags/{tag}/')
            sleep(5)
            self.webdriver.find_element_by_xpath(
                '//*[@id="react-root"]/section/main/article/div[1]/div/div/div[1]/div[1]/a/div').click()
        else:
            # print(f'当前浏览器 {self.webdriver.current_window_handle}')
            # for handle in self.webdriver.window_handles:
            #     if handle != self.webdriver.current_window_handle:
            #         # self.webdriver.switch_to_window(handle)
            #         self.webdriver.switch_to.window(handle)
            #         break
            # print(f'切换之后浏览器 {self.webdriver.current_window_handle}')
            # sleep(3)
            self.webdriver.find_element_by_link_text('下一页').click()
        sleep(15)
        while True:
            if self.webdriver.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/header/div[2]/div[1]/div[2]/button').text == '关注':
                username = self.webdriver.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/header/div[2]/div[1]/div[1]/span/a').text
                print(f'username : {username}')
                return username
            else:
                self.webdriver.find_element_by_link_text('下一页').click()
                sleep(15)

    def open_thumbanil(self, username):
        self.webdriver.execute_script(f'window.open("https://www.instagram.com/{username}/");')
        sleep(5)
        # print(self.webdriver.current_window_handle)
        befor_handle = self.webdriver.current_window_handle
        for handle in self.webdriver.window_handles:
            if handle != befor_handle:
                # self.webdriver.switch_to_window(handle)
                self.webdriver.switch_to.window(handle)
                break

        # print(self.webdriver.current_window_handle)
        print(f'当前操作用户 [{username}]')
        try:
            user_already = self.webdriver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/div[2]/a/span').text
            if '位用户关注了' in user_already:
                print(f'[{user_already}]不会操作')
                self.webdriver.close()
                self.webdriver.switch_to.window(befor_handle)
                return
        except:
            pass
        if username not in self.prev_user_list:
            print(f'未追踪用户 [{username}]')
            self.webdriver.get(f'https://www.instagram.com/{username}/')
            sleep(5)
            self.webdriver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/span')
            like_num = self.webdriver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/span').text
            if '万' in like_num or len(like_num) > 3 or int(like_num) > 300:
                print(f'当前用户[{username}]点赞人数为[{like_num}]大于300，可以操作')
                # 点击关注
                try:
                    self.webdriver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/span/span[1]/button').click()
                except:
                    self.webdriver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/span/span[1]/button').click()
                # 点击发送消息
                sleep(15)
                self.webdriver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/button').click()
                sleep(8)
                text_ = self.webdriver.find_element_by_xpath(
                    '//*[@id="react-root"]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[2]/textarea')
                text_.send_keys(Keys.CONTROL, 'v')
                text_.send_keys(Keys.ENTER)
                sleep(5)
                self.webdriver.save_screenshot(
                    f'{os.path.abspath(os.path.dirname(__file__))}/screen_img/{username}.png')
            else:
                print(f'当前用户[{username}]点赞人数为[{like_num}]不足300，跳过')
        else:
            print(f'已操作过用户[{username}]不会操作')
        self.webdriver.close()
        self.webdriver.switch_to.window(befor_handle)


if __name__ == '__main__':
    i = Instgram()
    i.login('xxxxxx', 'xxxxxxx')
    tag_list = ["新北", "桃園", "臺中", "臺南", "高雄", "新竹", "臺北", "苗栗", "彰化", "南投", "雲林", "嘉義", "屏東", "宜蘭", "花蓮", "臺東", "澎湖", "金門", "連江", "基隆", "新竹", "嘉義",
"臺北美食", "新北美食", "桃園美食", "臺中美食", "臺南美食", "高雄美食", "新竹美食", "苗栗美食", "彰化美食", "南投美食", "雲林美食", "嘉義美食", "屏東美食", "宜蘭美食", "花蓮美食", "臺東美食", "澎湖美食", "金門美食", "連江美食", "基隆美食", "新竹美食", "嘉義美食"]
    for j in tag_list:
        for w in range(0, 200):
            if w == 0:
                un = i.open_tag(j, is_first=True)
            else:
                un = i.open_tag(j, is_first=False)
            i.open_thumbanil(un)
            sleep(60)
