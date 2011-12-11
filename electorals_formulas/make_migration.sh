#!/bin/bash

case "$1" in
    --initial | -i) 
        rm -rf countries/migration
        rm -rf electoral/migrations
        
        python manage.py schemamigration countries --initial
        python manage.py schemamigration electoral --initial
    ;;   
    --migrate | -m)
        python manage.py migrate countries
        python manage.py migrate electoral
    ;;
    --list | -l)
        python manage.py migrate --list 
    ;;
    --shell | -s)
        python manage.py shell
    ;;
    --help | -h)
        echo ""
        echo "make-migration help information."
        echo ""
        echo "   sh make-migration.sh [option]"
        echo ""
        echo "      --initial | -i      Make initial migration scheme."
        echo "      --auto | -a |       Make migration scheme."
        echo "      --migrate | -m      Load exiting migration scheme."
        echo "      --list | -l         List all migrations schemes."
        echo "      --shell | -s        Show the django-south shell"
        echo "      --help | -h         Show this help text."
        echo ""
    ;;
    --auto | -a | *)
        python manage.py schemamigration countries --auto 
        python manage.py schemamigration electoral --auto
    ;; 
esac
