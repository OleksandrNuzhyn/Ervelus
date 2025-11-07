# Інструкція для розробки

## Фронтенд
- Під час розробки клієнтська частина доступна за адресою `http://localhost:5173/`
- Для pull request'ів автоматично створюється тимчасовий домен на Firebase для перегляду змін
- vite.config.js proxy на https://backend.ervelus.com

## Бекенд
Розробка ведеться на `https://backend.ervelus.com`

## Інфраструктура для розробки

### База даних
Для розробки створюється окремий екземпляр бази даних з мінімальними ресурсами та публічною IP-адресою

### Сховище (Buckets)
Замість продакшн бакетів `ervelus-storage` та `ervelus-temp` використовуються їхні аналоги для розробки (створюються нові бакети)

### Cloud Tasks
Використовуються вже існуючі черги Cloud Tasks

### Cloud Run
- Сервіс `background-worker` використовується з Cloud Run
- Запити, що в продакшні обробляються `web-worker` та `generations-worker`, під час розробки спрямовуються на `https://backend.ervelus.com`

## Процес роботи з Git
В гілку `main` дозволено зливати лише фінальний, повністю протестований код

## HTTPS клієнт
[https://valiant-hexagon-471121-i7.web.app/](https://valiant-hexagon-471121-i7.web.app/)

## Адмін-панель
[https://ervelus-web-service-281870812434.us-central1.run.app/sanekit/](https://ervelus-web-service-281870812434.us-central1.run.app/sanekit/)