#!/usr/bin/env python

# Author  : Y.Lemiere
# Date    : 2017/10
# Contact : lemiere@lpccaen.in2p3.fr
# Object  : SuperNEMO Reconstruction manager

from datetime import date, datetime
import time
import sys
import os
import subprocess
import ConfigParser
import uuid


import sn_simu_mgr
import sn_multi_launcher

#  # # ############# Fill DB using AMI client #########
#  #    line='AddElement -project="supernemo" -processingStep="production" -entity="demo"'
#  #    line+=' -simu_id="'+prefix_simu_file+'_'+str(current_index)+'"'
#  #    line+=' -confidence_level="damned"'
#  #    line+=' -checking_status="unchecked"'
#  #    line+=' -event_generator="'+my_event+'"'
#  #    line+=' -experiment="'+experiment_name+'"'
#  #    line+=' -event_per_file="'+nb_event+'"'
#  #    line+=' -nb_of_file="'+nb_of_file+'"'
#  #    line+=' -output_path="'+CURRENT_OUTPUT_PATH+'"'
#  #    line+=' -user_comment="'+sn_user_comment+'"'
#  #    line+=' -vertex_generator="'+my_vertex+'"'
#  #    line+=' -user="'+USER+'"'
#  #    #line+=' -date="'+start_time+'"'

#  #    #     ##########client = pyAMI.client.Client('supernemo')
#  #    #     ##########client.execute(line)        

def prepare_files(arg0=None,arg1=None):

    debug = True
    function_name = "prepare_files"

    if debug:
        print ("DEBUG : *************************************")
        print ("DEBUG : [%s] : Prepare files for reconstruction purpose using (%s, %s) "%(function_name,arg0,arg1) )

    CURRENT_OUTPUT_PATH = arg0
    INPUT_FILE          = arg1

    
    snemo_cfg = ConfigParser.ConfigParser()
    snemo_cfg.read('snemo.cfg')

    log_file_name=CURRENT_OUTPUT_PATH+snemo_cfg.get('PRODUCTION_CFG','sys_rel_path')+snemo_cfg.get('PRODUCTION_CFG','log_rel_path')+"/"+"main.log"
    log_file = open(log_file_name,"a")

    try:
        os.system("cp %s %s"%(snemo_cfg.get('RECO_CFG','reconstruction_conf'),CURRENT_OUTPUT_PATH+snemo_cfg.get('PRODUCTION_CFG','config_rel_path')+snemo_cfg.get('PRODUCTION_CFG','conf_rel_path')+"/."))    
    except:
        print("\033[91mERROR\033[00m : [%s] : Can not copy reconstruction config file"%function_name)
        log_file.write("\033[91mERROR\033[00m: [%s] :  Can not copy reconstruction config file"%function_name)
        sys.exit(1)
        
    try:
        sn_multi_launcher.prepare_reco_launcher(CURRENT_OUTPUT_PATH,INPUT_FILE)
    except:
        print("\033[91mERROR\033[00m : [%s] : Can not launch properly sn_multi_launcher.py"%function_name)
        log_file.write("\033[91mERROR\033[00m: [%s] : Can not launch properly sn_multi_launcher.py"%function_name)
        sys.exit(1)
        # #end f bunch
        
    if debug:
        print("DEBUG : [%s] : shell script production done !"%function_name )
        print("DEBUG : *************************************")
    



        
        
