import requests
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool

headers = {'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:41.0) Gecko/20100101 Firefox/41.0'}

#Создаем функцию получения данных по адресу
def getDataFromAddress(address):
    address = '%20'.join('%2C'.join(address.split(',')).split(' ')) #Получаем адрес, заменяем запятые на %2C, а пробелы на %20
    link = 'https://catalog.api.2gis.ru/3.0/items?type=street%2Cadm_div.city%2Ccrossroad%2Cadm_div.settlement%2Cstation%2Cbuilding%2Cadm_div.district%2Croad%2Cadm_div.division%2Cadm_div.region%2Cadm_div.living_area%2Cattraction%2Cadm_div.place%2Cadm_div.district_area%2Cbranch%2Cparking%2Cgate%2Croute&page=1&page_size=12&q='+address+'&locale=ru_RU&fields=request_type%2Citems.adm_div%2Citems.context%2Citems.attribute_groups%2Citems.contact_groups%2Citems.flags%2Citems.address%2Citems.rubrics%2Citems.name_ex%2Citems.point%2Citems.geometry.centroid%2Citems.region_id%2Citems.segment_id%2Citems.external_content%2Citems.org%2Citems.group%2Citems.schedule%2Citems.timezone_offset%2Citems.ads.options%2Citems.stat%2Citems.reviews%2Citems.purpose%2Csearch_type%2Ccontext_rubrics%2Csearch_attributes%2Cwidgets%2Cfilters&stat%5Bsid%5D=91e1c495-9e55-4ca9-8712-e15073071f6e&stat%5Buser%5D=a8e546d0-291f-4778-bc72-1f84d55dcdfc&key=ruoedw9225&r=1831242903' # передаем предобработанный адрес в запрос
    answer = requests.get(link, headers=headers) # делаем запрос
    return json.loads(answer.content.decode('utf-8')) # возвращаем ответ в виде json


def getDataFromBuildings(building_id):
    link = 'https://catalog.api.2gis.ru/2.0/catalog/branch/list?building_id='+str(building_id)+'&locale=ru_RU&fields=items.region_id%2Citems.segment_id%2Citems.reviews%2Citems.adm_div%2Citems.contact_groups%2Citems.flags%2Citems.address%2Citems.rubrics%2Citems.name_ex%2Citems.point%2Citems.external_content%2Citems.schedule%2Citems.timezone_offset%2Citems.org%2Citems.stat%2Citems.ads.options%2Citems.attribute_groups%2Crequest_type%2Csearch_attributes&stat%5Bsid%5D=91e1c495-9e55-4ca9-8712-e15073071f6e&stat%5Buser%5D=c8109e98-e546-455d-b6ed-fcfd7cb4ffe0&key=ruoedw9225&r=3862084826' #передаем id постройки в запрос
    answer = requests.get(link ,headers=headers) #делаем запрос
    return json.loads(answer.content.decode('utf-8'))# возвращаем ответ в виде json

building_id = getDataFromAddress('Арма,Нижний Сусальный переулок, 5 ст16,Басманный район, Москва')['result']['items'][0]['address']['building_id'] #получаем id постройки по данному адресу
getDataFromBuildings(building_id) #получаем json ответ с организациями в здании


# ---------------------------------------------------------------
pool = ThreadPool(32) #создаем пул, указываем количество потоков

def getFullData(address):
    addressData = getDataFromAddress(address) #получаем данные об адресе
    building_id = addressData['result']['items'][0]['address']['building_id'] #получаем id здания
    buildingData = getDataFromBuildings(building_id) #получаем данные об организациях в здании
    return buildingData, addressData #возвращаем кортеж с данными об адресе и организациях по этому адресу

addressAr = ['Арма,Нижний Сусальный переулок, 5 ст16, Басманный район, Москва', 'Щербанёва, 25, Омск'] #массив адресов
fullData = pool.map(getFullData, addressAr) #Применяем нашу функцию к массиву с адресами

#Закрываем пул
pool.close()
pool.join()