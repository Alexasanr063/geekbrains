from clickhouse_driver import Client
import json

client = Client('localhost')

client.execute('CREATE DATABASE IF NOT EXISTS town_cary')

client.execute('''
CREATE TABLE IF NOT EXISTS town_cary.crashes (
    NAME String,
    TYPE String,
    COST Float64,
    STRENGTH String,
    WEAKNESS String,
    OPPORTUNITIES String,
    THREATS String,
    P_LOW Float64,
    P_HIGH Float64,
    YEARLY_LOW Float64,
    YEARLY_HIGH Float64
) ENGINE = MergeTree()
ORDER BY NAME
''')

print("Таблица создана")

with open('stock_data_0.json', 'r') as file:
    data = json.load(file)

values = []
for item in data:
    # Проверяем, что значения для P_LOW и других числовых столбцов являются числами
    p_low = item.get('P_LOW')
    if not isinstance(p_low, (int, float)):
        p_low =0.0 # Устанавливаем значение по умолчанию, если значение не число

    values.append((
        item['NAME'],
        item['TYPE'] or '',
        item['COST'] or 0.0,
        item['STRENGTH'] or '',
        item['WEAKNESS'] or '',
        item['OPPORTUNITIES'] or '',
        item['THREATS'] or '',
        p_low,
        item['P_HIGH'] or 0.0,
        item['YEARLY_LOW'] or 0.0,
        item['YEARLY_HIGH'] or 0.0
    ))

client.execute("""
INSERT INTO town_cary.crashes(
    NAME, TYPE, COST,
    STRENGTH, WEAKNESS, OPPORTUNITIES,
    THREATS, P_LOW, P_HIGH,
    YEARLY_LOW, YEARLY_HIGH
) VALUES""", values)

print("Данные успешно загружены")

result = client.execute("SELECT * FROM town_cary.crashes")
print("Наша таблица:", result)