

# Выберите веб-сайт с табличными данными, который вас интересует.
# Напишите код Python, использующий библиотеку requests для отправки HTTP GET-запроса на сайт и получения HTML-содержимого страницы.
# Выполните парсинг содержимого HTML с помощью библиотеки lxml, чтобы извлечь данные из таблицы.
# Сохраните извлеченные данные в CSV-файл с помощью модуля csv.

import  requests
from lxml import html
import csv
import pandas as pd

url = 'https://finance.yahoo.com/trending-tickers/'

response = requests.get(url, headers={
'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'})

tree = html.fromstring(response.content)

table_rows = tree.xpath("//table[@class='W(100%)']/tbody/tr")

data_list = [] # в этом списке будем хранить словари с данным из каждой строки
for row in table_rows:
     data = {}
     columns = row.xpath(".//td/text()")

     data['Symbol'] = row.xpath(".//td[1]/a/text()")[0].strip()
     data['Name'] = columns[0].strip()
     data['Last_prace'] = row.xpath(".//td[3]/fin-streamer/text()")[0].strip()
     data['Marker_time'] = row.xpath(".//td[4]/fin-streamer/text()")[0].strip()
     data['Change'] = row.xpath(".//td[5]/fin-streamer/span/text()")[0].strip()
     data['%Change'] = row.xpath(".//td[6]/fin-streamer/span/text()")[0].strip()
     data['Volume'] = row.xpath(".//td[7]/fin-streamer/text()")[0].strip()
     data['Marker_Cap'] = ''.join(row.xpath(".//td[8]/fin-streamer/text()")) if row.xpath(".//td[8]/fin-streamer/text()") else 'ничего нету'
     data_list.append(data)
for i in data_list:
    print(i)

# Создание DataFrame
df = pd.DataFrame(data_list)

# Путь к файлу CSV
csv_file_path = "data.csv"

# Запись DataFrame в файл CSV
df.to_csv(csv_file_path, index=False)

print("Данные успешно записаны в файл CSV.")