# Tugas uts

Nama : Raja Saputera
NIM : 120140228

## how to run

1. clone this repo

```bash
git clone
```

2. change directory to this repo

```bash
cd this-project
```

3.  change development.ini url to your database url

```bash
sqlalchemy.url = mysql+pymysql://username:password@localhost:5432/dbname
```

4. install dependencies

```bash
 pip install -e .
```

5. migrate database

```bash
alembic -c development.ini upgrade head
```

6. load database

```bash
initialize_pwl_tugas4_db development.ini
```

5. run

```bash
pserve development.ini --reload
```

6. run test

```bash
pytest
```

## api routes

| Route         | Method | Description          |
| ------------- | ------ | -------------------- |
| products      | GET    | get all products     |
| products      | POST   | create product       |
| products/{id} | GET    | get product by id    |
| products/{id} | PUT    | update product by id |
| products/{id} | DELETE | delete product by id |
