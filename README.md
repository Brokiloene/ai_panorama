## <img src="./docs/logo.png" width="32"> АИ Панорама 
![](./docs/site-preview.png)
![](./docs/generate-article-menu.png)
### Вид на мобильных устройствах
![](./docs/site-preview-mobile.png)

## Создатели
|                              |                  |
| ---------------------------- | ---------------- |
| Brokiloene                   | Frontend/Backend |
| valerasaray                  | Design/AI        |
| MarchAleksey                 | AI               |

## Стек
|||
|-|-|
|**Backend**| Unicorn, Fastapi, Minio, RabbitMQ, MongoDB, Jinja|
|**Frontend**| HTML, CSS, JS|

## Архитектура (схема C4)
![](./docs/architecture.png)
> Одна точка входа для пользователя  
> Легко подключить дополнительные нейронки (всего в проекте их 3 типа) -- достаточно указать IP и порт RabbitMQ  
> Маршрутизация по Routing Keys RabbitMQ – backend взаимодействует с одной очередью, извлекая из неё нужные данные  

## Запуск проекта
Переименовать файл `sample.env` в `.env`  
Добавить свои сертификаты в папку `/certs`  
Запустить проект через `docker compose up`  
