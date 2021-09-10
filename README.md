# Приложение Транслятор JsonRPC API



## Общий функционал
Приложение, которое позволяет вызвать api с ипользованием пары сертификат+ключ (SSL/TLS Client Authentication)

## Основные технологии
* Python
* Django
* Docker Compose

### Ограничения
* использовал только http.client + ssl

### Запуск приложения
```
git clone https://github.com/azat715/translator
cd translator
```
в каталог ssl_store скопировать ключи client03test.crt, client03test.key
```
sudo docker-compose up --build
```

### Тесты
```
pytest tests/test_client.py
```

### Urls
* "" - список методов
* "metods/auth_check/" - метод проверки аутентификации
* "metods/test_metod" - тестовый метод с параметрами, форма запроса параметров. (всегда error)
