**SHELTER TELEGRAM BOT**


**ОПИСАНИЕ.**

Данный скрипт запускает Telegram bot’а под названием Shelter. Он находит отели с сайта Hotels.com, походящие под ваши условия, и выводит информацию по ним. Вы можете выбрать наилучший вариант и забронировать отель.


**УСТАНОВКА**.

Чтобы установить скрипт, необходимо клонировать репозиторий, в котором он размещен. Для этого откройте терминал Windows(нажмите Win+R и введите cmd) и введите команду git clone https://gitlab.skillbox.ru/damir_alimzhanov/python_basic_diploma.git <путь к директории>. Также эту операцию можно выполнить непосредственно в вашей IDE, например, PyCharm, открыв меню Git и выбрав Clone…
Также необходимо установить все модули, которые используются в коде бота. Для этого из терминала необходимо выполнить команду pip install -r requirements.txt.


**ИСПОЛЬЗОВАНИЕ.**

_Команды:_

lowprice - вывод самых дешевых отелей в выбранном городе 
highprice - вывод самых дорогих отелей в выбранном городе
bestdeal - вывод лучших отелей по цене и расположению от центра
history – вывод истории поиска (введенная команда[ы], дата и время ввода команды, информация по отелям)

_Необходимые данные от пользователя:_

1. Локация
2. Количество отелей для вывода (лимит – 10 отелей)
3. Необходимость загрузки фотографий для каждого (лимит – 5 шт.)
(не больше 5)
4. Даты въезда/выезда

_Дополнительные данные для команды bestdeal:_

1. Минимальная цена брони.
2. Максимальная цена брони.
3. Расстояние от отеля до центра.


**АВТОР.**

DAMIR. Сообщить о неполадках в работе бота, а также предложить улучшения можно по email: YWorker@yandex.ru.

version 1.0
