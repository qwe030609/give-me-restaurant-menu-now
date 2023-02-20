from bs4 import BeautifulSoup
from abc import ABC, abstractmethod
import requests


# 美食抽象類別
class Food(ABC):

    def __init__(self, area, foodtype):
        self.area = area  # 地區
        self.foodtype = foodtype  # 食物種類

    @abstractmethod
    def scrape(self):
        pass


# 愛食記爬蟲
class IFoodie(Food):

    def scrape(self):
        response = requests.get(
            "https://ifoodie.tw/explore/" + self.area +
            "/list/" + self.foodtype + "?sortby=rating")

        soup = BeautifulSoup(response.content, "html.parser")

        # 爬取前五筆餐廳卡片資料
        cards = soup.find_all(
            'div', {'class': 'jsx-2133253768 restaurant-item track-impression-ga'}, limit=5)

        content = ""
        for card in cards:

            title = card.find(  # 餐廳名稱
                "a", {"class": "jsx-2133253768 title-text"}).getText()

            stars = card.find(  # 餐廳評價
                "div", {"class": "jsx-1207467136 text"}).getText()

            address = card.find(  # 餐廳地址
                "div", {"class": "jsx-2133253768 address-row"}).getText()

            average_fee = card.find(  # 餐廳均消
                "div", {"class": "jsx-2133253768 avg-price"}).getText()

            # rempve space and comma
            average_fee = average_fee[2:]

            #將取得的餐廳名稱、評價及地址與均消連結一起，並且指派給content變數
            content += f"{title} \n{stars}顆星 \n{average_fee} \n{address} \n\n"

        return content

if __name__ == '__main__':
    try:
        keyword_area = "台中市"
        keyword_food = "漢堡"
        food = IFoodie(keyword_area, keyword_food)
        text = food.scrape()
        print(text)
        print("OK!")
    except:
        print("error!")
