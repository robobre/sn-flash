#!/usr/local/python/python-2.7/bin/python


# Author  : Y.Lemiere
# Date    : 2016/07
# Contact : lemiere@lpccaen.in2p3.fr
# Object  : SuperNEMO Simulation manager

import os

############### User env
MAIL_TO="lemiere@lpccaen.in2p3.fr"


############### Simulation env

USER=os.environ['USER']
MAIN=os.environ['HOME']
MAIN_PATH="/sps/nemo/scratch/ylemiere/beyond_flsimulate"
#MAIN+"/script/SuperNEMO/sn_simulation/"
SIMU_DB=MAIN_PATH+"simu.db"

## SW PATH ##
BX_INSTALL_PATH="/sps/nemo/sw/simulation/install_brew/cadfaelbrew/bin"
#"/sps/nemo/sw/simulation/Bayeux/Binary/Bayeux-3.0-git/Install/bin"

#"/sps/nemo/sw/simulation/cadfaelbrew.git/bin"
#"/sps/nemo/sw/simulation/Bayeux/Binary/Install/bin"
SW_BASE_PATH="/sps/nemo/scratch/ylemiere/soft_simu/Falaise/Install"
SW_PATH=SW_BASE_PATH+"/bin/"

## BLESSED URN ##
urn_blessed_snemo="urn:snemo:demonstrator:simulation:2.1"


##  SW name ##
sw_snemo_simulation="flsimulate"
sw_snemo_configuration="flsimulate-configure"
bx_seeds="bxg4_seeds"
bxvariant_inspector="bxvariant_inspector"


############# Output env

MAIN_SIMU_PATH="/sps/nemo/scratch/simu"
HPSS_USER_PATH="/hpss/in2p3.fr/group/nemo/users/"+USER+"/"
HPSS_BLESSED_PATH="/hpss/in2p3.fr/group/nemo/SuperNEMO/simulation/production"

config_rel_path="/config.d"
seed_rel_path="/seeds.d"
variant_rel_path="/variant.d"
conf_rel_path="/conf.d"

sys_rel_path="/.sys"
log_rel_path="/log.d"
launcher_rel_path="/launcher.d"

output_rel_path="/output_files.d"



############ PyAMI env

PROJECT_NAME="supernemo"
PROCESSING_NAME="production"
ENTITY_NAME="demo"

############ Batch system env
#SUBMIT_OPTION=" -V -P P_nemo -l sps=1 -r y -l h_cpu=72:00:00 -l s_cpu=71:20:00 -l h_rt=72:00:00 -l h_rss=8G -l h_fsize=40G"
SUBMIT_OPTION="-P P_nemo -l sps=1 -l hpss=1 -r y -V"

JOB_CHECKER="/simu_check.py"


def check_path():
    print ("Enter in check path function : ")
    print ("-------------------------------")
   
    single_check(MAIN_PATH)
    single_check(SIMU_DB)
    single_check(SW_PATH)
    single_check(SW_BASE_PATH)
    single_check(SW_PATH+sw_file)
    single_check(CONFIG_PATH)
    print ("-------------------------------")

def single_check(a_path):
    if os.path.exists(a_path):
        print ("INFO  : Existing path  : %s " % a_path)
    else:
        print ("ERROR : %s is missing" %  a_path)

