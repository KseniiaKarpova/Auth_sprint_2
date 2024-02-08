set -e

# Run the PostgreSQL entrypoint script
/usr/local/bin/docker-entrypoint.sh "$@"
echo "ALTER ROLE $POSTGRES_USER SET search_path = content, public;" | psql -U "$POSTGRES_USER" -d "$POSTGRES_DB"