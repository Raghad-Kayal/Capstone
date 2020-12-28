#!/bin/sh
export AUTH0_DOMAIN='fsndcoffeshop.us.auth0.com'
export ALGORITHMS='RS256'
export API_AUDIENCE='app'

export DATABASE_URL="postgres://postgres:111@127.0.0.1:5432/hospital"
export FLASK_APP=flaskr
export FLASK_DEBUG=True
export FLASK_ENVIRONMENT=debug