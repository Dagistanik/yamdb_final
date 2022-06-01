![example event parameter](https://github.com/github/docs/actions/workflows/main.yml/badge.svg?event=push)

## CI и CD проекта api_yamdb.

### Описание
Настроины для приложения Continuous Integration и Continuous Deployment: автоматический запуск тестов, обновление образов на Docker Hub,автоматический деплой на боевой сервер при пуше в главную ветку main.

#### Инструкция по развёртыванию
* Клонировать репозиторий и перейти в него в командной строке:

```python
git clone git@github.com:Dagistanik/yamdb_final.git
```

```python
cd yamdb_final
```


* Cоздать и активировать виртуальное окружение:
```python
python -m venv venv
```

```python
source venv/Scripts/activate
```


* Установить зависимости из файла requirements.txt

```python
python -m pip install --upgrade pip
```

```python
pip install -r requirements.txt
```

* Выполнить миграции
```
python manage.py migrate
```

* Запуск проекта

```python
python manage.py runserver
```
#### Язык

* Python 3.7

#### Стек технологий

* Python 3
* Continuous Integration
* Continuous Deployment

#### Необходимые переменные

* DOCKER_PASSWORD - пароль на Docker Hub
* DOCKER_USERNAME - логин на Docker Hub
* HOST - IP-адрес вашего сервера
* PASSPHRASE - пароль для ssh-ключа
* SSH_KEY - приватный ключ с компьютера, имеющего доступ к боевому серверу 
* TELEGRAM_TO - сохраните ID своего телеграм-аккаунта
* TELEGRAM_TOKEN - токен вашего бота
* USER - имя пользователя для подключения к серверу

#### Получение приватного ключа

* для получения приватного ключа, выполните команду в терминале:
```
cat ~/.ssh/id_rsa

```