#!/usr/local/python/python-2.7/bin/python


# Author  : Y.Lemiere
# Date    : 2017/10
# Contact : lemiere@lpccaen.in2p3.fr
# Object  : SuperNEMO Simulation manager

from datetime import date, datetime
import time
import sys
import os
import fnmatch
import subprocess
import pipes
import uuid
import tarfile
#import configparser as ConfigParser ## for python 3
import ConfigParser
###  AMI
# import pyAMI.client
# import pyAMI_supernemo


import sn_multi_launcher

def prepare_files(arg0=None,arg1=None,arg2=None,arg3=None,arg4=None,arg5=None, arg6=None):

     
    snemo_cfg = ConfigParser.ConfigParser()
    snemo_cfg.read('snemo.cfg')

    
    debug    = True
    gui_mode = True
    prepare_simu_start_time= datetime.now()
    function_name="prepare_files"
    
    if debug:
        print("DEBUG : *************************************")
        print ("INFO : [%s] : Prepare files for simulation purpose using (%s, %s, %s, %s, %s) "%(function_name,arg0,arg1,arg2,arg3,arg4) )
        
    variant_file_short_name   = arg1
    nb_of_files               = arg2
    nb_event                  = arg3
    CURRENT_OUTPUT_PATH       = arg0
    experiment_name           = arg4
    file_index                = arg5
    SEED_PATH           = CURRENT_OUTPUT_PATH+snemo_cfg.get('PRODUCTION_CFG','config_rel_path')+snemo_cfg.get('PRODUCTION_CFG','seed_rel_path')
    variant_file_name   = CURRENT_OUTPUT_PATH+snemo_cfg.get('PRODUCTION_CFG','config_rel_path')+snemo_cfg.get('PRODUCTION_CFG','variant_rel_path')+"/"+variant_file_short_name

    
    if arg6 != None:
        input_variant       = arg6
        gui_mode            = False
    else:
        print("No input variant file")
        
        
    urn_used = snemo_cfg.get('SIMU_CFG','urn_blessed_snemo')

    # To improve
    log_file_name=CURRENT_OUTPUT_PATH+snemo_cfg.get('PRODUCTION_CFG','sys_rel_path')+snemo_cfg.get('PRODUCTION_CFG','log_rel_path')+"/"+"main.log"
    log_file = open(log_file_name,"a")
    
    
    if gui_mode == True:
        print("\n\033[92mINFO\033[00m : [%s] : Starting GUI... Wait a while...."%(function_name))

    #     # ############### Start variant GUI to build variant config file #############
        if debug:
            print("DEBUG : [%s] : Configure variant file using gui"%(function_name))
            
        log_file.write('\nCOMMAND : %s/%s -t %s -o %s\n\n' %(snemo_cfg.get('SW_CFG','sw_path'),snemo_cfg.get('SW_CFG','sw_snemo_configuration'),urn_used,variant_file_name))    
        p = subprocess.Popen(args=[' %s/%s -t %s -o %s\n\n' %(snemo_cfg.get('SW_CFG','sw_path'),snemo_cfg.get('SW_CFG','sw_snemo_configuration'),urn_used,variant_file_name)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,shell=True)
        outputlines = p.stdout.readlines()
        p.wait()
        if p.wait() != 0:
            print ("\033[91mERROR\033[00m  : [%s] : Can not start variant gui ..."%function_name)
            print ("%s"%outputlines)
            exit(1)
        else:
            log_file.write("DEBUG : [%s] : variant file configuration done \n"%function_name)    
            if debug:
                print("DEBUG : [%s] : variant file configuration using gui done"%function_name )

    else:
    #             # ############### Start input variant file to prepare config #############
        if debug:
            print("DEBUG : [%s] use input variant file"%function_name)
            
        test_variant_file=os.path.isfile(input_variant)
        if test_input_variant == False:
            print("\033[91mERROR\033[00m  : %s :  Invalid variant file -> %s "%(function_name,input_variant))
            sys.exit(1)
        else:
            os.system("cp %s %s"%(input_variant,variant_file_name))  
            log_file.write('\nCOMMAND : %s/%s -t %s -i %s --no-gui\n\n' %(snemo_cfg.get('SW_CFG','sw_path'),snemo_cfg.get('SW_CFG','sw_snemo_configuration'),urn_used,variant_file_name))    
            p = subprocess.Popen(args=[' %s/%s -t %s -i %s --no-gui\n\n' %(snemo_cfg.get('SW_CFG','sw_path'),snemo_cfg.get('SW_CFG','sw_snemo_configuration'),urn_used,variant_file_name)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,shell=True)
            outputlines = p.stdout.readlines()
            p.wait()
            if p.wait() != 0:
                print ("\033[91mERROR\033[00m  : [%s] : variant file %s is not a valid config"%(function_name,input_variant))
                exit(1)
            else:
                log_file.write("INFO  : [%s] : variant file checked\n"%function_name)
                print("INFO  : [%s] : Input variant file checked"%function_name)
                #End of input variant file




    # # #######Create seeds files
    if debug:
        print("DEBUG : [%s] : start seeds production"%function_name )
        
    log_file.write('\nCOMMAND :%s/%s -d %s -n %s \n\n'%(snemo_cfg.get('SW_CFG','bx_install_path'),snemo_cfg.get('SW_CFG','bx_seeds'),SEED_PATH,nb_of_files))
    p = subprocess.Popen(args=['%s/%s -d %s -n %s'%(snemo_cfg.get('SW_CFG','bx_install_path'),snemo_cfg.get('SW_CFG','bx_seeds'),SEED_PATH,nb_of_files)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,shell=True)
    outputlines = p.stdout.readlines()
    p.wait()
    if p.wait() == 1:
        print ("\033[91mERROR\033[00m  : [%s] : Can not generate seeds ..."%function_name)
        print ("%s"%outputlines)
        exit(1)
    else:
        log_file.write("DEBUG : [%s] seeds files prodcution done\n"%function_name)
        if debug:
            print("DEBUG : [%s] : seeds files production done"%function_name )
            #End of seeds


    log_file.close()


    if debug:
        print("DEBUG : [%s] : ready to fill database logfile" %function_name)
    # ########## get vertex generator and primary event generator to fill DB #############
    variant_file=open(variant_file_name,"r")
    chaine=variant_file.readlines()
    size=len(chaine)
    for i in range(size):
        if chaine[i].find('registry="vertexes"') == 1:
            tmp=chaine[i+1]
            vertex_gen=tmp.split("=")
        if chaine[i].find('registry="primary_events"') == 1:
            tmp=chaine[i+1]
            primary_gen=tmp.split("=")

    my_vertex=vertex_gen[1].replace(' "','').rstrip("\n").rstrip('"')
    my_event=primary_gen[1].replace(' "','').rstrip("\n").rstrip('"')
    # generators obtained

    log_db_filename = CURRENT_OUTPUT_PATH+snemo_cfg.get('PRODUCTION_CFG','sys_rel_path')+snemo_cfg.get('PRODUCTION_CFG','log_rel_path')+"/"+snemo_cfg.get('DB_CFG','log_db')
    log_db = open(log_db_filename,'a')
    log_db.write('event_generator="%s"\n'%(my_event))
    log_db.write('vertex_generator="%s"\n'%(my_vertex))
    log_db.close()
    
    if debug:
        print("DEBUG : [%s] : ready for shell script production..." %function_name)
        ########### Prepare bunch of simulated files
    try:
        sn_multi_launcher.prepare_simu_launcher(nb_of_files,nb_event,experiment_name,CURRENT_OUTPUT_PATH,file_index,variant_file_short_name)
    except:
        print("\033[91mERROR\033[00m : [%s] : Can not launch properly sn_multi_launcher.py"%function_name)
        log_file.write("\033[91mERROR\033[00m: [%s] : Can not launch properly sn_multi_launcher.py"%function_name)
        sys.exit(1)
    # #end f bunch

    if debug:
        print("DEBUG : [%s] : shell script production done !"%function_name )
        print("DEBUG : *************************************")
