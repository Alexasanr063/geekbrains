import json
from pymongo import MongoClient

# Инициализация клиента
client = MongoClient('mongodb://localhost:27017/')

# Константы для имен базы данных и коллекции
DB_NAME = 'pyloungedb'
COLLECTION_NAME = 'youtubers'

# Подключение к базе данных и получение коллекции
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# Чтение данных из JSON
with open('stock_data_0.json', 'r') as file:
    data = json.load(file)

# Функция для разбиения данных на части
def chunk_data(data, chunk_size):
    for i in range(0, len(data), chunk_size):
        yield data[i:i + chunk_size]

# Размер чанка
chunk_size =50000
data_chunks = list(chunk_data(data, chunk_size))

# Вставка данных в базу
for chunk in data_chunks:
    try:
        collection.insert_many(chunk)
    except Exception as e:
        print(f"Ошибка при вставке данных: {e}")

print("Добавлена база данных")

# Подсчет документов
try:
    count = collection.count_documents({})
    print(f'Общее число документов: {count}')
except Exception as e:
    print(f"Ошибка при подсчете документов: {e}")

# Запросы к базе данных
queries = [
    {"COST": {'$lt':2}},
    {'COST': {'$gte':3}},
    {"STRENGTH": {'$regex': "Company", '$options': 'i'}},
    {'OPPORTUNITIES': {'$in': ["Positive", "Breakout"]}},
    {'properties.rdconfigur': {'$all': ["TWO-WAY", "DIVIDED"]}},
    {'properties.rdcondition': {'$ne': 'DRY'}}
]

for i, query in enumerate(queries, start=2):
    try:
        count = collection.count_documents(query)
        print(f'кол документов для запроса {i}: {count}')
    except Exception as e:
        print(f"Ошибка при выполнении запроса {i}: {e}")