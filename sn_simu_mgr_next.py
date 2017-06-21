#!/usr/local/python/python-2.7/bin/python


# Author  : Y.Lemiere
# Date    : 2016/07
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

###  AMI
import pyAMI.client
import pyAMI_supernemo


### Simulation launcher
import sn_multi_launcher
import cc_job_submitter


execfile("sn_simu_env.py")

### To do to improve that script 
### 
#   2017/02 --> VARIANT_REL_PATH="config/snemo/demonstrator/simulation/geant4_control/2.1/variants/repository.conf" 
#               |-> define in sn_simu_env.py but should propose/build by input/variable ? (demonstrator || bipo || half-comm)
#               |-> Improve a uniq id.
#   2017/06 --> Prepare some uniq server to provide blessed uniq ID before storage
#           --> Improve the way to create hpss dir     
###


def publish_production(arg0=None,arg1=None,arg2=None):

    debug=True
    function_name="publish_production"
    if debug:
        print ("\nDEBUG : Enter in %s function"%function_name)
        print ("DEBUG : --------------------------------------")
       
    
    if arg0 != None:
        INPUT_PATH = arg0
    else:
        print("ERROR : Need to provide input filename to publish")
        sys.exit(1)
    
    prod_mode=arg2
    simu_mode=arg1

    ##en fonction du role

    input_dir=os.path.dirname(INPUT_PATH)
    if prod_mode and simu_mode:
        official_name=input_dir+"/"+"snemo_production_0"
        os.system("mv %s %s"%(INPUT_PATH,official_name))
        print("INFO  : %s : Simu production renamed in %s"%(function_name,official_name))
    else:
        official_name=INPUT_PATH

#####UPDATE THE DB
    prepare_tarball(official_name)
    store_mc(official_name,"CCLYON",prod_mode)

def prepare_tarball(arg0=None):

    debug=True
    function_name="prepare_tarball"
    if debug:
        print ("\nDEBUG : Enter in %s function"%function_name)
        print ("DEBUG : --------------------------------------")
       
    
    if arg0 != None:
        CURRENT_OUTPUT_PATH = arg0
    else:
        print("ERROR : %s : Need to provide simu filename to make a tarball"% function_name)
        sys.exit(1)

    print("DEBUG : %s : Ready to make a tarball with %s" % (function_name,CURRENT_OUTPUT_PATH))
    
    in_file=CURRENT_OUTPUT_PATH#+"/"+simu_file_name
    simu_file_name      = os.path.basename(in_file)
    print ("DEBUG  : %s : prepare tarball from : %s "%(function_name,simu_file_name))
    tarball_name=in_file+".tar.gz"

    tar = tarfile.open(tarball_name, 'w:gz')
    for name in [in_file]:
        tar.add(name,arcname=simu_file_name)
    tar.close()
    
    print("DEBUG : Tarball prepared and ready to be stored safely")
    
    
    
        
def store_mc(arg0=None,arg1=None,arg2=None):
    
    debug=True
    function_name="store_mc"
    if debug:
        print ("\nDEBUG : Enter in %s function"%function_name)
        print ("DEBUG : --------------------------------------")
        
        
    if arg0 != None:
        file_to_store=arg0
    else:
        print("ERROR : Need to provide main simulation path for storage")
        sys.exit(1)
        
    if arg1 != "CCLYON":
        print("ERROR : Do not support other farm than CCLYON")
        sys.exit(1)
    else:
        print("DEBUG  : Ready to store %s on HPSS@CCLYON"%file_to_store)
    if arg2 == True:
        prod_mode=arg2
        print("INFO  : Storage in production mode (blessed) activated")
    if arg2 == None or arg2 == False:
        prod_mode=False
        print("INFO  : Storage in user mode (damned) activated")
    

    tarball_filename=file_to_store+".tar.gz"
    try:
        if prod_mode == False:
            os.system("rfcp %s %s" % (tarball_filename,HPSS_USER_PATH))
        else:
            os.system("rfcp %s %s" % (tarball_filename,HPSS_BLESSED_PATH))
    except:
        print("ERROR : %s : Can not store on %s "%(function_name,HPSS_USER_PATH))
        sys.exit(1)
        

def run_mc(arg0=None,arg1=None):
    
    if arg0 != None:
        main_path=arg0
    else:
        print("ERROR : Need to provide main simulation path for running")
        sys.exit(1)
        
    if arg1 != "CCLYON":
        print("ERROR : Do not support other farm than CCLYON")
        sys.exit(1)
    else:
        print("DEBUG : Ready to submit job at CCLYON")
        
    launch_path=main_path+sys_rel_path
        
    try:
        #os.system("chmod 755 %s" % uniq_launch_filename)
        log_path=main_path+sys_rel_path+log_rel_path+"/"
        launch_path=main_path+sys_rel_path+launcher_rel_path

        my_basename=os.path.basename(main_path)
        my_log_file="/main_"+my_basename+".log"
        print("DEBUG : Launch path : %s"%launch_path)
        print("DEBUG : Basename    : %s"%main_path)
        for file in os.listdir(launch_path):
            if fnmatch.fnmatch(file, '*.sh'):
                fileName, fileExtension = os.path.splitext(file)
                job_name=fileName
                uniq_launch_filename=launch_path+"/"+file
                cc_job_submitter.qsub(job_name,main_path,uniq_launch_filename)

                
        print("INFO  : cc_job_submitter.qsub done...")
    except:
        print("ERROR : %s : Can not use job_submitter properly using "%run_mc.__name__)
        sys.exit(1)



def prepare_mc_tree(arg0=None,arg1=None,arg2=None,arg3=None,arg4=None):
    
    debug=True
    gui_mode=True
    prepare_simu_start_time= datetime.now()
    function_name="prepare_mc_tree"

    ### Something to improve
    urn_used=urn_blessed_snemo



    if debug:
        print ("INFO : Enter in %s(%s, %s, %s, %s, %s) "%(function_name,arg0,arg1,arg2,arg3,arg4) )
        
        
    nb_of_file          = arg0
    nb_event            = arg1
    experiment_name     = arg2
    if arg3 == True:
        production_mode = True
    else:
        production_mode = False
    if arg4 == None:
        variant_profile = None
        print ("INFO : %s : GUI mode activated"%(function_name))
        gui_mode=True
    else:
        variant_profile     = arg4
        print ("INFO : %s : GUI mode NOT activated"%(function_name))
        gui_mode=False
        
    if production_mode:
        print ("\nINFO : Production mode activated\n")
        prefix_simu_file="sn_simu"
        SIMU_PATH=MAIN_SIMU_PATH+"/blessed"
        last_simu_index=0                                        ### A changer avec uniq ID
        current_simu_index=last_simu_index+1
        current_simu_index=uuid.uuid1()
    else:
        print ("\nINFO : User mode activated \n")
        prefix_simu_file="damned_simu"
        SIMU_PATH=MAIN_SIMU_PATH+"/"+os.environ['USER']            
        current_simu_index = input("REQUEST : Enter a unique identifier (number) : ")

    sn_user_comment = raw_input("REQUEST : Enter a comment : ")
    if not sn_user_comment:
        print("WARNING : No user comment --> No comment the dark side is ... it, you will use ...!\n")
    
        
    CURRENT_OUTPUT_PATH=SIMU_PATH+"/"+prefix_simu_file+"_"+str(current_simu_index)
    
 #     ###  ./config directory
    MAIN_CONFIG_PATH=CURRENT_OUTPUT_PATH+config_rel_path
    SEEDS_PATH= MAIN_CONFIG_PATH+seed_rel_path
    VARIANT_PATH=MAIN_CONFIG_PATH+variant_rel_path
    CONF_PATH=MAIN_CONFIG_PATH+conf_rel_path
    
    #### ./output directory
    CURRENT_OUTDATA_PATH=CURRENT_OUTPUT_PATH+output_rel_path

    #### ./.sys directory
    CURRENT_SYS_PATH=CURRENT_OUTPUT_PATH+sys_rel_path
    LOG_PATH=CURRENT_SYS_PATH+log_rel_path
    LAUNCHER_PATH=CURRENT_SYS_PATH+launcher_rel_path
    
    #### Filename
    #log_file_name=LOG_PATH+"/main_"+prefix_simu_file+"_"+str(current_simu_index)+".log"
    log_file_name=LOG_PATH+"/main"+".log"
    #variant_short_name="variant_"+str(current_simu_index)+".profile"
    variant_short_name="variant"+".profile"
    
    variant_file_name=VARIANT_PATH+"/"+variant_short_name
    


    if debug:
        print("\nDEBUG : %s : working tree starting by %s" % (function_name,CURRENT_OUTPUT_PATH))
        print("             |-> CONFIG PATH            : %s" % MAIN_CONFIG_PATH)
        print("             |      |-> SEEDS PATH      : %s" % SEEDS_PATH)
        print("             |      |-> VARIANT PATH    : %s" % VARIANT_PATH)
        print("             |      |      `-> file name: %s" % variant_short_name)
        print("             |      `-> CONF PATH       : %s" % CONF_PATH)
        print("             |->  OUTPUT DATA PATH      : %s" % CURRENT_OUTDATA_PATH)
        print("             `->  SYS PATH              : %s" % CURRENT_SYS_PATH)
        print("                    |-> LOG PATH        : %s" % LOG_PATH)
        print("                    |      `-> file name: %s" % log_file_name)
        print("                    `-> LAUNCHER PATH   : %s" % LAUNCHER_PATH)


     

 #    ################ Create tree directories for simulation bunch ##########
    try:
        os.makedirs(CURRENT_OUTPUT_PATH)
        #config
        os.makedirs(MAIN_CONFIG_PATH)
        ### os.makedirs(SEEDS_PATH) # created by bxg4_seeds
        os.makedirs(VARIANT_PATH) 
        os.makedirs(CONF_PATH)
        #data
        os.makedirs(CURRENT_OUTDATA_PATH) 
        #.sys
        os.makedirs(CURRENT_SYS_PATH) 
        os.makedirs(LOG_PATH) 
        os.makedirs(LAUNCHER_PATH) 
        
        
        os.system("chmod -R 755 %s" % CURRENT_OUTPUT_PATH)
        log_file = open(log_file_name,"w")
        variant_file = open(variant_file_name,"w")
    
    except:
        print ("ERROR : %s : Can not create directories ..."%function_name)
        exit(1)
    #End of directories creation

    if debug:
        print ("DEBUG : Working tree produced ! ")

        


    p = subprocess.Popen(args=["%s%s --version" % (SW_PATH,sw_snemo_simulation)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,shell=True)
    outputlines = p.stdout.readlines()
    p.wait()
        
    log_file.write("\n")
    log_file.write("DEBUG : %s working tree : \n"%function_name)
    log_file.write("DEBUG : Start at           : %s \n" % prepare_simu_start_time)
    log_file.write("DEBUG : That log file name : %s \n"%log_file_name)
    log_file.write("DEBUG : ***** SW used ******\n")     
    log_file.write("DEBUG : Simulation exe     : %s%s \n" % (SW_PATH,sw_snemo_simulation))
    log_file.write("DEBUG : Simulation version :\n \t%s\t%s\t%s\t%s" % (outputlines[5],outputlines[6],outputlines[7],outputlines[8] ) )
    log_file.write("DEBUG : ***** setup used ******\n")     
    log_file.write("DEBUG : main setup urn     : %s \n" % urn_used)
    log_file.write("DEBUG : ***** Path used ******\n")     
    log_file.write("DEBUG : SIMU_PATH          : %s \n" % SIMU_PATH)
    log_file.write("DEBUG : prefix_simu_file   : %s \n" % prefix_simu_file)
    log_file.write("DEBUG : %s : working tree starting by %s \n" % (function_name,CURRENT_OUTPUT_PATH))
    log_file.write("             |-> CONFIG PATH         : %s \n" % MAIN_CONFIG_PATH)
    log_file.write("             |      |-> SEEDS PATH   : %s \n" % SEEDS_PATH)
    log_file.write("             |      |-> VARIANT PATH : %s \n" % VARIANT_PATH)
    log_file.write("             |      `-> CONF PATH    : %s \n" % CONF_PATH)
    log_file.write("             |->  OUTPUT DATA PATH   : %s \n" % CURRENT_OUTDATA_PATH)
    log_file.write("             `->  SYS PATH           : %s \n" % CURRENT_SYS_PATH)
    log_file.write("                    |-> LOG PATH     : %s \n" % LOG_PATH)
    log_file.write("                    `-> LAUNCHER PATH: %s \n" % LAUNCHER_PATH)
    log_file.write("DEBUG : variant file name  : %s \n" % variant_file_name)
    

    if gui_mode == True:
        # ############### Start variant GUI to build variant config file #############
        if debug:
            print("DEBUG : start variant gui" )
            
            log_file.write('\nCOMMAND : %s/%s -t %s -o %s\n\n' %(SW_PATH,sw_snemo_configuration,urn_blessed_snemo,variant_file_name))    
            p = subprocess.Popen(args=[' %s/%s -t %s -o %s\n\n' %(SW_PATH,sw_snemo_configuration,urn_blessed_snemo,variant_file_name)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,shell=True)
            outputlines = p.stdout.readlines()
            p.wait()
            if p.wait() != 0:
                print ("ERROR : %s : Can not start variant gui ..."%function_name)
                print ("%s"%outputlines)
                exit(1)
            else:
                log_file.write("DEBUG : variant file done \n")    
                if debug:
                    print("DEBUG : %s : variant gui done"%function_name )
        #End of variant GUI
    else:
        # ############### Start input variant file to prepare config #############
        if debug:
            print("DEBUG : use input variant file" )
            
        test_variant_file=os.path.isfile(variant_profile)
        if test_variant_file == False:
            print("ERROR : %s :  Invalid variant file -> %s "%(function_name,variant_profile))
            sys.exit(1)
        else:
            os.system("cp %s %s"%(variant_profile,variant_file_name))  
            log_file.write('\nCOMMAND : %s/%s -t %s -i %s --no-gui\n\n' %(SW_PATH,sw_snemo_configuration,urn_blessed_snemo,variant_file_name))    
            p = subprocess.Popen(args=[' %s/%s -t %s -i %s --no-gui\n\n' %(SW_PATH,sw_snemo_configuration,urn_blessed_snemo,variant_file_name)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,shell=True)
            outputlines = p.stdout.readlines()
            p.wait()

            if p.wait() != 0:
                print ("ERROR : %s : variant file %s is not a valid config"%(function_name,variant_profile))
                exit(1)
            else:
                log_file.write("INFO  : variant file checked\n")
                print("INFO  : %s : Input variant file checked"%function_name)

        #End of input variant file




    # #######Create seeds files
    if debug:
        print("DEBUG : start seeds production" )
       
    log_file.write('\nCOMMAND :%s/%s -d %s -n %s \n\n'%(BX_INSTALL_PATH,bx_seeds,SEEDS_PATH,nb_of_file))
    p = subprocess.Popen(args=['%s/%s -d %s -n %s'%(BX_INSTALL_PATH,bx_seeds,SEEDS_PATH,nb_of_file)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,shell=True)
    outputlines = p.stdout.readlines()
    p.wait()
    if p.wait() == 1:
        print ("ERROR : %s : Can not generate seeds ..."%function_name)
        print ("%s"%outputlines)
        exit(1)
    else:
        log_file.write("DEBUG : seeds files done\n")
        if debug:
            print("DEBUG : seeds production done" )
    #End of seeds


    log_file.close()

    ########## get vertex generator and primary event generator to fill DB #############
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

    if debug:
        print("DEBUG : ready for shell script production..." )
    ########### Prepare bunch of simulated files
    try:
        sn_multi_launcher.prepare_launcher(nb_of_file,nb_event,experiment_name,CURRENT_OUTPUT_PATH,prefix_simu_file+"_"+str(current_simu_index),variant_short_name)
        
    except:
        print("ERROR : Can not launch properly sn_multi_launcher.py")
        log_file.write("ERROR : Can not launch properly sn_multi_launcher.py")
        sys.exit(1)
    #end f bunch

    if debug:
        print("DEBUG : shell script production done !" )
        
 # ############# Fill DB using AMI client #########
    line='AddElement -project="supernemo" -processingStep="production" -entity="demo"'
    line+=' -simu_id="'+prefix_simu_file+'_'+str(current_simu_index)+'"'
    line+=' -confidence_level="damned"'
    line+=' -checking_status="unchecked"'
    line+=' -event_generator="'+my_event+'"'
    line+=' -experiment="'+experiment_name+'"'
    line+=' -event_per_file="'+nb_event+'"'
    line+=' -nb_of_file="'+nb_of_file+'"'
    line+=' -simu_path="'+CURRENT_OUTPUT_PATH+'"'
    line+=' -user_comment="'+sn_user_comment+'"'
    line+=' -vertex_generator="'+my_vertex+'"'
    line+=' -user="'+USER+'"'
    #line+=' -date="'+start_time+'"'
    
    # try: 
    #     #log_file.write("INFO  : %s\n" % line)
    #     ##########client = pyAMI.client.Client('supernemo')
    #     ##########client.execute(line)        
    #     log_file.write("INFO : DB filled with %s" % line)
    #     print("DEBUG : client.execute done!")
    # except:
    #     print("ERROR : Can not fill properly the AMI DB")
    #     sys.exit(1)
    # End of DB access
    try:
        sn_multi_launcher.prepare_fill_db(CURRENT_OUTPUT_PATH,prefix_simu_file+"_"+str(current_simu_index),line)
        #sn_multi_launcher.prepare_tarball(CURRENT_OUTPUT_PATH,prefix_simu_file+"_"+str(current_simu_index))
        
    except:
        print("ERROR : Can not launch properly sn_multi_launcher.py")
        log_file.write("ERROR : Can not launch properly sn_multi_launcher.py")
        sys.exit(1)
    #end f bunch



   



    simu_stop_time= datetime.now()
    duration = simu_stop_time - prepare_simu_start_time
        
    if debug:
        print ("DEBUG : Start at %s" % prepare_simu_start_time)
        print ("DEBUG : Stop at %s" % simu_stop_time)
        print ("DEBUG : Duration is %s seconds " %duration.seconds) 
        
    log_file = open(log_file_name,"a")
    log_file.write("\n")
    log_file.write("DEBUG : Stop at %s \n" % simu_stop_time)
    log_file.write("DEBUG : Duration is %s seconds \n" %duration.seconds) 
    log_file.close()




