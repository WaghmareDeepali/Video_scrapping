from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import logging
logging.basicConfig(filename="scrapper.log" , level=logging.INFO)

app = Flask(__name__)

@app.route("/", methods = ['GET'])
def homepage():
    return render_template('index.html')

@app.route("/review" , methods = ['POST' , 'GET'])
def index():
    if request.method == 'POST':
        try:
            chrome_option = webdriver.ChromeOptions()
            chrome_option.add_argument("--headless")

            driver = webdriver.Chrome(options=chrome_option)
            driver.maximize_window()

            searchString = request.form['content']

            driver.get(searchString)

            url_box = driver.find_elements(By.XPATH, '//*[@id="video-title-link"]')
            thumbnail_box = driver.find_elements(By.XPATH, '//*[@id="thumbnail"]/yt-image/img')
            title_box = driver.find_elements(By.XPATH, '//*[@id="video-title"]')
            views_box = driver.find_elements(By.XPATH, '//*[@id="metadata-line"]/span[1]')
            time_box = driver.find_elements(By.XPATH, '//*[@id="metadata-line"]/span[2]')

            reviews = []


            for i, j, k, l, m in zip(url_box, thumbnail_box, title_box, views_box, time_box):
                reviews.append([i.get_attribute('href'), j.get_attribute('src'), k.text, l.text, m.text])

            # print(data_scrap)
            # data = pd.DataFrame(data_scrap, columns=['Video URL', 'Thumbnails', 'Titles', 'Views', 'Upload Time'])
            # data.to_csv('url scrapper.csv')
            
            logging.info(f"log my final result {reviews}")
            return render_template('result.html', reviews=reviews[:5])

        except Exception as e:
            logging.info(e)
            return 'something is wrong'

if __name__=="__main__":
    app.run(host="0.0.0.0")


    


