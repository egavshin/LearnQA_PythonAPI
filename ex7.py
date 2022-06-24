import requests

codeList = ['get','post', 'put', 'delete']

# 1. Делает http-запрос любого типа без параметра method, описать что будет выводиться в этом случае.
for i in range(len(codeList)):
    st = f"requests.{codeList[i]}('https://playground.learnqa.ru/ajax/api/compare_query_type')"
    response = eval(st)
    print(response.text)

# 2. Делает http-запрос не из списка. Например, HEAD. Описать что будет выводиться в этом случае.
response = requests.head('https://playground.learnqa.ru/ajax/api/compare_query_type')
print(response)

response = requests.get('https://playground.learnqa.ru/ajax/api/compare_query_type', params={'method':'GET'})
print(response.status_code)
print(response.text)

# 3. Делает запрос с правильным значением method. Описать что будет выводиться в этом случае.
for i in range(len(codeList)):
    params = 'data'
    if codeList[i] == 'get':
        params = 'params'
    st = "requests." + codeList[i] + "('https://playground.learnqa.ru/ajax/api/compare_query_type'," + params + "= {'method':'" + codeList[i].upper() + "'})"
    print(st)
    response = eval(st)
    print(response.status_code)
    print(response.text)

# 4. С помощью цикла проверяет все возможные сочетания реальных типов запроса и значений параметра method. Например с GET-запросом
# передает значения параметра method равное ‘GET’, затем ‘POST’, ‘PUT’, ‘DELETE’ и так далее. И так для всех типов запроса.
# Найти такое сочетание, когда реальный тип запроса не совпадает со значением параметра, но сервер отвечает так, словно все ок.
# Или же наоборот, когда типы совпадают, но сервер считает, что это не так.

for i in range(len(codeList)):
    params = 'params'
    for j in range(len(codeList)):
        if codeList[i] != 'get':
            params = 'data'
        st = "requests." + codeList[i] + "('https://playground.learnqa.ru/ajax/api/compare_query_type'," + params + "= {'method':'" + codeList[j].upper() + "'})"
        print(st)
        response = eval(st)
        print(response.text)