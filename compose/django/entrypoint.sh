#!/bin/bash
set -e
cmd="$@"

# This entrypoint is used to play nicely with the current cookiecutter configuration.
# Since docker-compose relies heavily on environment variables itself for configuration, we'd have to define multiple
# environment variables just to support cookiecutter out of the box. That makes no sense, so this little entrypoint
# does all this for us.
export REDIS_URL=redis://redis:6379
export C_FORCE_ROOT=true

# the official postgres image uses 'postgres' as default user if not set explictly.
if [ -z "$LINK_DB_USER" ]; then
    export POSTGRES_USER=postgres
fi
#$POSTGRES_PASSWORD is not defined then it is empty/blank in the DB_URL

#this is because i am using alpine postgres image ... did not build it from custom docker file to set a different db like linkage
#by deafult available db is postgres
#(for alpine postgres base image postgres usr has no pass)

function postgres_ready(){
python << END
import sys
import psycopg2
try:
    #this is because i am using alpine postgres image ... did not build it from custom docker file to set a different db like linkage
    #by deafult available db is postgres
    conn = psycopg2.connect(dbname="$LINK_DB_NAME", user="$LINK_DB_USER", password="$LINK_DB_PASSWORD", host="$LINK_DB_HOST")

except psycopg2.OperationalError:
    sys.exit(-1)
sys.exit(0)
END
}

until postgres_ready; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - continuing..."
exec $cmd
