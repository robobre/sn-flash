#!/usr/bin/env python

# Author  : Y.Lemiere
# Date    : 2017/11
# Contact : lemiere@lpccaen.in2p3.fr
# Object  : SuperNEMO output tree manager



from datetime import date, datetime
import time
import sys
import os
import subprocess
## import configparser as ConfigParser ##python3
#import ConfigParser

try:
    # Python 2 only:
    import ConfigParser as ConfigParser
except ImportError:
    # Python 2 and 3 (after ``pip install configparser``)
    import configparser as ConfigParser



import uuid
import fnmatch
import tarfile

import sn_simu_mgr
import sn_reco_mgr
import cc_job_submitter
import sim_database_connector
import variant_parser
import getpass

###  AMI
# import pyAMI.client
# import pyAMI_supernemo


def prepare_tree(arg0=None,arg1=None,arg2=None,arg3=None,arg4=None,arg5=None,arg6=None):
    
    debug=True
    gui_mode=True
    function_start_time= datetime.now()
    function_name="prepare_tree"

    snemo_cfg = ConfigParser.ConfigParser()
    snemo_cfg.read('snemo.cfg')

    user_cfg = ConfigParser.ConfigParser()
    user_cfg.read('user.cfg')

    
        
    if arg1 == "simulation":
        simulation_mode     = True
        reconstruction_mode = False
        nb_of_files         = arg5
        nb_event            = arg6
        if debug:
            print ("DEBUG : [%s] : Start simulation tree using (%s, %s, %s, %s, %s, %s, %s) "%(function_name,arg0,arg1,arg2,arg3,arg4,arg5,arg6) )
    elif arg1 == "reconstruction":
        simulation_mode     = False
        reconstruction_mode = True
        INPUT_PATH          = arg0
        if debug:
            print ("DEBUG : [%s] : Start reconstruction tree using (%s) "%(function_name,arg0) )
    else:
        simulation_mode     = False
        reconstruction_mode = False
        
    experiment_name     = arg2
    if arg3 == True:
        production_mode = True
    else:
        production_mode = False
    # if arg4 == None:
    #     pipeline_file   = None
    # else:
    #     pipeline_file   = arg4
    #pipeline_file ONLY if reconstruction_mode

    if simulation_mode:
        sw = snemo_cfg.get('SW_CFG','sw_snemo_simulation')
        prefix_file=snemo_cfg.get('SIMU_CFG','simulation_tag')
        
    elif reconstruction_mode:
        sw = snemo_cfg.get('SW_CFG','sw_snemo_reconstruction')
        prefix_file=snemo_cfg.get('RECO_CFG','reconstruction_tag')
        
    if production_mode:
        print ("\n\033[92mINFO\033[00m : [%s] : Production mode activated\n"%(function_name) )
        OUTPUT_PATH=snemo_cfg.get('PRODUCTION_CFG','main_production_path')+"/blessed"
        #current_index=uuid.uuid1()
#        try:
        myconnect=sim_database_connector.MYSQL_SIM_DATA()
        print(myconnect.is_connected())
        if simulation_mode:
           current_index=myconnect.new_row()
        if reconstruction_mode:
           current_index=myconnect.new_row_reco()
#        except:
#                print ("\033[91mERROR\033[00m   Can not connect to MYSQL ...")
	
	

    else:
        print ("\n\033[92mINFO\033[00m : [%s] : User mode activated \n"%(function_name))
        prefix_file="damned_"+prefix_file
        OUTPUT_PATH=snemo_cfg.get('PRODUCTION_CFG','main_production_path')+"/"+user_cfg.get('USER_CFG','user')
        current_index = input("REQUEST : Enter a unique identifier (number) : ")

    if sys.version_info[0] == 2:
        sn_user_comment = raw_input("REQUEST : Enter a comment : ")
    if sys.version_info[0] == 3:
        sn_user_comment = input("REQUEST : Enter a comment : ")

        
    if not sn_user_comment:
        print("\033[1;33;40mWARNING\033[00m : No user comment --> No comment the dark side is ... it, you will use ...!\n")


        
    CURRENT_OUTPUT_PATH = OUTPUT_PATH+"/"+prefix_file+"_"+str(current_index)
    if production_mode:
        HPSS_OUTPUT_PATH = snemo_cfg.get('PRODUCTION_CFG','hpss_blessed_path')+"/"+prefix_file+"_"+str(current_index)
    else:
        HPSS_OUTPUT_PATH = snemo_cfg.get('PRODUCTION_CFG','hpss_user_path')+"/"+prefix_file+"_"+str(current_index)
    
    log_file_short_name="main"+".log"
    variant_short_name="variant"+".profile"
    
    
    
    #if debug:
    print("\nINFO : [%s] : working tree starting by %s" % (function_name,CURRENT_OUTPUT_PATH))
    if reconstruction_mode:
        print("\nINFO : [%s] : Based on SD production : %ss" % (function_name,INPUT_PATH))
    print("             |-> CONFIG PATH            : %s" % (CURRENT_OUTPUT_PATH+snemo_cfg.get('PRODUCTION_CFG','config_rel_path')))
    if simulation_mode:
        print("             |      |-> VARIANT PATH    : %s/" % (snemo_cfg.get('PRODUCTION_CFG','variant_rel_path')))
        print("             |      |      `-> file name: \033[96m {}\033[00m".format(variant_short_name))
        print("             |      |-> SEED PATH    : %s/" % (snemo_cfg.get('PRODUCTION_CFG','seed_rel_path')))
        
    print("             |      `-> CONF PATH       : %s/" % (snemo_cfg.get('PRODUCTION_CFG','conf_rel_path')))
    print("             |->  OUTPUT DATA PATH      : %s" % (CURRENT_OUTPUT_PATH+snemo_cfg.get('PRODUCTION_CFG','output_rel_path')))
    print("             `->  SYS PATH              : %s" % (CURRENT_OUTPUT_PATH+snemo_cfg.get('PRODUCTION_CFG','sys_rel_path')) )
    print("                    |-> LOG PATH        : %s/" % snemo_cfg.get('PRODUCTION_CFG','log_rel_path'))
    print("                    |      `-> file name: \033[96m {}\033[00m".format(log_file_short_name))
    print("                    `-> LAUNCHER PATH   : %s/" % snemo_cfg.get('PRODUCTION_CFG','launcher_rel_path'))


     

 #    ################ Create tree directories for simulation bunch ##########
    try:
        os.makedirs(CURRENT_OUTPUT_PATH)
        #config
        os.makedirs(CURRENT_OUTPUT_PATH+snemo_cfg.get('PRODUCTION_CFG','config_rel_path'))
        if simulation_mode:
            os.makedirs(CURRENT_OUTPUT_PATH+snemo_cfg.get('PRODUCTION_CFG','config_rel_path')+snemo_cfg.get('PRODUCTION_CFG','variant_rel_path'))
        os.makedirs(CURRENT_OUTPUT_PATH+snemo_cfg.get('PRODUCTION_CFG','config_rel_path')+snemo_cfg.get('PRODUCTION_CFG','conf_rel_path'))
        #data
        os.makedirs(CURRENT_OUTPUT_PATH+snemo_cfg.get('PRODUCTION_CFG','output_rel_path')) 
        #.sys
        os.makedirs(CURRENT_OUTPUT_PATH+snemo_cfg.get('PRODUCTION_CFG','sys_rel_path')) 
        os.makedirs(CURRENT_OUTPUT_PATH+snemo_cfg.get('PRODUCTION_CFG','sys_rel_path')+snemo_cfg.get('PRODUCTION_CFG','log_rel_path'))
        os.makedirs(CURRENT_OUTPUT_PATH+snemo_cfg.get('PRODUCTION_CFG','sys_rel_path')+snemo_cfg.get('PRODUCTION_CFG','launcher_rel_path')) 
        
        
        os.system("chmod -R 755 %s" % CURRENT_OUTPUT_PATH)
        log_file = open(CURRENT_OUTPUT_PATH+snemo_cfg.get('PRODUCTION_CFG','sys_rel_path')+snemo_cfg.get('PRODUCTION_CFG','log_rel_path')+"/"+log_file_short_name,"w")
        
    
    except:
        print ("\033[91mERROR\033[00m : [%s] : Can not create directories ..."%function_name)
        exit(1)
    #End of directories production

    if debug:
        print ("DEBUG : [%s] : Working tree produced ! "%function_name)


    p = subprocess.Popen(args=["%s/%s --version" % (snemo_cfg.get('SW_CFG','sw_path'),sw)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,shell=True)
    outputlines = p.stdout.readlines()
    p.wait()

    
    p = subprocess.Popen(args=["%s/flsimulate --version" % (snemo_cfg.get('SW_CFG','sw_path'))],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,shell=True)
    subprocess_output = p.stdout.readlines()
    p.wait()
    

    
    
    falaise_version=str(subprocess_output[0]).split(" ")[1]
    
    log_file.write("\n")
    log_file.write("DEBUG : [%s] :  working tree : \n"%function_name)
    log_file.write("DEBUG : Start at             : %s \n" % function_start_time)
    log_file.write("DEBUG : That log file name   : %s \n"%log_file_short_name)
    log_file.write("DEBUG : ***** SW used ******\n")     
    if simulation_mode:
        log_file.write("DEBUG : Simulation exe       : %s/%s \n" % (snemo_cfg.get('SW_CFG','sw_path'),sw))
        log_file.write("DEBUG : Simulation version   :\n \t%s\t%s\t%s\t%s\n" % (outputlines[5],outputlines[6],outputlines[7],outputlines[8] ) )
        log_file.write("DEBUG : ***** setup used ******\n")     
        log_file.write("DEBUG : main setup urn     : %s \n" % snemo_cfg.get('SIMU_CFG','urn_blessed_snemo'))
    elif reconstruction_mode:
        log_file.write("DEBUG : Reconstruction exe       : %s/%s \n" % (snemo_cfg.get('SW_CFG','sw_path'),sw))
        log_file.write("DEBUG : Reconstruction version   :\n \t%s\t%s\t%s" % (outputlines[5],outputlines[6],outputlines[7] ) )
        
    log_file.write("DEBUG : ***** Path used ******\n")     
    log_file.write("DEBUG : OUTPUT_PATH          : %s \n" % (CURRENT_OUTPUT_PATH))
    log_file.write("DEBUG : prefix_file          : %s \n" % prefix_file)
    log_file.write("DEBUG : [%s] : working tree starting by %s \n" % (function_name,CURRENT_OUTPUT_PATH))
    log_file.write("             |-> CONFIG PATH         : %s \n" % snemo_cfg.get('PRODUCTION_CFG','config_rel_path'))
    if simulation_mode:
        log_file.write("             |      |-> SEED PATH   : %s \n" % snemo_cfg.get('PRODUCTION_CFG','seed_rel_path'))
        log_file.write("             |      |-> VARIANT PATH : %s \n" % snemo_cfg.get('PRODUCTION_CFG','variant_rel_path'))
    log_file.write("             |      `-> CONF PATH    : %s \n" % snemo_cfg.get('PRODUCTION_CFG','conf_rel_path'))
    log_file.write("             |->  OUTPUT DATA PATH   : %s \n" % snemo_cfg.get('PRODUCTION_CFG','output_rel_path'))
    log_file.write("             `->  SYS PATH           : %s \n" % snemo_cfg.get('PRODUCTION_CFG','sys_rel_path'))
    log_file.write("                    |-> LOG PATH     : %s \n" % snemo_cfg.get('PRODUCTION_CFG','log_rel_path'))
    log_file.write("                    `-> LAUNCHER PATH: %s \n" % snemo_cfg.get('PRODUCTION_CFG','launcher_rel_path'))
    if simulation_mode:
        log_file.write("DEBUG : [%s] variant file name  : %s \n" % (function_name,variant_short_name))
    

    log_db_filename = CURRENT_OUTPUT_PATH+snemo_cfg.get('PRODUCTION_CFG','sys_rel_path')+snemo_cfg.get('PRODUCTION_CFG','log_rel_path')+"/"+snemo_cfg.get('DB_CFG','log_db')
    log_db = open(log_db_filename,'w')
    log_db.write('project="supernemo"\n')
    log_db.write('processingStep="production"\n')
    log_db.write('entity="demo"\n')
    
    log_db.write('sw_version="Falaise_%s"\n'%(falaise_version))
    log_db.write('experiment="%s"\n'%(experiment_name))
    log_db.write('user="%s"\n'%(user_cfg.get('USER_CFG','user')))
    log_db.write('simu_id="%s"\n'%(prefix_file+"_"+str(current_index)))
    log_db.write('checking_status="unchecked"\n')
    
    
    
    if production_mode:
        log_db.write('confidence_level="blessed"\n')
    else:
        log_db.write('confidence_level="damned"\n')
        
    if simulation_mode:
        log_db.write('event_per_file="%s"\n'%(nb_event))
        log_db.write('nb_of_file="%s"\n'%(nb_of_files))
        log_db.write('UID="%s"\n'%(current_index))
    
    log_db.write('user_comment="%s"\n'%(sn_user_comment))
    log_db.write('date="%s"\n'%(datetime.now()))

    log_db.close()




    if simulation_mode:
        if debug:
            print("DEBUG : [%s] : ready for simulation files production..."%function_name )
            try:
              sn_simu_mgr.prepare_files(CURRENT_OUTPUT_PATH,variant_short_name,nb_of_files,nb_event,experiment_name,prefix_file+"_"+str(current_index))
              if production_mode:
                variant_p=variant_parser.variant_parser(0)
                variant_path=CURRENT_OUTPUT_PATH+snemo_cfg.get('PRODUCTION_CFG','config_rel_path')+snemo_cfg.get('PRODUCTION_CFG','variant_rel_path')
                variant_p.parse_file( variant_path,variant_short_name)
                magnetic = [val for key, val in variant_p.data["geometry"].items() if "magnetic_field" in key]
                source=[val for key, val in variant_p.data["geometry"].items() if "source_layout" in key]
                myconnect.init_prod(int(current_index),getpass.getuser(),  variant_p.data["primary_events"]["generator"],  variant_p.data["vertexes"]["generator"],snemo_cfg.get('SIMU_CFG','urn_blessed_snemo'),str(magnetic),str(source),variant_path+"/"+variant_short_name,CURRENT_OUTPUT_PATH, falaise_version,sn_user_comment,nb_event,nb_of_files  )
            except:
              print("\033[91mERROR\033[00m : [%s] : Can not prepare files for simulation purpose"%function_name)
              log_file.write("\033[91mERROR\033[00m : [%s] : Can not prepare files for simulation purpose"%function_name)
              sys.exit(1)
    
    elif reconstruction_mode:
        if debug:
            print("DEBUG : [%s] : ready for reconstruction files production..."%function_name )
            sn_reco_mgr.prepare_files(CURRENT_OUTPUT_PATH,INPUT_PATH)
            if production_mode:
              par=variant_parser.variant_parser(0)
              par.parse_db(INPUT_PATH+"/.sys/log.d/","simu.db")
              myconnect.init_reco(int(current_index),par.data["UID"], falaise_version,1,CURRENT_OUTPUT_PATH+"/config.d/conf.d/flreconstruct.conf","none", CURRENT_OUTPUT_PATH ,sn_user_comment)
#              myconnect.store_simu()
            
    else:
        print ("\033[91mERROR\033[00m : [%s] : Should be simulation OR reconstruction..."%function_name)
        exit(1)
        
 

 #    #     ##########client = pyAMI.client.Client('supernemo')
 #    #     ##########client.execute(line)        

 #    try:
 #        sn_multi_launcher.prepare_fill_db(CURRENT_OUTPUT_PATH,prefix_simu_file+"_"+str(current_index),line)
 #        #sn_multi_launcher.prepare_tarball(CURRENT_OUTPUT_PATH,prefix_simu_file+"_"+str(current_index))




   



    simu_stop_time= datetime.now()
    duration = simu_stop_time - function_start_time
        
    if debug:
        print ("DEBUG : [%s] : Start at %s" % (function_name,function_start_time))
        print ("DEBUG : [%s] : Stop at %s" % (function_name,simu_stop_time))
        print ("DEBUG : [%s] : Duration is %s seconds " %(function_name,duration.seconds))

    log_file = open(CURRENT_OUTPUT_PATH+snemo_cfg.get('PRODUCTION_CFG','sys_rel_path')+snemo_cfg.get('PRODUCTION_CFG','log_rel_path')+"/"+log_file_short_name,"a")        

    log_file.write("\n")
    log_file.write("DEBUG : [%s] : Stop at %s \n" % (function_name,simu_stop_time))
    log_file.write("DEBUG : [%s] : Duration is %s seconds \n" %(function_name,duration.seconds))
    log_file.close()



##################################################### fucntion run_mc
def run(arg0=None,arg1=None):

    debug = True
    function_name="run"
    snemo_cfg = ConfigParser.ConfigParser()
    snemo_cfg.read('snemo.cfg')
    
    if arg0 != None:
        main_path=arg0
    else:
        print("\033[91mERROR\033[00m : [%s] : Need to provide main simulation path for running"%function_name)
        sys.exit(1)
        
    if arg1 != "CCLYON":
        print("\033[91mERROR\033[00m :  [%s] : Do not support other farm than CCLYON"%function_name)
        sys.exit(1)
    else:
        print("DEBUG : [%s] : Ready to submit job at CCLYON"%function_name)
        
        #launch_path=main_path+snemo_cfg.get('PRODUCTION_CFG','sys_rel_path')
        
    try:
        #os.system("chmod 755 %s" % uniq_launch_filename)
        log_path=main_path+snemo_cfg.get('PRODUCTION_CFG','sys_rel_path')+snemo_cfg.get('PRODUCTION_CFG','log_rel_path')+"/"
        launch_path=main_path+snemo_cfg.get('PRODUCTION_CFG','sys_rel_path')+snemo_cfg.get('PRODUCTION_CFG','launcher_rel_path')

        my_basename=os.path.basename(main_path)
        my_log_file="/main_"+my_basename+".log"

        list_of_script = os.listdir(launch_path)
        if not list_of_script:
            print("\033[91mERROR\033[00m : [%s] : No script to process :%s"%(function_name,launch_path))
            sys.exit(1)

        
        if debug: 
            print("DEBUG : [%s] : Basename    : %s"%(function_name,main_path))
            print("DEBUG : [%s] : Launch path : %s"%(function_name,launch_path))
            print("DEBUG : [%s] : List of script : %s"%(function_name,list_of_script))
                        
            
        for file in list_of_script:
            if fnmatch.fnmatch(file, '*.sh'):
                fileName, fileExtension = os.path.splitext(file)
                job_name=fileName
                uniq_launch_filename=launch_path+"/"+file
                cc_job_submitter.qsub(job_name,main_path,uniq_launch_filename)
		

                
        print("INFO  : [%s] : cc_job_submitter.qsub done..."%function_name)
    except:
        print("\033[91mERROR\033[00m : [%s] : Can not use job_submitter properly using "%run.__name__)
        sys.exit(1)
##################################################### end of run_mc


##################################################### function prepare_tarball
def prepare_tarball(arg0):

    debug=True
    function_name="prepare_tarball"
    if debug:
        print ("DEBUG : --------------------------------------")
        print ("DEBUG : [%s] : Start function"%function_name)

    snemo_cfg = ConfigParser.ConfigParser()
    snemo_cfg.read('snemo.cfg')

    CURRENT_OUTPUT_PATH = arg0
    in_file_conf = CURRENT_OUTPUT_PATH+"/"+snemo_cfg.get('PRODUCTION_CFG','config_rel_path')
    in_file_sys  = CURRENT_OUTPUT_PATH+"/"+snemo_cfg.get('PRODUCTION_CFG','sys_rel_path')

    COPY_OUTPUT_PATH = CURRENT_OUTPUT_PATH+"_bkp"

    os.makedirs(COPY_OUTPUT_PATH)
    os.makedirs(COPY_OUTPUT_PATH+snemo_cfg.get('PRODUCTION_CFG','output_rel_path'))
    conf_tarball = COPY_OUTPUT_PATH+"/meta.tar.gz"

    if debug:
        print("DEBUG : [%s] : Ready to prepare a tarball with %s" % (function_name,CURRENT_OUTPUT_PATH))
    
    tar = tarfile.open(conf_tarball, 'w:gz')
    for name in [in_file_conf]:
        tar.add(name,arcname="config.d")
        
        
    for name in [in_file_sys]:
        tar.add(name,arcname=".sys")
            
    tar.close()
    if debug: 
        print("DEBUG : [%s] : Tarball prepared and ready to be stored safely"%function_name)


def store(arg0=None,arg1=None,arg2=None):
    
    debug=True
    function_name="store_mc"
    if debug:
        print ("DEBUG : --------------------------------------")
        print ("DEBUG : [%s] Start function "%function_name)
    

    snemo_cfg = ConfigParser.ConfigParser()
    snemo_cfg.read('snemo.cfg')

    user_cfg = ConfigParser.ConfigParser()
    user_cfg.read('user.cfg')
        


    if arg0 != None:
        file_to_store=arg0
    else:
        print("\033[91mERROR\033[00m : [%s] : Need to provide main production path for storage"%function_name)
        sys.exit(1)
        
    if arg1 != "CCLYON":
        print("\033[91mERROR\033[00m : [%s] : Do not support other farm than CCLYON"%function_name)
        sys.exit(1)
    else:
        print("DEBUG : [%s] : Ready to store %s on HPSS@CCLYON"%(function_name,file_to_store))
    if arg2 == True:
        prod_mode=arg2
        print("\033[92mINFO\033[00m  : [%s] : Storage in production mode (blessed) activated"%function_name)
    if arg2 == None or arg2 == False:
        prod_mode=False
        print("\033[92mINFO\033[00m  : [%s] : Storage in user mode (damned) activated"%function_name)
    

    tarball_filename  = file_to_store+"_bkp"
    tarball_meta      = tarball_filename+"/meta.tar.gz"
    basename_file     = os.path.basename(file_to_store)
    dirname_file      = os.path.dirname(file_to_store)
    output_briofile   =  file_to_store+"/output_files.d"

    legal_ext = [".brio", ".meta"]
   
    list_of_files=os.listdir(output_briofile)
    list_of_legal_files=[]
    for el in list_of_files:
        if el.endswith(tuple(legal_ext)):
            list_of_legal_files.append(el)

    if not list_of_legal_files:
        print("\033[91mERROR\033[00m : [%s] : No BRIO files in :%s"%(function_name,output_briofile))
        sys.exit(1)
    else:
        if debug: 
            print ("DEBUG : [%s] : list of (%s) files to backup : \n%s"%(function_name,len(list_of_legal_files),list_of_legal_files)) 

    

    try:
        if prod_mode == False:
            copy_path = snemo_cfg.get('PRODUCTION_CFG','hpss_user_path')+"/"+user_cfg.get('USER_CFG','user')
        else:
            copy_path = snemo_cfg.get('PRODUCTION_CFG','hpss_blessed_path')

        if debug: 
            print("\033[92mINFO\033[00m  : [%s] : Expected storage path : %s/%s"%(function_name,copy_path,basename_file))

        path_exist = os.system("rfstat %s >/dev/null 2>&1"%copy_path)
        if path_exist != 0:
            success_command = os.system("rfmkdir %s"%copy_path)
            if success_command == False:
                print ("\033[91mERROR\033[00m : [%s] : Can not create storage path %s"%(function_name,copy_path))
                sys.exit(1)
            else:
                if debug: 
                    print("DEBUG : [%s] : Storage path create (%s)"%(function_name,copy_path))
                
        else:
            os.system("rfmkdir %s/%s" % (copy_path,basename_file))
            os.system("rfmkdir %s/%s/output_files.d" % (copy_path,basename_file))
            for el in list_of_legal_files:
                os.system("rfcp %s/%s %s/%s/output_files.d/." % (output_briofile,el,copy_path,basename_file))


            os.system("rfcp %s %s/%s/." % (tarball_meta,copy_path,basename_file))
                
                


    except:
        print("\033[91mERROR\033[00m : [%s] : Can not store on %s "%(function_name,HPSS_USER_PATH))
        sys.exit(1)


##################################################### function publish_production
def publish_production(arg0=None,arg1=None,arg2=None):

    debug=True
    function_name="publish_production"
    if debug:
        print ("DEBUG : --------------------------------------")
        print ("\nDEBUG : [%s] : Start function"%function_name)

       
    
    if arg0 != None:
        INPUT_PATH = arg0
    else:
        print("\033[91mERROR\033[00m : Need to provide input filename to publish")
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

##################################################### end of publish_production


def prepare_db(arg0):

    debug=True
    function_name="prepare_db"


    if debug:
        print ("DEBUG : --------------------------------------")
        print ("DEBUG : [%s] : Start function for production : %s "%(function_name,arg0))
        
    
    snemo_cfg = ConfigParser.ConfigParser()
    snemo_cfg.read('snemo.cfg')


    #client = pyAMI.client.Client('supernemo')

    CURRENT_OUTPUT_PATH = arg0
    
    log_db_filename = CURRENT_OUTPUT_PATH+snemo_cfg.get('PRODUCTION_CFG','sys_rel_path')+snemo_cfg.get('PRODUCTION_CFG','log_rel_path')+"/"+snemo_cfg.get('DB_CFG','log_db')
    log_db = open(log_db_filename,'r')

    db_input="AddElement "

    with open(log_db_filename) as file_to_read:
        for line in file_to_read:
            db_input+="-"+line.rstrip('\n')+" "

    print(db_input)
    #client.execute(db_input)
    log_db.close()



    if debug:
        print ("DEBUG : --------------------------------------")



def check_production_status(arg0):
    
    snemo_cfg = ConfigParser.ConfigParser()
    snemo_cfg.read('snemo.cfg')
    
    debug       = True
    prod_status = False
    if debug:
        print("DEBUG : *************************************")
        print("INFO  : [%s] : Check production status for official publication (%s)"%(check_production_status.__name__,arg0) )


    PROD_PATH = arg0
    
    main_log_filename = PROD_PATH+snemo_cfg.get('PRODUCTION_CFG','sys_rel_path')+snemo_cfg.get('PRODUCTION_CFG','log_rel_path')+"/main.log"
    main_log          = open(main_log_filename,'r')
    
    
    for line in main_log:
        if line.rstrip('\n') == "BACKUP : OK":

            prod_status = True
    
    main_log.close()
    return prod_status



def is_hpss_path(arg0):

    is_hpss = False
    debug  = True

    if debug:
        print("INFO  : [%s] : check input path origin (%s)"%(is_hpss_path.__name__,arg0) )

    if arg0.split('/')[1] == "sps":
#        print("File from sps...")
        is_hpss = False
    elif arg0.split('/')[1] == "hpss":
#        print("File from hpss...")
        is_hpss = True
    else:
        print("\033[91mERROR\033[00m : [%s] : Not designed to get file from other path than 'sps' OR 'hpss'")
        sys.exit(1)
    
    return is_hpss
