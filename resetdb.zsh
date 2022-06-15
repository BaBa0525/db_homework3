#!/bin/zsh

echo "WARNING: Your database will be cleared"
read "response?Do you want to continue? [y/N] "
if [[ $response =~ ^(YES|Y|yes|y)$ ]]; then
    cd backend
    echo "from ordering import db\ndb.drop_all()\ndb.create_all()" | python
    cd -
else
    echo
fi

