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


    if [ "$ENV" = "dev" ] ; then
    
        # Set Environment Vars 
        export PROJECT_ENV='development'
        source ../../../configuration_home_root/mymoney_manual.conf
        
        if [ "$WHAT" = "y" ] ; then
            # Set generic FLASK_APP
            export FLASK_APP=mymoney.__main__        
            # Run Flask from virtualenv
            ../venv_main_dev/bin/flask init-db
        elif [ "$WHAT" = "n" ] ; then
            # Set generic FLASK_APP
            export FLASK_APP=followstrategy.__main__        
            # Run Flask from virtualenv
            ../venv_main_dev/bin/flask init-db-nodata
        fi        
        
    elif [ "$ENV" = "prod" ] ; then
    
        # Set Environment Vars
        export PROJECT_ENV='production'         
        source /root/mymoney_app_confs/mymoney_manual.conf
        
        if [ "$WHAT" = "y" ] ; then
            # Set generic FLASK_APP
            export FLASK_APP=mymoney.__main__        
            # Run Flask from virtualenv
            ../venv_main_prod/bin/flask init-db
        elif [ "$WHAT" = "n" ] ; then
            # Run Flask from virtualenv
            ../venv_main_prod/bin/flask init-db-nodata
        fi
                
    fi

    break
          
done



