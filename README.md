# Проект по дисциплине "Нейроинформатика"
## АИ Панорама
## Авторы
| ФИО                          | Группа      |
| ---------------------------- | ----------- |
| Рылов Александр Дмитриевич   | М80-407Б-21 |
| Соколов Арсений Игоревич     | М80-407Б-21 |
| Марченко Алексей Эдуардович  | М80-407Б-21 |

## Презентация проекта
## Отчет
### Описание
### Бизнес цель проекта
- Описание проблемы: Отсутствие ресурса для автоматической генерации новостей, включающих текст, заголовки и изображения, приводит к длительным временным затратам и ручной работе.
- Цель: Создать автоматизированный сайт для генерации новостей с минимальным вовлечением человека.
- Целевая аудитория: Медиа-агентства, контент-креаторы, платформы для автоматической публикации новостей.
### ML-цель проекта
- Автоматизировать процесс создания качественных новостей (заголовок, текст, изображение).
- Использовать современные диффузионные модели и языковые модели для генерации контента.
- Обеспечить высокую производительность и масштабируемость для обработки запросов пользователей.
### Архитектура (схема C4)
### Обоснование архитектуры
### Объяснение выбора используемого стека
#### **FastAPI**
- Асинхронность
- Высокая производительность
- Автоматическая генерация документации
#### MongoDB
- Для проекта нужна всего одна таблица
- Меньшее потребление ресурсов по сравнению с реляционными БД
- Поддержка сложных запросов
- Поддержка асинхронной обработки
#### RabbitMQ
- Гарантированная доставка
- Маршрутизация по ключам
- Поддержка асинхронной обработки

### Описание сетей
## Конфигурация проекта
## Запуск проекта
