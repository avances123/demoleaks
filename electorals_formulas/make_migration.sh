#!/bin/bash

case "$1" in
    --initial | -i) 
        rm -rf migration
        mkdir migration
    
        python manage.py schemamigration migration --initial
        python manage.py migrate migration
    ;;   
    --migrate | -m)
        python manage.py schemamigration migration --auto
        python manage.py migrate migration --auto
    ;;
    --list | -l)
        python manage.py migrate --list        
    ;;
    --shell | -s)
        python manage.py shell

    ;;
    *)
        echo ""
        echo "make-migration help information."
        echo ""
        echo "   sh make-migration.sh [option]"
        echo ""
        echo "      --initial | -i      Create initial migration structure."
        echo "      --migrate | -m      Update exiting migration."
        echo "      --list | -l         List all migrations."
        echo "      --shell | -s        Show the django-south shell"
        echo ""
    ;; 
esac
