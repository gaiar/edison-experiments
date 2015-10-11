# edison-experiments
Небольшой эксперимент по созданию Telegram бота для взаимодействия с Intel Edison

## Основные компоненты

### Системные компоненты

* Python 2.7
* uwsgi
* nginx

### Используемые библиотеки и модули
* Flask
* mraa
* upm
* python-telegram-bot

## Установка и настройка основных компонентов

Подключаем сторонний репозиторий

```
echo "src/gz all http://repo.opkg.net/edison/repo/all" >> /etc/opkg/base-feeds.conf  && echo "src/gz edison http://repo.opkg.net/edison/repo/edison" >> /etc/opkg/base-feeds.conf  && echo "src/gz core2-32 http://repo.opkg.net/edison/repo/core2-32" >> /etc/opkg/base-feeds.conf && opkg update
```

Обновляем библиотеки

```
opkg update
opkg upgrade libmraa0 upm
```

Устанавливаем необходимое ПО

```
opkg install git openssl libgnutls-openssl27 python-pip nano mc htop python-distutils python-distutils-staticdev ntpdate
```

Выставляем корректную временную зону

```
ntpdate -v ntp.mobatime.ru
timedatectl set-timezone "Europe/Moscow"
```

Устанавливаем необходимые пакеты Python

```
pip install requests
pip install requests[security]
```

## Сборка и установка необходимых сетевых сервисов

### Собираем и устанавливаем библиотеку libpcre

```
wget ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre/pcre-8.37.tar.gz
tar xvf pcre-8.37.tar.gz
cd pcre-8.37
./configure --enable-utf --enable-unicode-properties --enable-jit
make -j2
make install
```

### Устанавливаем и настраиваем uwsgi

#### Устанавливаем uwsgi
```
pip install uwsgi
```

#### systemd скрипт для запуска uwsgi

Лежит в /lib/systemd/system/uwsgi.service

```
[Unit]
Description=uWSGI Emperor
After=syslog.target

[Service]
Environment=statedir=/var/run/uwsgi
ExecStartPre=/bin/mkdir -p ${statedir}
ExecStart=/usr/bin/uwsgi --ini /etc/uwsgi/emperor.ini
Restart=always
KillSignal=SIGQUIT
Type=notify
StandardError=syslog
NotifyAccess=all

[Install]
WantedBy=multi-user.target
```

#### Образец настройки uwsgi и emperor

**uwsgi.ini**

Лежит в /etc/uwsgi/sites-available

```
[uwsgi]
socket = /var/run/uwsgi/iotbot.ru.sock
pidfile=/var/run/uwsgi/iotbot.pid
pcre-jit = on
chmod-socket=666
wsgi-file = /home/Developer/edison-experiments/app.py
chdir = /home/Developer/edison-experiments/
callable = app
master = true
home = /home/Developer/edison-experiments/edison
; www-data uid/gid
;uid = 1
;gid = 1
harakiri = 20
harakiri-verbose = true
die-on-term = true
processes = 4
threads = 2
logger = file://var/log/uwsgi/iotbot.ru.log
req-logger = file://var/log/uwsgi/iotbot.ru_full.log
```

**emperor.ini**
Лежит в /etc/uwsgi/
```
[uwsgi]
emperor = /etc/uwsgi/sites-enabled
```

### Устанавливаем и настраиваем nginx

#### Собираем и настраиваем nginx

```
wget http://nginx.org/download/nginx-1.9.5.tar.gz
tar xvf nginx-1.9.5.tar.gz
cd nginx-1.9.5
./configure --with-http_ssl_module --with-pcre-jit --with-ipv6 --with-pcre-jit --with-http_gzip_static_module --with-http_ssl_module --with-ipv6  --with-http_stub_status_module
make -j2
make install
```

#### systemd скрипт для запуска nginx

```
nano /lib/systemd/system/nginx.service
```
вставить следующее содержимое

```
[Unit]
Description=The NGINX HTTP and reverse proxy server
After=syslog.target network.target remote-fs.target nss-lookup.target

[Service]
Type=forking
PIDFile=/usr/local/nginx/logs/nginx.pid
ExecStartPre=/usr/local/nginx/sbin/nginx -t
ExecStart=/usr/local/nginx/sbin/nginx
ExecReload=/bin/kill -s HUP $MAINPID
ExecStop=/bin/kill -s QUIT $MAINPID
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

#### Образец настройки nginx 

```
upstream flask_serv {
    server unix:/var/run/uwsgi/iotbot.ru.sock;
}


map $http_upgrade $connection_upgrade {
    default upgrade;
    ''      close;
}

server {
       listen         80;
       server_name    *.iotbot.ru;
       return         301 https://$server_name$request_uri;
	   
	   access_log  /var/log/nginx/iotbot_access.log;
	   error_log  /var/log/nginx/iotbot_error.log;
}

server {
        listen         443 ssl;
        server_name    *.iotbot.ru;
		
		access_log  /var/log/nginx/iotbot_access.log;
		error_log  /var/log/nginx/iotbot_error.log;

        ssl_certificate /etc/ssl/nginx/iotbot.ru.crt;
        ssl_certificate_key /etc/ssl/nginx/iotbot.ru.key;
        ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
        ssl_ciphers 'EECDH+AESGCM:EDH+AESGCM:AES256+EECDH:AES256+EDH';
		


        location / {
		    uwsgi_pass flask_serv;
			include uwsgi_params;
            if ($uri != '/') {
                expires 30d;
            }
        }
}
```


#### Убираем стандартный web сервер edison с 80го порта

В файле /usr/lib/edison_config_tools/edison-config-server.js ищем строчку 
```
http.createServer(requestHandler).listen(80);
```
изменяем порт 80 на любой, например, 8080


