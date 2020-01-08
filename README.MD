# Python django RealTime notifications

## Installation guide
#### 1. Install `docker-ce`
```
$ sudo apt install apt-transport-https ca-certificates curl software-properties-common
$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
$ sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic stable"
$ sudo apt update
$ apt-cache policy docker-ce
$ sudo apt install docker-ce
$ sudo usermod -aG docker ${USER}
$ su - ${USER}
$ docker login
```

#### 2. Install `docker-compose`
```
$ sudo apt install python
$ sudo apt install python-pip
$ sudo pip install docker-compose
```

#### 3 Clone GitLab repository.
```
$ git clone <ssh for repo>
```

#### 4 Pull the latest Docker image from repository and start Docker containers
```
$ docker-compose pull
$ docker-compose build
$ docker-compose up -d
```

#### 5 Create tables and superuser in both django apps
```
$ docker exec -it <django-producing> bash
$ docker exec -it <django_admin> bash
$ python manage.py createsuperuser
$ python manage.py migrate
```

#### 6 Enable RabbitMQ Management Plugins
```
$ docker exec -it <rabbitmq-container> bash
$ rabbitmq-plugins enable rabbitmq_management
```
## Usage guide
#### Now you can use the following urls:
1. <http://localhost> Main page
2. <http://localhost:8080/admin> Admin page 
3. <http://localhost:15672/> RabbitMQ dashboard
4. <http://localhost:8888/> Celery Flower dashboard