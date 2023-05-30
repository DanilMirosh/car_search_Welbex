# **Тестовое задание web-программист Python** (Middle)

### #API: Сервис поиска ближайших машин для перевозки грузов.

<aside>
🔥 Необходимо разработать REST API сервиc для поиска ближайших машин к грузам.

</aside>

◼Стек и требования:

- **Python** (Django Rest Framework / FastAPI) на выбор.
- **DB** - Стандартный PostgreSQL.
- Приложение должно запускаться в docker-compose без дополнительных доработок.
- Порт - 8000.
- БД по умолчанию должна быть заполнена 20 машинами.
- Груз обязательно должен содержать следующие характеристики:
    - локация pick-up;
    - локация delivery;
    - вес (1-1000);
    - описание.
- Машина обязательно должна в себя включать следующие характеристики:
    - уникальный номер (цифра от 1000 до 9999 + случайная заглавная буква английского алфавита в конце, пример: "1234A", "2534B", "9999Z")
    - текущая локация;
    - грузоподъемность (1-1000).
- Локация должна содержать в себе следующие характеристики:
    - город;
    - штат;
    - почтовый индекс (zip);
    - широта;
    - долгота.

> *Список уникальных локаций представлен в прикрепленном csv файле "uszips.csv".*
>
>
> [uszips.csv](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/73ce520f-5205-47d4-8169-2266c628f6a7/uszips.csv)
>
> *Необходимо осуществить выгрузку списка в базу данных Postgres при запуске приложения.*
>
- При создании машин по умолчанию локация каждой машины заполняется случайным образом;
- Расчет и отображение расстояния осуществляется в милях;
- Расчет расстояния должен осуществляться с помощью библиотеки geopy. help(geopy.distance). Маршруты не учитывать, использовать расстояние от точки до точки.

<aside>
⭐ Задание разделено на 2 уровня сложности. Дедлайн по времени выполнения зависит от того, сколько уровней вы планируете выполнить.
**1 уровень** - 3 рабочих дня.
**2 уровень** - 4 рабочих дня.

</aside>

### ◼Уровень 1

Сервис должен поддерживать следующие базовые функции:

- Создание нового груза (характеристики локаций pick-up, delivery определяются по введенному zip-коду);
- Получение списка грузов (локации pick-up, delivery, количество ближайших машин до груза ( =< 450 миль));
- Получение информации о конкретном грузе по ID (локации pick-up, delivery, вес, описание, список номеров ВСЕХ машин с расстоянием до выбранного груза);
- Редактирование машины по ID (локация (определяется по введенному zip-коду));
- Редактирование груза по ID (вес, описание);
- Удаление груза по ID.

### ◼Уровень 2

Все что в уровне 1 + дополнительные функции:

- Фильтр списка грузов (вес, мили ближайших машин до грузов);
- Автоматическое обновление локаций всех машин раз в 3 минуты (локация меняется на другую случайную).

### ◼**Критерии оценки:**

- Адекватность архитектуры приложения;
- Оптимизация работы приложения.
-
# Технологии
- Python
- Django
- Postgres
- Docker

Обратите внимание, что в данном примере не реализованы обработка ошибок и валидация данных.
В реальном проекте рекомендуется добавить дополнительную обработку ошибок и проверку данных,
а также реализовать механизм аутентификации и авторизации для защиты эндпоинтов, и конечно же тесты

Запуск проекта
Склонируйте репозиторий

Запустите docker-compose docker-compose up --build

При Get-запросе http://127.0.0.1:8000/api/locations просмотр Локаций
ответ в формате
```json
HTTP 200 OK
Allow: GET, POST, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "count": 33788,
    "next": "http://127.0.0.1:8000/api/locations/?limit=10&offset=10",
    "previous": null,
    "results": [
        {
            "city": "Adjuntas",
            "state": "Puerto Rico",
            "zip_code": "00601",
            "latitude": "18.180270",
            "longitude": "-66.752660"
        },
        {
            "city": "Aguada",
            "state": "Puerto Rico",
            "zip_code": "00602",
            "latitude": "18.360750",
            "longitude": "-67.175410"
        }   ...
```
При Get-запросе http://127.0.0.1:8000/api/cars/ просмотр авто
ответ в формате
```json
HTTP 200 OK
Allow: GET, POST, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "count": 40,
    "next": "http://127.0.0.1:8000/api/cars/?limit=10&offset=10",
    "previous": null,
    "results": [
        {
            "id": 3,
            "unique_number": "3101G",
            "capacity": 943,
            "latitude": "49.517274",
            "longitude": "-148.638274"
        },
        {
            "id": 4,
            "unique_number": "6020I",
            "capacity": 554,
            "latitude": "-12.465218",
            "longitude": "-34.391958"
        },
```
При GET-запросе http://127.0.0.1:8000/api/cars/3/ просмотр конкретного авто
ответ в формате
```json
HTTP 200 OK
Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "id": 3,
    "unique_number": "3101G",
    "capacity": 943,
    "latitude": "49.517274",
    "longitude": "-148.638274"
}
```
При PUT-запросе http://127.0.0.1:8000/api/cars/3/ можно изменить данные конкретного авто

При GET-запросе http://127.0.0.1:8000/api/cargos/ просмотр груза
ответ в формате
```json
HTTP 200 OK
Allow: GET, POST, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "count": 6,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "pick_up_location": {
                "city": "Arecibo",
                "state": "Puerto Rico",
                "zip_code": "00612",
                "latitude": "18.412830",
                "longitude": "-66.705100"
            },
            "delivery_location": {
                "city": "Bajadero",
                "state": "Puerto Rico",
                "zip_code": "00616",
                "latitude": "18.418780",
                "longitude": "-66.667900"
            },
            "weight": 500,
            "description": "test",
            "cars": []
        },   ....
```
При POST-запросе http://127.0.0.1:8000/api/cargos/ создание груза
пример тела запроса
```json
{
    "pick_up_location": {
        "city": "Adjuntas",
        "state": "Puerto Rico",
        "zip_code": "00601",
        "latitude": "18.180270",
        "longitude": "-66.752660"
    },
    "delivery_location": {
        "city": "Aguada",
        "state": "Puerto Rico",
        "zip_code": "00602",
        "latitude": "18.360750",
        "longitude": "-67.175410"
    },
    "weight": 500,
    "description": "test"
}
```
При GET-запросе http://127.0.0.1:8000/api/cargos/1/ просмотр конкретного груза
ответ в формате
```json
HTTP 200 OK
Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "id": 1,
    "pick_up_location": {
        "city": "Arecibo",
        "state": "Puerto Rico",
        "zip_code": "00612",
        "latitude": "18.412830",
        "longitude": "-66.705100"
    },
    "delivery_location": {
        "city": "Bajadero",
        "state": "Puerto Rico",
        "zip_code": "00616",
        "latitude": "18.418780",
        "longitude": "-66.667900"
    },
    "weight": 500,
    "description": "test",
    "cars": []
}
```
При POST-запросе http://127.0.0.1:8000/api/cargos/1/ можно изменять значения груза
