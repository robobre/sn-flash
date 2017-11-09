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


# def prepare_tree(arg0=None,arg1=None,arg2=None,arg3=None,arg4=None,arg5=None,arg6=None):
    
#     debug=True
#     gui_mode=True
#     function_start_time= datetime.now()
#     function_name="prepare_tree"

    
#     cfg = ConfigParser.ConfigParser()
#     snemo_cfg.read('config.cfg')

#     if debug:
#         print ("DEBUG : [%s] : Start function using (%s, %s, %s, %s, %s, %s) "%(function_name,arg0,arg1,arg2,arg3,arg4,arg5) )


#     if arg1 == "simulation":
#         simulation_mode = True
#         reconstruction_mode = False
#         nb_of_files         = arg5
#         nb_event            = arg6
#     elif arg1 == "reconstruction":
#         simulation_mode = False
#         reconstruction_mode = True
#     else:
#         simulation_mode = False
#         reconstruction_mode = False
        
#     experiment_name     = arg2
#     if arg3 == True:
#         production_mode = True
#     else:
#         production_mode = False
#     if arg4 == None:
#         pipeline_file   = None
#     else:
#         pipeline_file   = arg4
#     #pipeline_file ONLY if reconstruction_mode

#     if simulation_mode:
#         sw = snemo_cfg.get('SW_CFG','sw_snemo_simulation')
#         prefix_file=snemo_cfg.get('SIMU_CFG','simulation_tag')
        
#     elif reconstruction_mode:
#         sw = snemo_cfg.get('SW_CFG','sw_snemo_reconstruction')
#         prefix_file=snemo_cfg.get('RECO_CFG','reconstruction_tag')
        
#     if production_mode:
#         print ("\n\033[92mINFO\033[00m : [%s] : Production mode activated\n"%(function_name) )
#         OUTPUT_PATH=snemo_cfg.get('PRODUCTION_CFG','main_production_path')+"/blessed"
#         current_index=uuid.uuid1()

#     else:
#         print ("\n\033[92mINFO\033[00m : [%s] : User mode activated \n"%(function_name))
#         prefix_file="damned_"+prefix_file
#         OUTPUT_PATH=snemo_cfg.get('PRODUCTION_CFG','main_production_path')+"/"+snemo_cfg.get('USER_CFG','user')
#         current_index = input("REQUEST : Enter a unique identifier (number) : ")

        
#     sn_user_comment = raw_input("REQUEST : Enter a comment : ")
#     if not sn_user_comment:
#         print("\033[1;33;40mWARNING\033[00m : No user comment --> No comment the dark side is ... it, you will use ...!\n")
        
        
#     CURRENT_OUTPUT_PATH=OUTPUT_PATH+"/"+prefix_file+"_"+str(current_index)
    
    
#     log_file_short_name="main"+".log"
#     variant_short_name="variant"+".profile"
    
    
    
#     if debug:
#         print("\nDEBUG : [%s] : working tree starting by %s" % (function_name,CURRENT_OUTPUT_PATH))
#         print("             |-> CONFIG PATH            : %s" % (CURRENT_OUTPUT_PATH+snemo_cfg.get('PRODUCTION_CFG','config_rel_path')))
#         print("             |      |-> VARIANT PATH    : %s/" % (snemo_cfg.get('PRODUCTION_CFG','variant_rel_path')))
#         if simulation_mode:
#             print("             |      |-> SEED PATH    : %s/" % (snemo_cfg.get('PRODUCTION_CFG','seed_rel_path')))
#         print("             |      |      `-> file name: \033[96m {}\033[00m".format(variant_short_name))
#         print("             |      `-> CONF PATH       : %s/" % (snemo_cfg.get('PRODUCTION_CFG','conf_rel_path')))
#         print("             |->  OUTPUT DATA PATH      : %s" % (CURRENT_OUTPUT_PATH+snemo_cfg.get('PRODUCTION_CFG','output_rel_path')))
#         print("             `->  SYS PATH              : %s" % (CURRENT_OUTPUT_PATH+snemo_cfg.get('PRODUCTION_CFG','sys_rel_path')) )
#         print("                    |-> LOG PATH        : %s/" % snemo_cfg.get('PRODUCTION_CFG','log_rel_path'))
#         print("                    |      `-> file name: \033[96m {}\033[00m".format(log_file_short_name))
#         print("                    `-> LAUNCHER PATH   : %s/" % snemo_cfg.get('PRODUCTION_CFG','launcher_rel_path'))


     

#  #    ################ Create tree directories for simulation bunch ##########
#     try:
#         os.makedirs(CURRENT_OUTPUT_PATH)
#         #config
#         os.makedirs(CURRENT_OUTPUT_PATH+snemo_cfg.get('PRODUCTION_CFG','config_rel_path'))
#         if simulation_mode:
#             os.makedirs(CURRENT_OUTPUT_PATH+snemo_cfg.get('PRODUCTION_CFG','config_rel_path')+snemo_cfg.get('PRODUCTION_CFG','variant_rel_path')) 
#         os.makedirs(CURRENT_OUTPUT_PATH+snemo_cfg.get('PRODUCTION_CFG','config_rel_path')+snemo_cfg.get('PRODUCTION_CFG','conf_rel_path'))
#         #if simulate_mode:
#         #os.makedirs(CURRENT_OUTPUT_PATH+snemo_cfg.get('PRODUCTION_CFG','config_rel_path')+snemo_cfg.get('PRODUCTION_CFG','seed_rel_path')) ---> produced by g4seeds
#         #data
#         os.makedirs(CURRENT_OUTPUT_PATH+snemo_cfg.get('PRODUCTION_CFG','output_rel_path')) 
#         #.sys
#         os.makedirs(CURRENT_OUTPUT_PATH+snemo_cfg.get('PRODUCTION_CFG','sys_rel_path')) 
#         os.makedirs(CURRENT_OUTPUT_PATH+snemo_cfg.get('PRODUCTION_CFG','sys_rel_path')+snemo_cfg.get('PRODUCTION_CFG','log_rel_path'))
#         os.makedirs(CURRENT_OUTPUT_PATH+snemo_cfg.get('PRODUCTION_CFG','sys_rel_path')+snemo_cfg.get('PRODUCTION_CFG','launcher_rel_path')) 
        
        
#         os.system("chmod -R 755 %s" % CURRENT_OUTPUT_PATH)
#         log_file = open(CURRENT_OUTPUT_PATH+snemo_cfg.get('PRODUCTION_CFG','sys_rel_path')+snemo_cfg.get('PRODUCTION_CFG','log_rel_path')+"/"+log_file_short_name,"w")
#         #variant_file = open(variant_file_name,"w")
    
#     except:
#         print ("\033[91mERROR\033[00m : %s : Can not create directories ..."%function_name)
#         exit(1)
#     #End of directories creation

#     if debug:
#         print ("DEBUG : [%s] Working tree produced ! "%function_name)


#     p = subprocess.Popen(args=["%s/%s --version" % (snemo_cfg.get('SW_CFG','sw_path'),sw)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,shell=True)
#     outputlines = p.stdout.readlines()
#     p.wait()
    
#     log_file.write("\n")
#     log_file.write("DEBUG : [%s] :  working tree : \n"%function_name)
#     log_file.write("DEBUG : Start at             : %s \n" % function_start_time)
#     log_file.write("DEBUG : That log file name   : %s \n"%log_file_short_name)
#     log_file.write("DEBUG : ***** SW used ******\n")     
#     if simulation_mode:
#         log_file.write("DEBUG : Simulation exe       : %s/%s \n" % (snemo_cfg.get('SW_CFG','sw_path'),sw))
#         log_file.write("DEBUG : Simulation version   :\n \t%s\t%s\t%s\t%s" % (outputlines[5],outputlines[6],outputlines[7],outputlines[8] ) )
#         log_file.write("DEBUG : ***** setup used ******\n")     
#         log_file.write("DEBUG : main setup urn     : %s \n" % snemo_cfg.get('SIMU_CFG','urn_blessed_snemo'))
#     elif reconstruction_mode:
#         log_file.write("DEBUG : Reconstruction exe       : %s/%s \n" % (snemo_cfg.get('SW_CFG','sw_path'),sw))
#         log_file.write("DEBUG : Reconstruction version   :\n \t%s\t%s\t%s" % (outputlines[5],outputlines[6],outputlines[7] ) )
        
#     log_file.write("DEBUG : ***** Path used ******\n")     
#     log_file.write("DEBUG : OUTPUT_PATH          : %s \n" % (CURRENT_OUTPUT_PATH))
#     log_file.write("DEBUG : prefix_file          : %s \n" % prefix_file)
#     log_file.write("DEBUG : [%s] : working tree starting by %s \n" % (function_name,CURRENT_OUTPUT_PATH))
#     log_file.write("             |-> CONFIG PATH         : %s \n" % snemo_cfg.get('PRODUCTION_CFG','config_rel_path'))
#     if simulation_mode:
#         log_file.write("             |      |-> SEED PATH   : %s \n" % snemo_cfg.get('PRODUCTION_CFG','seed_rel_path'))
#         log_file.write("             |      |-> VARIANT PATH : %s \n" % snemo_cfg.get('PRODUCTION_CFG','variant_rel_path'))
#     log_file.write("             |      `-> CONF PATH    : %s \n" % snemo_cfg.get('PRODUCTION_CFG','conf_rel_path'))
#     log_file.write("             |->  OUTPUT DATA PATH   : %s \n" % snemo_cfg.get('PRODUCTION_CFG','output_rel_path'))
#     log_file.write("             `->  SYS PATH           : %s \n" % snemo_cfg.get('PRODUCTION_CFG','sys_rel_path'))
#     log_file.write("                    |-> LOG PATH     : %s \n" % snemo_cfg.get('PRODUCTION_CFG','log_rel_path'))
#     log_file.write("                    `-> LAUNCHER PATH: %s \n" % snemo_cfg.get('PRODUCTION_CFG','launcher_rel_path'))
#     if simulation_mode:
#         log_file.write("DEBUG : [%s] variant file name  : %s \n" % (function_name,variant_short_name))
    

#     #log_file.close()


#     if simulation_mode:
#         if debug:
#             print("DEBUG : [%s] : ready for simulation files production..."%function_name )
#             try:
#                 sn_simu_mgr.prepare_files(CURRENT_OUTPUT_PATH,variant_short_name,nb_of_files,nb_event,experiment_name,prefix_file+"_"+str(current_index))
#             except:
#                 print("\033[91mERROR\033[00m : [%s] : Can not prepare files for simulation purpose"%function_name)
#                 log_file.write("\033[91mERROR\033[00m : [%s] : Can not prepare files for simulation purpose"%function_name)
#                 sys.exit(1)
                
#     elif reconstruction_mode:
#         if debug:
#             print("DEBUG : [%s] : ready for reconstruction files production..."%function_name )
#             prepare_files(CURRENT_OUTPUT_PATH)
#     else:
#         print ("\033[91mERROR\033[00m : [%s] : Should be simulation OR reconstruction..."%function_name)
#         exit(1)
        

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
    
#  #    # try: 
#  #    #     #log_file.write("\033[92mINFO\033[00m  : %s\n" % line)
#  #    #     ##########client = pyAMI.client.Client('supernemo')
#  #    #     ##########client.execute(line)        
#  #    #     log_file.write("\033[92mINFO\033[00m : DB filled with %s" % line)
#  #    #     print("DEBUG : client.execute done!")
#  #    # except:
#  #    #     print("\033[91mERROR\033[00m : Can not fill properly the AMI DB")
#  #    #     sys.exit(1)
#  #    # End of DB access
#  #    try:
#  #        sn_multi_launcher.prepare_fill_db(CURRENT_OUTPUT_PATH,prefix_simu_file+"_"+str(current_index),line)
#  #        #sn_multi_launcher.prepare_tarball(CURRENT_OUTPUT_PATH,prefix_simu_file+"_"+str(current_index))
        
#  #    except:
#  #        print("\033[91mERROR\033[00m : Can not launch properly sn_multi_launcher.py")
#  #        log_file.write("\033[91mERROR\033[00m : Can not launch properly sn_multi_launcher.py")
#  #        sys.exit(1)
#  #    #end f bunch



   



#     simu_stop_time= datetime.now()
#     duration = simu_stop_time - function_start_time
        
#     if debug:
#         print ("DEBUG : [%s] : Start at %s" % (function_name,function_start_time))
#         print ("DEBUG : [%s] : Stop at %s" % (function_name,simu_stop_time))
#         print ("DEBUG : [%s] : Duration is %s seconds " %(function_name,duration.seconds))

#     log_file = open(CURRENT_OUTPUT_PATH+snemo_cfg.get('PRODUCTION_CFG','sys_rel_path')+snemo_cfg.get('PRODUCTION_CFG','log_rel_path')+"/"+log_file_short_name,"a")        

#     log_file.write("\n")
#     log_file.write("DEBUG : [%s] : Stop at %s \n" % (function_name,simu_stop_time))
#     log_file.write("DEBUG : [%s] : Duration is %s seconds \n" %(function_name,duration.seconds))
#     log_file.close()




def prepare_files(arg0=None,arg1=None):

    debug = True
    function_name = "prepare_files"

    if debug:
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

    



        
        
