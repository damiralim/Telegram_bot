import requests, json, jmespath
from config import RapidAPI
from loguru import logger
from typing import Optional, Union, Dict, List
from requests.models import Response

''' Заголовки и urls для запросов к API '''

headers: Dict[str, str] = {
                           "X-RapidAPI-Key": RapidAPI,
                           "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
                          }

urls: Dict[str, str] = {
                        'locations': "https://hotels4.p.rapidapi.com/locations/v3/search",
                        'properties': "https://hotels4.p.rapidapi.com/properties/v2/list",
                        'photos': "https://hotels4.p.rapidapi.com/properties/v2/detail"
                       }

''' Проверка корректности запроса к API '''

def check_request(method: str, url: str, headers: dict, params: dict) -> Optional[Response]:
    if method == 'GET':
        response: Response = requests.get(url=url, params=params,
                                          headers=headers, timeout=15)
    elif method == 'POST':
        response: Response = requests.post(url=url, json=params,
                                           headers=headers, timeout=15)
    try:
        if response.status_code == requests.codes.ok:
            logger.info(f"Запрос на сервер успешно выполнен, страница обращения: {url}")
            return response
        response.raise_for_status() # вызов исключения HTTPError при некорректном ответе от API
    except requests.exceptions.RequestException as exc:
        logger.exception(f'Вызвано исключение: {exc}')

''' Запроса к API для вывода клавиатуры со списком локаций '''

def city_request(method: str, url: str, headers: dict,
                 params: dict) -> Union[Dict[str, str], str]:
    response: Response = check_request(method, url, headers, params) # функция проверки корректности запроса
    if response:

        ''' Проверка наличия значений в списке регионов '''

        if len(regions := response.json()["sr"]) > 0:
            data: Dict[str, str] = {
                                    elem['regionNames']['shortName']: elem['gaiaId']
                                    for elem in regions if 'gaiaId' in elem
                                   }
            return data

        logger.info("Нет информации в ответе от API")
        return 'К сожалению, данный город не найден. ' \
               'Пожалуйста, вернитесь к началу по команде /start'

''' Запрос к API для вывода данных по отелям(c подзапросом фотографий отелей) '''

def hotel_request(method: str, url: str, headers: dict,
                  params: dict, add_params: tuple) -> Union[Dict[str, str], float]:
    response: Response = check_request(method, url, headers, params)
    if response:
        data: List[str] = response.json()['data']['propertySearch']['properties'] # основная информация от API
        hotels = dict()

        ''' Проверка наличия значений в ответе от API.
            Извлечение из API необходимых параметров '''

        if len(data) != 0:
            for hotel in data:
                price: float = round(hotel['price']['lead']['amount'], 2)
                cost: float = round(float(price) * add_params[1], 2)
                landmark: float = hotel['destinationInfo']['distanceFromDestination']['value']
                payload: Dict[str, str, int] = {
                                                "currency": "USD", "eapid": 1, "locale": "ru_RU",
                                                "siteId": 300000001, "propertyId": hotel['id']
                                               }
                hotel_info: Response = check_request('POST', urls['photos'], headers, payload) # запрос к API
                if hotel_info:

                    ''' Получение адреса отеля '''

                    address = jmespath.search(
                                              'propertyInfo.summary.location.'
                                              'address.addressLine', hotel_info.json()['data']
                                             )

                ''' Формирование словаря с данными по каждому отелю '''

                hotels[hotel['id']] = {
                                       '\U0001F3E8 Отель': f"<b>{hotel['name']}</b>",
                                       '\U0001F4CD Адрес': f"<b>{address}</b>",
                                       '\U0001F4B2 Цена за ночь': f"<b>{price}</b>",
                                       '\U0001F4B3 Стоимость за все время пребывания': f"<b>{cost}</b>",
                                       '\U0001F6E3 Расстояние до центра': f"<b>{landmark}</b>",
                                       '\U0001F310 Страничка отеля': f"https://www.hotels.com/h{hotel['id']}.Hotel-Information"
                                      }

                ''' Получение фото отелей '''

                if add_params[0] != 0:
                    photo_data: List[str] = jmespath.search(
                                                            f'propertyInfo.propertyGallery.'
                                                            f'images[0:{add_params[0]}]',
                                                            hotel_info.json()['data']
                                                           )
                    photos: List[str] = [photo['image']['url'] for photo in photo_data]

                    ''' Проверка наличия фото к каждому отелю '''

                    hotels[hotel['id']]['Фото'] = 0 if len(photos) == 0 else photos

            ''' Сортировка отелей при выборе команды highprice '''

            if add_params[2] == 'highprice':
                hotels: Dict[str, float] = dict(sorted(hotels.items(),
                               key=lambda tup: (tup[1]['💲 Цена за ночь'],
                                                tup[1]['💳 Стоимость за все время пребывания']),
                               reverse=True))

            return hotels

        logger.info("Нет информации в ответе от API")
        return 'К сожалению, никаких отелей не найдено'

    return 'Произошла ошибка'











