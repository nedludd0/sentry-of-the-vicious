#!/bin/bash

#set -xv   # this line will enable debug

# Choose
MSGENV="In che ambiente siamo? (dev/prod ; default dev): "
MSGCHOOSE_DATA=">> Start with Bjoer WSGI Server or with Flask WSGI Server? (f/b ; default f): "

while true; do

    # Nome Ambiente 
    echo ""
    read -p "$MSGENV" ENV
    read -p "$MSGCHOOSE_DATA" WHAT
    
    # se non sono stati messi gli inputs
    if [[ -z "$ENV" ]] ; then
        ENV="dev"
    fi
    if [[ -z "$WHAT" ]] ; then
        WHAT="f"
    fi
    
    if [ "$ENV" = "dev" ] ; then
    
        # Set Environment Vars 
        export PROJECT_ENV='development'
        source ../../../configuration_home_root/mymoney_manual.conf
        
        if [ "$WHAT" = "b" ] ; then
            # Run Project from virtualenv
            ../venv_main_dev/bin/python3.8 -m mymoney
        elif [ "$WHAT" = "f" ] ; then
            # Set generic FLASK_APP
            export FLASK_APP=mymoney.__main__
            # Run Project Flask from virtualenv
            ../venv_main_dev/bin/flask run --host=0.0.0.0 --port=5000
        fi        
        
    elif [ "$ENV" = "prod" ] ; then
    
        # Set Environment Vars
        export PROJECT_ENV='production'
        source /root/mymoney_app_confs/mymoney_manual.conf
        
        if [ "$WHAT" = "b" ] ; then
            # Run Project from virtualenv
            ../venv_main_prod/bin/python3.8 -m mymoney
        elif [ "$WHAT" = "f" ] ; then
            # Set generic FLASK_APP
            export FLASK_APP=mymoney.__main__
            # Run Project Flask from virtualenv
            ../venv_main_prod/bin/flask run --host=0.0.0.0 --port=5000
        fi        
        
        
    fi
    
    break
          
done
