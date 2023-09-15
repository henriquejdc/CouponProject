### Coupon System RestAPI
**Abordagem:** Utilizado um projeto meu de base acrescentando a
o app e o viewset Coupon (Cupom) onde o POST /coupon/
trata-se da criação do coupom e o POST 
/coupon/use_coupon/ trata-se da utilização do cupom.

**Por que desta abordagem?**
Acredito que um cupom não seja apenas um ID inteiro,
caso fosse poderia tratar-se com o próprio POST de criação
e o PUT para sua utilização/atualização.

Entretanto, acredito que um cupom possa ser várias letras
e números, podendo em caso de ser utilizado como chave primária
prejudicar consultas e performance.
Também, deixaria exposto o cupom como chave ao ser utilizado
no navegador.


### Environment: 
```
python3 -m venv venv 
OR
virtualenv --python=python3 venv

source venv/bin/activate
```


### Requirements: 
```
pip install -r requirements.txt
```


### Database - POSTGRES (Linux): 
```
sudo -i -u postgres
psql
CREATE USER user_default WITH PASSWORD 'defaultdatabase';
ALTER USER user_default CREATEDB;
CREATE DATABASE default_database;
ALTER DATABASE default_database OWNER TO user_default;
CREATE EXTENSION pg_trgm;
```


### Migration: 
```
python manage.py migrate
```


### Collect Staticfiles: 
```
python manage.py collectstatic   
```


### Run: 
```
python manage.py runserver
```


### Create Super User / Login: 
```
python manage.py createsuperuser 

To login use email and password
```


### Docs: 
```
/docs
/docs/redoc
```


### Unit Tests: 
```
python manage.py test --failfast coupon
```

### Unit Tests Report HTML: 
```
coverage run --source='./coupon' manage.py test
coverage report

coverage html
```


### New translations:
```
python manage.py makemessages --locale pt_BR

Change to pt-br on settings:
LANGUAGE_CODE= 'pt-BT'

Obs: Necessary translate to portuguese.
```


### Create User and Access Token: 
```
Use endpoint /auth/signup/ 
Before use /auth/jwt/create/ 

Now you have your access_token and refresh_token
```


### Use Authenticate Token: 
```
Bearer {access_token}
```


### Dump seed: 
```
python manage.py dumpdata {app} --indent 4 > seed/{app}.json
```


### Load dump seed: 
```
bash migrate_and_seed.sh
```


