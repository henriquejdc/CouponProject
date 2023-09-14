### Coupon System RestAPI

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

### Envoriment: 
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

### New translations:
```
python manage.py makemessages --locale pt_BR

Change to pt-br on settings:
LANGUAGE_CODE= 'pt-BT'

Obs: Não traduzi - Poderia se usar o Poedit. Deixei assim para futuras traduções.
```

### Run: 
```
python manage.py runserver
```


### Unit Tests: 
```
python manage.py test --failfast
```


### Unit Tests Report: 
Relatório de cobertura do app feito para o teste
```
coverage run --source='./coupon' manage.py test
coverage report

coverage html
```
Isso criará uma pasta chamada htmlcov com o html dos arquivos.

### Dump seed: 
```
python manage.py dumpdata {app} --indent 4 > seed/{app}.json
```

### Load dump seed: 
```
bash migrate_and_seed.sh
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



