#!/usr/local/python/python-2.7/bin/python


# Author  : Y.Lemiere
# Date    : 2016/07
# Contact : lemiere@lpccaen.in2p3.fr
# Object  : job submitter for CCLYON

from datetime import date, datetime
import time
import sys
import os
import subprocess


execfile("sn_simu_env.py")

def qsub(arg0=None,arg1=None,arg2=None ):

    debug=True
    name=arg0
    path=arg1
    launch_filename=arg2 

    if debug:
        print("DEBUG : JOB                 : %s" % name)
        print("DEBUG : path                : %s" % path)
        print("DEBUG : launch_filename     : %s" % launch_filename)
        
    
    try:
        log_path=path+sys_rel_path+log_rel_path+"/"
        check_file=path+sys_rel_path+"launcher.d/simu_check.py"

        #        subprocess.call("qsub %s -N %s -v RUN_SIMU_PATH='%s' -e %s -o %s -m e -M lemiere@lpccaen.in2p3.fr %s -af %s" %(SUBMIT_OPTION,name,path,log_path,log_path,launch_filename,check_file), shell=True)
        subprocess.call("qsub %s -N %s -v RUN_SIMU_PATH='%s' -e %s -o %s -m e -M lemiere@lpccaen.in2p3.fr %s" %(SUBMIT_OPTION,name,path,log_path,log_path,launch_filename), shell=True)
        print("INFO : Job : %s"%launch_filename)
        print ("=============> %s started ! <============= \n" % name)
        
    except:
        print("ERROR : %s : Can not submit job using qsub at cclyon"%qsub.__name__)
        sys.exit(1)
