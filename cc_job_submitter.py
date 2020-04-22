
#!/usr/bin/env python



# Author  : Y.Lemiere
# Date    : 2016/07
# Contact : lemiere@lpccaen.in2p3.fr
# Object  : job submitter for CCLYON

from datetime import date, datetime
import time
import sys
import os
import subprocess

## import configparser as ConfigParser
#import ConfigParser


try:
    # Python 2 only:
    import ConfigParser as ConfigParser
except ImportError:
    # Python 2 and 3 (after ``pip install configparser``)
    import configparser as ConfigParser


##execfile("sn_simu_env.py")

def qsub(arg0=None,arg1=None,arg2=None):

    debug=True
    name=arg0
    path=arg1
    launch_filename=arg2 


    
    snemo_cfg = ConfigParser.ConfigParser()
    snemo_cfg.read('snemo.cfg')
    
    usr_cfg = ConfigParser.ConfigParser()
    usr_cfg.read('user.cfg')
    
    if debug:
        print("DEBUG : [%s] : JOB                 : %s" %(qsub.__name__,name))
        print("DEBUG : [%s] : path                : %s" %(qsub.__name__,path))
        print("DEBUG : [%s] : launch_filename     : %s" %(qsub.__name__,launch_filename))
        
    
    try:
        log_path=path+snemo_cfg.get('PRODUCTION_CFG','sys_rel_path')+snemo_cfg.get('PRODUCTION_CFG','log_rel_path')+"/"
        log_file_name=log_path+"/main"+".log"
        log_file = open(log_file_name,"a")


        check_file=path+snemo_cfg.get('PRODUCTION_CFG','sys_rel_path')+snemo_cfg.get('PRODUCTION_CFG','launcher_rel_path')+"/simu_check.py"

        log_file.write("INFO : [%s] : Job submission \n"%qsub.__name__)
        log_file.write("COMMAND : [%s] : qsub %s -N %s -v WORKING_PATH='%s' -e %s -o %s -m e -M %s %s\n" %(qsub.__name__,snemo_cfg.get('BATCH_CFG','submit_option'),name,path,log_path,log_path,usr_cfg.get('USER_CFG','mail_to'),launch_filename))


        subprocess.call("qsub %s -N %s -v WORKING_PATH='%s' -v SW_PATH='%s' -e %s -o %s -m e -M %s %s" %(snemo_cfg.get('BATCH_CFG','submit_option'),name,path,snemo_cfg.get('SW_CFG','sw_path'),log_path,log_path,usr_cfg.get('USER_CFG','mail_to'),launch_filename), shell=True)


        print("INFO : Job : %s"%launch_filename)
        print ("\033[92=============> %s started ! <============= \033[00m\n" % name)
        
        log_file.close()




    except:
        print("\033[91mERROR\033[00m : [%s] : Can not submit job using qsub at cclyon"%qsub.__name__)
        sys.exit(1)
