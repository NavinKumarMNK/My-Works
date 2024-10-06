# Bookly - Book Management App


## Sample .env Config
```env
JWT_SECRET_KEY=your_secret_key_here
JWT_MAXAGE=60
JWT_ALGORITHM=HS256

POSTGRES_USER=postgres
POSTGRES_DB=bookly
POSTGRES_PASSWORD=postgres

DATABASE_URL=postgresql+asyncpg://postgres:postgres@postgres:5432/bookly
```


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
- Revert Last Migration 
```bash
$ alembic downgrade -1 
```