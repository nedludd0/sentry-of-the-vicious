#!/bin/bash

#set -xv   # this line will enable debug

# Choose
MSGENV="In che ambiente siamo? (dev/prod ; default dev): "
MSGCHOOSE_DATA=">> With Start Data or Not? (y/n ; default y ): "

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
        WHAT="y"
    fi

    # Set envs
    if [ "$ENV" = "dev" ] ; then
    
        # Set Environment Vars 
        export PROJECT_ENV='development'
        source /home/ned/Progetti/SentryOfTheVicious/configuration_home_root/sentry_manual.conf
        
    elif [ "$ENV" = "prod" ] ; then
    
        # Set Environment Vars
        export PROJECT_ENV='production'
        source /root/sentry_app_confs/sentry_manual.conf
        
    fi
    
    # Run code
    export WITH_DATA=$WHAT
    ../venv_main_dev/bin/python3.9 sentry/database/db_init.py

    break
          
done



