#!/bin/sh
set -e  # exit if anything fails

# user creation if not exists
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "postgres" -q <<-EOSQL
    DO \$\$
    BEGIN
        IF NOT EXISTS (SELECT FROM pg_catalog.pg_user WHERE usename = '$POSTGRES_USER') THEN
            CREATE ROLE $POSTGRES_USER WITH LOGIN PASSWORD '$POSTGRES_PASSWORD';
        END IF;
    END
    \$\$;
EOSQL

# database creation if not exists
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "postgres" -tAc "SELECT 1 FROM pg_database WHERE datname = '$POSTGRES_DB'" | grep -q 1 || psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "postgres" -qc "CREATE DATABASE $POSTGRES_DB"
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "postgres" -q <<-EOSQL
    GRANT ALL PRIVILEGES ON DATABASE $POSTGRES_DB TO $POSTGRES_USER;
EOSQL

# Appendix
# -v ON_ERROR_STOP=1 -> stops executing if an error occurs
# <<- EOSQL -> starts a here-document, allowing multiple lines of SQL
# DO \$\$ -> anonymous code block
# -tAc -> Combines Tuples only (no columns) , no alignment, executes a single command
# | grep -q 1 -> sliently check if the output contains 1
# || if the grep fails, execute the command afterwards%
