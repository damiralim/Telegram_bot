import requests, re, json
from config import RapidAPI
from loguru import logger

headers = {
	"X-RapidAPI-Key": RapidAPI,
	"X-RapidAPI-Host": "hotels4.p.rapidapi.com"
}

urls = {'locations': "https://hotels4.p.rapidapi.com/locations/v2/search",
        'properties': "https://hotels4.p.rapidapi.com/properties/list",
        'photos': "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"}

def check_request(u, h, p, t):
    response = requests.get(url=u, headers=h, params=p, timeout=t)
    try:
        if response.status_code == requests.codes.ok:
            return response
        response.raise_for_status()
    except requests.exceptions.RequestException as exc:
        logger.exception(f'Вызвано исключение: {exc}')


def city_request(url, headers, params, timeout):
    response = check_request(url, headers, params, timeout)
    if response:

        if json.loads(response.text)['moresuggestions'] > 0:
            pattern = r'(?<="CITY_GROUP",).+?[\]]'
            text_response = re.findall(pattern, response.text)

            if text_response:
                suggestions = json.loads(f"{{{text_response[0]}}}")
                data = {sugg['name']: sugg['destinationId'] for sugg in suggestions['entities']}
                return data

        return f'Данный город не найден'

    return f'Прозошла ошибка'

def hotel_request(url, headers, params, timeout):
    response = check_request(url, headers, params, timeout)


