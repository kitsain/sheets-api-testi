# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import webapp2
import cgi

import gspread
import oauth2client.service_account as service_account
# from oauth2client.service_account import ServiceAccountCredentials
import pprint
	
from datetime import datetime


# https://stackoverflow.com/questions/41246976/getting-chunkedencodingerror-connection-broken-incompleteread
# from requests_toolbelt.adapters import appengine
# appengine.monkeypatch()

# https://stackoverflow.com/questions/12664696/how-to-properly-output-json-with-app-engine-python-webapp2

# from webapp2_extras import json

import json

from googlesheets.google_sheet_manager import GoogleSheetManager

# use creds to create a client to interact with the Google Drive API
scopes = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials_path = 'client_secret.json'
# creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scopes)
# client = gspread.authorize(creds)

#import urllib.requests
#from urllib.parse import unquote
from lxml import html
import requests

k_eanurl = "https://www.k-ruoka.fi/kauppa/tuote/"

eanurl = k_eanurl

enableskräpäys = True

# scrape, scrape, scrape: https://docs.python-guide.org/scenarios/scrape/
def findTitle(url):
    pass

def findKProductName(EAN):
    url = eanurl + EAN
    page = requests.get(url)
    tree = html.fromstring(page.content)

    product = tree.xpath('//*[@id="app"]/section/section/div[2]/div[2]/div/div/div/div/div[1]/section/section[1]/div[2]/h1/span/text()')
    return(product[0])

def findIngredients(EAN):
    url = eanurl + EAN
    page = requests.get(url)
    tree = html.fromstring(page.content)

    ingredients = tree.xpath('//*[@id="product-basic-details"]/div/div[1]/p[1]/span/text()')
    return(ingredients[0])

class KaljaaForm(webapp2.RequestHandler):

# check_value = request.POST['user']
# userr = self.request.post('user')        
# request = Request.blank('/KaljaaForm')
# request.method = 'POST'
     # https://www.jqueryscript.net/other/jQuery-Plugin-For-Easily-Readable-JSON-Data-Viewer.html



    def get(self):
#       userr.content = self.request.get('userr')
        self.response.write("""
        <html><head></head>
        
        <body>
        <form action="/KaljaaForm" method="get">
        <p>
        Namez: <input type="text" name="user" autofocus>
        </p>
        <p>
        Message <input type="text" name="message" >
        </p>
        <p>
        <input type="Submit" value="Send">

        </p>
        </body>
        </form>
            """)

        self.form_user = self.response.out.write(cgi.escape(self.request.get('user')))
        self.form_message = self.response.out.write(cgi.escape(self.request.get('message')))
        manager = GoogleSheetManager(credentials_path='client_secret.json', sheet_id="161eZSq0ETZWdExmrkr3pVyIqilB_Oh1Yq59fZcm00n4")
        manager.start_session()
        rows = manager.get_all_rows()
        cols = manager.get_col_values(2)
        self.timestamp = str(datetime.now())
        new_row = (self.timestamp, self.form_user, self.form_message)
        manager.append_row(new_row)
        manager.insert_row(new_row, 2)
#        write(userr)
      
        self.response.write("""
        </html>
            """)

class KaljaaFormEAN(webapp2.RequestHandler):

# check_value = request.POST['user']
# userr = self.request.post('user')        
# request = Request.blank('/KaljaaForm')
# request.method = 'POST'
     # https://www.jqueryscript.net/other/jQuery-Plugin-For-Easily-Readable-JSON-Data-Viewer.html


    def get(self):
#       userr.content = self.request.get('userr')
        self.response.write("""
        <html><head></head>
        
        <body>
        <form action="/KaljaaFormEAN" method="get">
        <p>
        EAN: <input type="text" name="user" autofocus>
        </p>
        <p>
        Tuote: <input type="text" name="message" >
        </p>        
        <p>
        Hinta: <input type="text" name="price" >
        </p>
        <p>
        <input type="Submit" value="Send">

        </p>
        </body>
        </form>
            """)
        if self.request.get('user'):
            self.form_user = cgi.escape(self.request.get('user'))
            self.response.out.write(self.form_user)
            self.form_message = cgi.escape(self.request.get('message'))
            self.response.out.write(self.form_message)
            self.form_price = cgi.escape(self.request.get('price'))
            self.response.out.write(self.form_price)
            self.response.write("""
            </br>
            </br>
                """)
            print(self.form_user,self.form_price)
            # form_price = str(self.response.out.write(cgi.escape(self.request.get('price'))))
            manager = GoogleSheetManager(credentials_path='client_secret.json', sheet_id="161eZSq0ETZWdExmrkr3pVyIqilB_Oh1Yq59fZcm00n4")
            manager.start_session()
            rows = manager.get_all_rows()
            cols = manager.get_col_values(2)
            #Get EAN Title from K-Kauppa https://www.k-ruoka.fi/kauppa/tuote/6413600015550
            url = eanurl + self.form_user
            print(url)
            if enableskräpäys:
                self.product_name = findKProductName(self.form_user)
            else:
                self.product_name = self.form_user
            self.response.out.write(self.product_name)
            self.response.write("""
            </br>
            </br>
                """)
            if enableskräpäys:
                self.ingredients = findIngredients(self.form_user)
            else:
                self.ingredients = self.form_user
            self.response.out.write(self.ingredients)
            self.response.write("""
            </br>
            </br>
                """)
            self.timestamp = str(datetime.now())
            self.new_row = (self.timestamp, self.form_user, self.product_name, self.form_message, self.ingredients, self.form_price)
            #manager.append_row(self.new_row)
            manager.insert_row(self.new_row, 2)
    #        write(userr)
      
        self.response.write("""
        </html>
            """)

        
class KaljaaMsgCan(webapp2.RequestHandler):
    def get(self):
        self.response.write
    
    
class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello, World! wot-test')


class Kaljaa(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'application/json'   
        obj = {
        	'success': 'some var', 
        	'payload': 'some var',
        	} 
        self.response.write(json.dumps(obj))

        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = service_account.credentials.from_json_keyfile_name('client_secret.json', scopes)
        client = gspread.authorize(creds)
 


        sheet = client.open("hinnat01b").sheet1
        
        pp = pprint.PrettyPrinter()
        
        list_of_hashes = sheet.get_all_records()
        web = pp.pprint(list_of_hashes)
        
class Kaljaa2(webapp2.RequestHandler):
    def get(self):                     
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = service_account.credentials.from_json_keyfile_name('client_secret.json', scopes)
        client = gspread.authorize(creds)
 


        sheet = client.open("hinnat01b").sheet1
        
        pp = pprint.PrettyPrinter()
        
        list_of_hashes = sheet.get_all_records()
        self.response.headers['Content-Type'] = 'application/json'   
        self.response.write(json.dumps(list_of_hashes))
        
class Kaljaa3(webapp2.RequestHandler):
    def get(self):
                
        #scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        #creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scopes)
        #client = gspread.authorize(creds)
 


        #sheet = client.open("hinnat01").sheet1
        
        #pp = pprint.PrettyPrinter()
        
        from webapp2_extras import json
        
        list_of_hashes = sheet.get_all_records()
        #web = pp.pprint(list_of_hashes)
        #self.response.headers['Content-Type'] = 'application/json'   
        #self.response.write(json.dumps(pp.pprint(list_of_hashes)))
        self.response.headers['Content-Type'] = 'application/json'   
        self.response.write(json.encode(list_of_hashes))

# https://stackoverflow.com/questions/26724083/how-to-load-html-page-with-python-on-app-engine
class Quagga(webapp2.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'quagga/camera_example.html') 
        self.response.out.write(template.render(path, {}))        
        
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/kaljaa', Kaljaa),
    ('/kaljaa2', Kaljaa2),
    ('/kaljaa3', Kaljaa3),
    ('/KaljaaForm', KaljaaForm),
    ('/KaljaaFormEAN', KaljaaFormEAN),
    ('/can', KaljaaMsgCan),
], debug=True)
