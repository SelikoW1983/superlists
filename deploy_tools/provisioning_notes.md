Обеспечение работы нового сайта
=======================

## Необходимые пакеты:

* nginx
* Python 3.8
* virtualenv + pip
* Git

например, в Ubuntu:

    sudo add-apt-repository ppa:deadsnakes/ppa
    sudo apt update
    sudo apt install nginx git python38 python3.8-venv

## Конфигурация виртуального узла Nginx

* см nginx.template.conf
* заменить SITENAME, например, на  staging.superlists.ru

## Служба Systemd

* см. gunicorn-systemd.template.service
* заменить SITENAME, например, на  staging.superlists.ru

## Структура папок:

Если допустить, что есть учётная запись пользователя в /home/username

/home/username
└── sites
    ├── SITENAME 1
    │    ├── .env
    │    ├── db.sqlite3
    │    ├── manage.py etc
    │    ├── static
    │    └── virtualenv
    └── SITENAME 2
         ├── .env
         ├── db.sqlite3
         ├── etc
