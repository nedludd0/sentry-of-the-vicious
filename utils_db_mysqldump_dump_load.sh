#!/bin/bash  

#set -xv   # this line will enable debug

# Welcome
printf "\n"
printf "####################################################\n"
printf "## Script per DB Dump o Load All or Tg Users Conf ##\n"
printf "####################################################\n"

# Prompt
MSGENV="In che ambiente siamo? (dev/prod): "
MSGWHAT="Lavorare su Tutto, solo sulle User Confs o solo sulle Catalogs? (All 1 / User Conf 2 /  Catalogs 3 ): "
MSGCHOOSE_DL="Dump Data, Dump DDL o Load Sql Data? (d/c/l): "
MSGFILESQL="Scegli il nome del file da importare: "

# Variabili
DATA=`date '+%Y%m%d.%H%M'`

TABLES_USER_CONF='tg_users tg_users_config app_traders app_users'

TABLES_CATALOG_GENERAL='app_tg_msgs_catalog app_users_logs_catalog app_terms_condition_use tg_msgs_logs_catalog tg_users_logs_catalog'
TABLES_CATALOG_TRADE='trade_exchanges trade_exchanges_wallet trade_orders_type tg_users_trade_logs_catalog'
TABLES_CATALOGS=$TABLES_CATALOG_GENERAL" "$TABLES_CATALOG_TRADE

OPTZ_SQL_DUMP_DATA='--lock-tables --complete-insert --extended-insert=FALSE --no-create-info'
OPTZ_SQL_DUMP_DDL='--no-data --compact'
OPTZ_GREP_V='^\/\*![0-4][0-9]\{4\}.*\/;$' # per pulire ulteriormente il dump ddl --> tolgo righe come questa /*!40101 SET character_set_client = utf8 */;

while true; do

    # PROMPT DEI VALORI
    echo ""
    read -p "$MSGENV" ENV 
    read -p "$MSGWHAT" WHAT
    
    # CHECK SE È STATO INDICATO L'AMBIENTE - ENV
    if [[ -z "$ENV" ]] ; then
        echo ""
        echo "ERRORE: specificare l'ambiente --> "$MSGENV
        echo ""
        exit
    fi

    # CHECK SE È STATO INDICATO COSA - WHAT
    if [[ -z "$WHAT" ]] ; then
        echo ""
        echo "ERRORE: specificare oggetti del db --> "$MSGWHAT
        echo ""
        exit
    fi

    # LOAD ENVIRONMENT VARS
    if [ "$ENV" = "dev" ] ; then
        source ../../../configuration_home_root/mymoney_manual.conf
        DB_SCHEMA=$DB_SCHEMA_DEV
        DB_USER=$DB_USER_DEV
        DB_PASSWORD=$DB_PASSWORD_DEV        
    elif [ "$ENV" = "prod" ] ; then
        source /root/mymoney_app_confs/mymoney_manual.conf
        DB_SCHEMA=$DB_SCHEMA_PROD
        DB_USER=$DB_USER_PROD
        DB_PASSWORD=$DB_PASSWORD_PROD
    fi
    break
    
done


while true; do

    # PROMPT DEI VALORI
    echo ""
    read -p "$MSGCHOOSE_DL" ACTION

    # CHECK SE STATO INDICATO COSA - ACTION
    if [[ -z "$ACTION" ]] ; then
        echo ""
        echo "ERRORE: specificare l'azione --> "$MSGCHOOSE_DL
        echo ""
        exit
    fi  
    
    case $ACTION in
        d)
          if [[ "$WHAT" = "1" ]] ; then
                mysqldump --user=$DB_USER --password=$DB_PASSWORD --host=$DB_HOST --port=$DB_PORT $OPTZ_SQL_DUMP_DATA $DB_SCHEMA > "DB.dump."$DATA.$DB_SCHEMA."all".sql
          elif [[ "$WHAT" = "2" ]] ; then
                mysqldump --user=$DB_USER --password=$DB_PASSWORD --host=$DB_HOST --port=$DB_PORT $OPTZ_SQL_DUMP_DATA $DB_SCHEMA --tables $TABLES_USER_CONF > "DB.dump."$DATA.$DB_SCHEMA."users_conf".sql
          elif [[ "$WHAT" = "3" ]] ; then
                mysqldump --user=$DB_USER --password=$DB_PASSWORD --host=$DB_HOST --port=$DB_PORT $OPTZ_SQL_DUMP_DATA $DB_SCHEMA --tables $TABLES_CATALOGS > "DB.dump."$DATA.$DB_SCHEMA."catalogs".sql
          fi
          break
          ;;
        c)
          if [[ "$WHAT" = "1" ]] ; then
                mysqldump --user=$DB_USER --password=$DB_PASSWORD --host=$DB_HOST --port=$DB_PORT $OPTZ_SQL_DUMP_DDL $DB_SCHEMA | grep -v $OPTZ_GREP_V > "DB.dump."$DATA.$DB_SCHEMA."all.only.ddl".sql
          elif [[ "$WHAT" = "2" ]] ; then
                mysqldump --user=$DB_USER --password=$DB_PASSWORD --host=$DB_HOST --port=$DB_PORT $OPTZ_SQL_DUMP_DDL $DB_SCHEMA $TABLES_USER_CONF | grep -v $OPTZ_GREP_V > "DB.dump."$DATA.$DB_SCHEMA."users_conf.only.ddl".sql
          elif [[ "$WHAT" = "3" ]] ; then
                mysqldump --user=$DB_USER --password=$DB_PASSWORD --host=$DB_HOST --port=$DB_PORT $OPTZ_SQL_DUMP_DDL $DB_SCHEMA $TABLES_CATALOGS | grep -v $OPTZ_GREP_V > "DB.dump."$DATA.$DB_SCHEMA."catalogs.only.ddl".sql
          fi
          break
          ;;
        l)
          echo ""
          read -p "$MSGFILESQL" FILESQL  
          if [[ -z "$FILESQL" ]] ; then
            echo ""
            echo "ERRORE: specificare il file --> "$MSGFILESQL
            echo ""
            exit
          fi
          mysql --user=$DB_USER --password=$DB_PASSWORD --host=$DB_HOST --port=$DB_PORT $DB_SCHEMA < $FILESQL
          break
          ;;
    esac
done
