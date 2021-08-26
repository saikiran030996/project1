from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
app = Flask(__name__)
@app.route('/',methods=['GET'])  # route to display the home page
@cross_origin()
def homePage():
    return render_template("index.html")
@app.route('/search',methods=['POST','GET']) # route to show the review comments in a web UI
@cross_origin()
def index():
    if request.method == 'POST':
        try:
            search_string = request.form['content'].replace("" , "")
            google_url = "https://www.google.com/images?q=" + search_string
            uclient = uReq(google_url)
            google_page = uclient.read()
            uclient.close()
            google_html = bs(google_page,'html.parser')
            print(google_html)
            filename = search_string + ".csv"
            fw = open(filename, "w")
            headers = "images_to_be_searched,URLs_link \n"
            fw.write(headers)
            links = []
            urls = []
            for raw_img in google_html.find_all('img'):
               link = raw_img.get('src')
               if link:
                   links.append(link)
            my_dict = {'images_to_be_searched':search_string,'URLs':links}
            urls.append(my_dict)
            return render_template('results.html', urls=urls[0:(len(urls)-1)])
        except Exception as e:
            print('The Exception message is: ',e)
            return 'something is wrong'
if __name__ == "__main__":
    #app.run(host='127.0.0.1', port=8001, debug=True)
	app.run(debug=True)