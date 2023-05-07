import re
import fitz
import ocrspace
import sqlite3
from bs4 import BeautifulSoup
import requests
import re
import wget
from uuid import uuid4
import datetime
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent


db_path = BASE_DIR / 'db.sqlite3'

con = sqlite3.connect(db_path)
c = con.cursor()
pages = [6,7,8,9]
size = 1.2

TEST_FILENAME = 'image.png'
content1 = requests.get("https://www.tuiost.edu.np/result").text
regex = r"^(?!.*\btotal\w*\b)(?!.*\bmake\w*\b)(?=.*\bcsit\b)(?=.*\bresult\b).+$"

def scrapper():
      soup = BeautifulSoup(content1, 'lxml')
      results = soup.find_all('div', class_ = 'mt-3')

      for result in results:
         pdf_title = result.find('b', class_='').text
         pdf_link = result.find('a', class_ ='text-primary small').get("href")
         if re.match(regex, pdf_title, re.IGNORECASE):
            file = str(uuid4())
            c.execute('SELECT * FROM result_downloads WHERE name=?', (pdf_title,))
            existing_data = c.fetchone()

            if existing_data:
               print('Data already exists in the table')

            else:
               now = datetime.datetime.now()
               wget.download(pdf_link, "downloads/{}.pdf".format(file))

               for page1 in pages:
                   
                convert(file,page1,size)
                passer(file,page1)
               c.execute('INSERT INTO result_downloads (key, name, date, link) VALUES (?, ?, ?,?)', (file,pdf_title,now.strftime('%Y-%m-%d %H:%M:%S'),pdf_link))
               con.commit()


      now = datetime.datetime.now()
      id = uuid4().hex
      c.execute('UPDATE result_update SET id=?, time=? WHERE rowid=(SELECT rowid FROM result_update LIMIT 1)', (id, now.strftime('%Y-%m-%d %H:%M:%S')))

      con.commit()
      con.close()


            

def convert(file,page1,size):
    pdffile = "downloads/{}.pdf".format(file)
    doc = fitz.open(pdffile)
    zoom = size
    mat = fitz.Matrix(zoom, zoom)

    val = TEST_FILENAME
    try:
        page = doc.load_page(page1)
    except ValueError:
        print("Error: Page number out of range.")
        doc.close()
        return
    pix = page.get_pixmap(matrix=mat)
    pix.save(val)
    doc.close()

def extract():
    api = ocrspace.API(endpoint='https://api.ocr.space/parse/image', api_key='K87043301788957', language=ocrspace.Language.English)

    result= api.ocr_file(TEST_FILENAME)

    array_result = result.split("\r\n")

    pattern = r'27[4-9][6-9]\d*'

    filtered_list = []

    for x in array_result:
       matches = re.findall(pattern, x)
       for match in matches:
          match_num = int(match[:5])
          if 27464 <= match_num <= 27499:
             filtered_list.append(match_num)

    passed = len(filtered_list)

    filtered_list = sorted(filtered_list)
    return filtered_list

def database():
   
   symbol_numbers = extract()

   for t in symbol_numbers:
      con.execute("UPDATE turesult SET result='Failed' WHERE symbol_num<>?",[t])
      con.commit()
   
   for i in symbol_numbers:
       con.execute("UPDATE turesult SET result='Passed' WHERE symbol_num=?",[i])
       con.commit()


   for j in con.execute("SELECT * FROM turesult WHERE result='Passed'"):
         print(j)   
   
   con.close() 


def passer(file,page1):
   
   try:
    symbol_numbers = extract()
   except Exception as e:
      if 'File failed validation. File size exceeds the maximum permissible file size limit of 1024 KB' in str(e):
         print("\nFile size is too big , compressing more")
         size = 1.1
         convert(file,page1,size)
         symbol_numbers = extract()
      else:
        print("Error:", e)

   
   for t in symbol_numbers:
      today = datetime.date.today()
      id = uuid4().hex
      c.execute('INSERT INTO result_results (id, key, symbol_num, date) VALUES (?,?, ?, ?)', (id,file,t,today))
      con.commit()
   
    
   print("Updated")

scrapper()
