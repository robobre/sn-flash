#!/bin/bash

echo
echo "### SN-flash initialisation ###"
echo

INIT_BAYEUX=`bxquery --prefix 2>/dev/null`
if [ $? -ne 0 ] ; then echo "Bayeux  : [not found] -> please setup the environnement" ; exit 1 ; fi
echo "Bayeux   : $INIT_BAYEUX"

FLSIMULATE_PATH=`which flsimulate 2>/dev/null`
if [ $? -ne 0 ] ; then echo "Falaise : [not found] -> please setup the environnement" ; exit 1 ; fi
INIT_FALAISE=${FLSIMULATE_PATH/\/bin\/flsimulate/}
echo "Falaise  : $INIT_FALAISE"

INIT_SNFLASH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
echo "SN-flash : $INIT_SNFLASH"

INIT_USER=$USER
echo "user     : $INIT_USER"

echo

read -p "this configuration is fine ? " -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]] ; then echo "ok ... bye bye !"; exit 2 ; fi

echo -ne "last, please enter an email address : "
read INIT_EMAIL
echo

## replace all / by \/ to handle correctly path with 'sed' !
INIT_BAYEUX=${INIT_BAYEUX//\//\\\/}
INIT_FALAISE=${INIT_FALAISE//\//\\\/}
INIT_SNFLASH=${INIT_SNFLASH//\//\\\/}

echo "generating snemo.cfg ..."
sed "s/INIT_BAYEUX/${INIT_BAYEUX}/g;s/INIT_FALAISE/${INIT_FALAISE}/g" snemo.cfg.in > snemo.cfg

echo "generating user.cfg ..."
sed "s/INIT_SNFLASH/${INIT_SNFLASH}/g;s/INIT_USER/${INIT_USER}/g;s/INIT_EMAIL/${INIT_EMAIL}/g" user.cfg.in > user.cfg

echo
