#!/bin/bash

#set -xv   # this line will enable debug

# Choose
MSGENV="In che ambiente siamo? (dev/prod ; default dev): "

while true; do

    # Nome Ambiente 
    echo ""
    read -p "$MSGENV" ENV
    
    # se non sono stati messi gli inputs
    if [[ -z "$ENV" ]] ; then
        ENV="dev"
    fi
    
    if [ "$ENV" = "dev" ] ; then
    
        # Set Environment Vars 
        export PROJECT_ENV='development'
        source /home/ned/Progetti/SentryOfTheVicious/configuration_home_root/sentry_manual.conf
        
        # Run Project from virtualenv
        ../venv_main_dev/bin/python3.9 -m sentry
        
    elif [ "$ENV" = "prod" ] ; then
    
        # Set Environment Vars
        export PROJECT_ENV='production'
        source /root/sentry_app_confs/sentry_manual.conf
        
        # Run Project from virtualenv
        ../venv_main_prod/bin/python3.9 -m sentry

    fi
    
    break
          
done
