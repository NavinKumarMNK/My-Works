# Bookly - Book Management App


## Migration - Alembic
- Create Setup for the Alembic migration
```bash
$ alembic init -t async migrations
```
- Create a version/migration
```bash
$ alembic revision --autogenerate -m "init"
```
- Run Migration
```bash
$ alembic upgrade head 
```