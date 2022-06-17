#!/bin/zsh

echo 'drop table `order`; drop table `order_detail`;' | sqlite3 db_homework.db
echo 'from ordering import db; db.create_all()' | python3