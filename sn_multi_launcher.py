#!/usr/local/python/python-2.7/bin/python


from datetime import date, datetime
import time
import sys
import os
import subprocess
import glob
import ConfigParser


### Simulation launcher
import cc_job_submitter
import sn_tree_mgr

#execfile("sn_simu_env.py")



def prepare_fill_db(arg1=None,arg2=None,arg3=None):

    debug=True
    function_name="prepare_fill_db"

    if debug:
       print ("\nDEBUG : [%s] Enter in function"%function_name)
       print ("DEBUG : --------------------------------------")


    CURRENT_OUTPUT_PATH = arg1
    simu_file_name      = arg2
    db_input            = arg3



    check_filename=CURRENT_OUTPUT_PATH+sys_rel_path+launcher_rel_path+JOB_CHECKER
    db_file=CURRENT_OUTPUT_PATH+sys_rel_path+log_rel_path+"/"+"db.log"
    os.system("chmod 777 %s" % check_filename)
    check_file = open(check_filename,"a")


    check_file.write("db_request_file='%s' \n" %db_file)
    check_file.write("db_input='%s' \n" %db_input)

    check_file.write("\n\
if running_iterator == 0 and error_iterator == 0 and success_iterator == iterator:\n\
    print ('INFO  : DB updated with : %s' % db_input)\n\
    log_file.write('INFO  : DB updated with : %s'%db_input) \n\
    # client = pyAMI.client.Client('supernemo')\n\
    # client.execute(db_input)\n\
    db_request = open(db_request_file,'w')\n\
    db_request.write(db_input)\n\
else:\n\
    print ('Simulation not finished ! Can not update supernemo DB')\n\
    log_file.write('WARNING : Simulation is not finished ! Can not update SuperNEMO DB')\n")


    check_file.close()
    os.system("chmod 555 %s" % check_filename)

def prepare_reco_launcher(arg0=None,arg1=None):


    debug=True
    function_name="prepare_reco_launcher"
    snemo_cfg = ConfigParser.ConfigParser()
    snemo_cfg.read('snemo.cfg')

    
    if debug:
        print ("DEBUG : --------------------------------------")
        print ("DEBUG : [%s] : Enter in function using  (%s,%s) "%(function_name,arg0,arg1) )

  
    
    CURRENT_OUTPUT_PATH = arg0
    LAUNCH_PATH=CURRENT_OUTPUT_PATH+snemo_cfg.get('PRODUCTION_CFG','sys_rel_path')+snemo_cfg.get('PRODUCTION_CFG','launcher_rel_path')
    OUT_DATA_PATH=CURRENT_OUTPUT_PATH+snemo_cfg.get('PRODUCTION_CFG','output_rel_path')
    LOG_PATH=CURRENT_OUTPUT_PATH+snemo_cfg.get('PRODUCTION_CFG','sys_rel_path')+snemo_cfg.get('PRODUCTION_CFG','log_rel_path')
    SW_PATH=snemo_cfg.get('SW_CFG','sw_path')
    sw_file=snemo_cfg.get('SW_CFG','sw_snemo_reconstruction')
    reco_conf_filename = snemo_cfg.get('RECO_CFG','reconstruction_conf')
    reco_file_name="file"


    #TMP STUFF
    INPUT_DATA_PATH  = arg1+snemo_cfg.get('PRODUCTION_CFG','output_rel_path')

    print("DEBUG : [%s] : Input data path : %s "%(function_name,INPUT_DATA_PATH))

    from_hpss_status = False
    from_hpss_status = sn_tree_mgr.is_hpss_path(INPUT_DATA_PATH)
    
    if from_hpss_status == True:
        if debug: 
            print("DEBUG : [%s] : Input data are from HPSS "%function_name)
        cp_cmd='xrdcp root://ccxroot:1999//'
    else:
        if debug: 
            print("DEBUG : [%s] : Inpu data are NOT from HPSS "%function_name)
        cp_cmd='cp '

    if debug:
        print("DEBUG : [%s] : Check list of input SD files "%function_name)
    

    if from_hpss_status == False:
        list_of_sd_files = os.listdir(INPUT_DATA_PATH)
    else:
        list_of_sd_files = os.popen("rfdir %s | grep brio | tr -s ' ' | cut --d=' ' --f=9"%INPUT_DATA_PATH).readlines()
        

    list_of_brio=[]
    for el in list_of_sd_files:
        clean_el=el.rstrip("\n")
        if clean_el.endswith('.brio'):
            list_of_brio.append(clean_el)
         

    if not list_of_brio:
        print("\033[91mERROR\033[00m : [%s] : No input SD files in :%s"%(function_name,INPUT_DATA_PATH))
        sys.exit(1)

    if debug:
        print ("DEBUG : [%s] : Prepare stuff for list of input files : \n%s"%(function_name,list_of_brio))
        
    JOB_CHECKER="/check.py"




    try:
        log_file_name=LOG_PATH+"/main"+".log"
        check_filename=LAUNCH_PATH+JOB_CHECKER
        check_file = open(check_filename,"w")
        check_file.write("#!/usr/local/python/python-2.7/bin/python\n\n")
        check_file.write("# Author  : Y.Lemiere \n")
        check_file.write("# Date    : 2016/07 \n")
        check_file.write("# Contact : lemiere@lpccaen.in2p3.fr\n")
        check_file.write("# Object  : SuperNEMO Simulation check\n")

        check_file.write("# Create this file automatically from %s at %s \n\n" % (function_name,datetime.now()))
        check_file.write("import sys\nimport tarfile\nimport os\n\n\n")
        check_file.write("# import pyAMI.client\n")
        check_file.write("# import pyAMI_supernemo\n\n\n")

        check_file.write("WORKING_PATH=os.environ['WORKING_PATH']\n")
        check_file.write("iterator=0 \nrunning_iterator=0\nerror_iterator=0\nsuccess_iterator=0\n\n")
        
        iterator = 0
        for in_file in list_of_brio:

            if debug:
                print ("DEBUG : [%s] : Prepare shell script file #%s"%(function_name,iterator))
            
            iterator = in_file.split("_")[1].split(".")[0]
            
            uniq_launch_filename = LAUNCH_PATH+"/launch_"+reco_file_name+"_"+str(iterator)+".sh"
            uniq_launch =  open(uniq_launch_filename,"w")
            
            uniq_short_log_filename = reco_file_name+"_"+str(iterator)+".log"
            uniq_log                = open(LOG_PATH+"/"+uniq_short_log_filename,"w")
            
            

            begin_input_filename    = in_file.split("_")[0]
            end_input_filename    = in_file.split("_")[1]
        
            
            short_output_filename = reco_file_name+"_"+end_input_filename
            job_name="job_"+reco_file_name+"_"+str(iterator)
            
            uniq_log.write("INFO : Prepare script using ${INPUT_DATA_PATH}\n")
            uniq_log.write("INFO : Up to now, ${INPUT_DATA_PATH}=%s \n"%INPUT_DATA_PATH)
            uniq_log.write("INFO : 'export WORKING_PATH=%s' \n"%CURRENT_OUTPUT_PATH)
            uniq_log.write("INFO : 'export SW_PATH=%s' \n"%SW_PATH)
            uniq_log.write("INFO : Ready for uniq job submission, so let's go !\n")
            uniq_log.close()
            

            check_file.write("iterator=iterator+1\n")
            check_file.write("job_name='%s' \n" %job_name)
            check_file.write("uniq_log_filename=WORKING_PATH+'/%s/%s' \n" %(snemo_cfg.get('PRODUCTION_CFG','sys_rel_path')+snemo_cfg.get('PRODUCTION_CFG','log_rel_path'),uniq_short_log_filename))
            check_file.write("result=os.system('qstat -j %s > /dev/null 2>&1' % job_name)\n")
            check_file.write("\
if result != 0:\n\
   print ('INFO  : %s finished' % job_name)\n\
else:\n\
   print ('WARNING : %s not yet finished' % job_name)\n\
   running_iterator=running_iterator+1\n\n\
")

            check_file.write("grep_result=os.system('grep successfully %s > /dev/null' % uniq_log_filename)\n")
            check_file.write("\
if grep_result != 0:\n\
   print ('WARNING  : %s not running but no sucess' % job_name)\n\
   #running_iterator=running_iterator+1\n\
else:\n\
   print ('INFO  : %s  successfully finished' % job_name)\n\
   success_iterator=success_iterator+1\n\
")

            check_file.write("grep_result=os.system('grep failed %s > /dev/null' % uniq_log_filename)\n")
            check_file.write("\
if grep_result != 0:\n\
   print ('INFO  : %s no error found' % job_name)\n\
   #running_iterator=running_iterator+1\n\
else:\n\
   print ('WARNING : %s  FAILED' % job_name)\n\
   error_iterator=error_iterator+1\n\n\
")



            
            uniq_launch.write("#!/bin/bash\n")
            uniq_launch.write("# Author  : Y.Lemiere\n")
            uniq_launch.write("# Date    : %s\n\n" % datetime.now())
            uniq_launch.write("# Contact : lemiere@lpccaen.in2p3.fr\n")
            uniq_launch.write("# Object  : SuperNEMO Uniq Simulation launcher\n\n")
            
            uniq_launch.write("%s%s/%s .\n"%(cp_cmd,INPUT_DATA_PATH,in_file))
            uniq_launch.write("if [ $? -eq 0 ];\nthen\n echo 'INFO : successfully copied on batch'>>  ${WORKING_PATH}/%s/%s\nelse\n  echo 'ERROR : copy failed'>>  ${WORKING_PATH}/%s/%s\n exit 1\nfi\n" % (snemo_cfg.get('PRODUCTION_CFG','sys_rel_path')+snemo_cfg.get('PRODUCTION_CFG','log_rel_path'),uniq_short_log_filename,snemo_cfg.get('PRODUCTION_CFG','sys_rel_path')+snemo_cfg.get('PRODUCTION_CFG','log_rel_path'),uniq_short_log_filename))


            uniq_launch.write('if [ "x$WORKING_PATH" != "x" ];\nthen\n echo "INFO : WORKING_PATH exist : " ${WORKING_PATH} >>  ${WORKING_PATH}/%s/%s\nelse\n  echo "ERROR : WORKING_PATH is empty"\n exit 1\nfi\n'% (snemo_cfg.get('PRODUCTION_CFG','sys_rel_path')+snemo_cfg.get('PRODUCTION_CFG','log_rel_path'),uniq_short_log_filename))

            uniq_launch.write('if [ "x$SW_PATH" != "x" ];\nthen\n echo "INFO : SW_PATH exist : " ${SW_PATH} >>  ${WORKING_PATH}/%s/%s\nelse\n  echo "ERROR : SW_PATH is empty"\n exit 1\nfi\n' % (snemo_cfg.get('PRODUCTION_CFG','sys_rel_path')+snemo_cfg.get('PRODUCTION_CFG','log_rel_path'),uniq_short_log_filename))

            
            uniq_launch.write("ls -rthla >> ${WORKING_PATH}/%s/%s"%(snemo_cfg.get('PRODUCTION_CFG','sys_rel_path')+snemo_cfg.get('PRODUCTION_CFG','log_rel_path'),uniq_short_log_filename))




            uniq_launch.write("\n\n#*************** COMMAND **************\n")
            uniq_launch.write('${SW_PATH}/%s -i %s/%s -o %s -p %s \n' % (sw_file,INPUT_DATA_PATH,in_file,short_output_filename,reco_conf_filename))
            
            uniq_launch.write("if [ $? -eq 0 ];\nthen\n echo 'INFO : successfully finished'>>  ${WORKING_PATH}/%s/%s\nelse\n  echo 'ERROR : reconstruction failed'>>  ${WORKING_PATH}/%s/%s\n exit 1\nfi\n" % (snemo_cfg.get('PRODUCTION_CFG','sys_rel_path')+snemo_cfg.get('PRODUCTION_CFG','log_rel_path'),uniq_short_log_filename,snemo_cfg.get('PRODUCTION_CFG','sys_rel_path')+snemo_cfg.get('PRODUCTION_CFG','log_rel_path'),uniq_short_log_filename))
            uniq_launch.write("#*************** END OF CMD **************\n\n")
            
            uniq_launch.write("mv %s ${WORKING_PATH}/%s/%s \n\n" % (short_output_filename,snemo_cfg.get('PRODUCTION_CFG','output_rel_path'),short_output_filename))
            uniq_launch.write("if [ $? -eq 0 ];\nthen\n echo 'INFO : data copy done'>>  ${WORKING_PATH}/%s/%s\nelse\n  echo 'ERROR : data copy failed'>>  ${WORKING_PATH}/%s/%s\n exit 1\nfi\n\n" % (snemo_cfg.get('PRODUCTION_CFG','sys_rel_path')+snemo_cfg.get('PRODUCTION_CFG','log_rel_path'),uniq_short_log_filename,snemo_cfg.get('PRODUCTION_CFG','sys_rel_path')+snemo_cfg.get('PRODUCTION_CFG','log_rel_path'),uniq_short_log_filename))


            uniq_launch.write("python %s \n"%check_filename)
            uniq_launch.write("echo queue : $QUEUE\n")
            uniq_launch.write("echo job : $JOB_ID\n")
            uniq_launch.write("cat /proc/cpuinfo | grep -m 1 bogomips\n")
            
            uniq_launch.close()
            os.system("chmod 555 %s" % uniq_launch_filename)
            

        check_file.write("print('INFO  : running : %s / %s' % (running_iterator,iterator))\n")
        check_file.write("print('INFO  : error   : %s /%s'  %(error_iterator,iterator))\n")
        check_file.write("print('INFO  : success   : %s /%s'  %(success_iterator,iterator))\n\n")

        check_file.write("log_filename='%s' \n" % (log_file_name))
        check_file.write("log_file=open(log_filename,'a') \n")
        check_file.write("log_file.write('INFO  : running :  %s / %s \\n'  %(running_iterator,iterator)) \n")
        check_file.write("log_file.write('INFO  : error :  %s / %s \\n'    %(error_iterator,iterator))\n")
        check_file.write("log_file.write('INFO  : success :  %s / %s \\n'  %(success_iterator,iterator))\n\n")
        db_file=snemo_cfg.get('PRODUCTION_CFG','sys_rel_path')+snemo_cfg.get('PRODUCTION_CFG','log_rel_path')+"/"+"db.log"
        new_db_file=snemo_cfg.get('PRODUCTION_CFG','sys_rel_path')+snemo_cfg.get('PRODUCTION_CFG','log_rel_path')+"/"+"db2.log"

        
        check_file.write("\n\
if success_iterator == iterator:\n\
    log_file.write('BACKUP : OK\\n')\n\
    db_request_file=WORKING_PATH+'/%s'\n\
    new_db_request_file=WORKING_PATH+'/%s'\n" %(db_file,new_db_file))
        
        check_file.write("\n\
    val1='unchecked'\n\
    val2='checked'\n")

        check_file.write("\n\
    open(new_db_request_file,'w').write(\n\
       open(db_request_file).read().replace(val1,val2))\n\n")
        check_file.write("\n\
    os.system('mv %s %s'%(new_db_request_file,db_request_file))\n\n")
        check_file.write("\n\
    log_file.write('INFO  : db file updated')\n")
            
                
        check_file.close()
        os.system("chmod 555 %s" % check_filename)
        
    except:
        print("\033[91mERROR\033[00m : [%s] : Do not create sh script successfully"%function_name)
        sys.exit(1)
        
    if debug:
        print ("DEBUG : --------------------------------------")
        
def prepare_simu_launcher(arg1=None,arg2=None,arg3=None,arg4=None, arg5=None, arg6=None):

    debug=True
    function_name="prepare_simu_launcher"
    snemo_cfg = ConfigParser.ConfigParser()
    snemo_cfg.read('snemo.cfg')

    if debug:
        print ("DEBUG : --------------------------------------")
        print ("DEBUG : [%s] : Enter in function"%function_name)



    #Argument from sn_simu_mgr_next.py
    nb_of_file          = arg1
    nb_event            = arg2
    experiment_name     = arg3
    CURRENT_OUTPUT_PATH = arg4
    simu_file_name      = arg5
    variant             = arg6

    SW_PATH=snemo_cfg.get('SW_CFG','sw_path')
    sw_file=snemo_cfg.get('SW_CFG','sw_snemo_simulation')

    
    if debug:
        print("DEBUG : [%s] : nb_of_file          : %s" % (function_name,nb_of_file))
        print("DEBUG : [%s] : nb_event            : %s" % (function_name,nb_event))
        print("DEBUG : [%s] : experiment_name     : %s" % (function_name,experiment_name))
        print("DEBUG : [%s] : CURRENT_OUTPUT_PATH : %s" % (function_name,CURRENT_OUTPUT_PATH))
        print("DEBUG : [%s] : simu_file_name      : %s" % (function_name,simu_file_name))
        print("DEBUG : [%s] : variant             : %s" % (function_name,variant))

        ### To change


    ###  ./config direactory
    MAIN_CONFIG_PATH=CURRENT_OUTPUT_PATH+snemo_cfg.get('PRODUCTION_CFG','config_rel_path')
    SEEDS_PATH= MAIN_CONFIG_PATH+snemo_cfg.get('PRODUCTION_CFG','seed_rel_path')
    VARIANT_PATH=MAIN_CONFIG_PATH+snemo_cfg.get('PRODUCTION_CFG','variant_rel_path')

    CONF_PATH=MAIN_CONFIG_PATH+snemo_cfg.get('PRODUCTION_CFG','conf_rel_path')
    
    #### ./.sys directory
    CURRENT_SYS_PATH=CURRENT_OUTPUT_PATH+snemo_cfg.get('PRODUCTION_CFG','sys_rel_path')
    LOG_PATH=CURRENT_SYS_PATH+snemo_cfg.get('PRODUCTION_CFG','log_rel_path')
    



    LAUNCHER_PATH=CURRENT_SYS_PATH+snemo_cfg.get('PRODUCTION_CFG','launcher_rel_path')
    #### ./output directory
    CURRENT_OUTDATA_PATH  = CURRENT_OUTPUT_PATH+snemo_cfg.get('PRODUCTION_CFG','output_rel_path')
    CURRENT_METADATA_PATH = CURRENT_OUTDATA_PATH

    JOB_CHECKER="/check.py"

    
    try:
        log_file_name=LOG_PATH+"/main"+".log"
        short_log_file_name=snemo_cfg.get('PRODUCTION_CFG','sys_rel_path')+snemo_cfg.get('PRODUCTION_CFG','log_rel_path')+"/main"+".log"
        log_file = open(log_file_name,"a")
        log_file.write("INFO : Up to now, ${WORKING_PATH}=%s \n"%CURRENT_OUTPUT_PATH)

        check_filename=LAUNCHER_PATH+JOB_CHECKER
        short_check_filename=snemo_cfg.get('PRODUCTION_CFG','sys_rel_path')+snemo_cfg.get('PRODUCTION_CFG','launcher_rel_path')+JOB_CHECKER
        check_file = open(check_filename,"w")

        check_file.write("#!/usr/local/python/python-2.7/bin/python\n\n")
        check_file.write("# Author  : Y.Lemiere \n")
        check_file.write("# Date    : 2016/07 \n")
        check_file.write("# Contact : lemiere@lpccaen.in2p3.fr\n")
        check_file.write("# Object  : SuperNEMO Simulation check\n")

        check_file.write("# Create this file automatically from %s at %s \n\n" % (function_name,datetime.now()))
        check_file.write("import sys\nimport tarfile\nimport os\n\n\n")
        check_file.write("# import pyAMI.client\n")
        check_file.write("# import pyAMI_supernemo\n\n\n")

        check_file.write("WORKING_PATH=os.environ['WORKING_PATH']\n")
        check_file.write("iterator=0 \nrunning_iterator=0\nerror_iterator=0\nsuccess_iterator=0\n\n")


        if debug:
            print("DEBUG : [%s] : Ready to loop for shell script production"%function_name)

    # create individual script per simulation file production
            iterator=0
            for iterator in range(int(nb_of_file)):
                #         ## To change
                log_file.write("DEBUG : [%s] : create launcher for file %s/%s\n"%(function_name,iterator,nb_of_file))

                ###### ici
                simu_file_name="file"
                uniq_log_filename = LOG_PATH+"/"+simu_file_name+"_"+str(iterator)+".log"
                uniq_short_log_filename = snemo_cfg.get('PRODUCTION_CFG','sys_rel_path')+snemo_cfg.get('PRODUCTION_CFG','log_rel_path')+"/"+simu_file_name+"_"+str(iterator)+".log"


                uniq_short_launch_filename = "/launch_"+simu_file_name+"_"+str(iterator)+".sh"
                uniq_launch_filename = LAUNCHER_PATH+uniq_short_launch_filename

                uniq_config_launch_filename= CONF_PATH+"/launch_"+simu_file_name+"_"+str(iterator)+".conf"
                uniq_short_config_filename= snemo_cfg.get('PRODUCTION_CFG','config_rel_path')+snemo_cfg.get('PRODUCTION_CFG','conf_rel_path')+"/launch_"+simu_file_name+"_"+str(iterator)+".conf"
                uniq_log    =  open(uniq_log_filename,"w")
                uniq_launch =  open(uniq_launch_filename,"w")
                uniq_config =  open(uniq_config_launch_filename,"w")

                seeds_list_file=SEEDS_PATH+"/__bxg4_seeds-runs.lis"
                seeds_conf_file=None

        # Obtain dedicated seed file per simulation file production
                list_seeds = open(seeds_list_file,"r")
                for ligne in list_seeds:
                    seed_number, seed_file = ligne.split()
                    if int(seed_number) == iterator:
                        seeds_conf_file=seed_file
                list_seeds.close()
        # End of seed file

        #Input config file for flsimuate configuration
                uniq_config.write("")
                uniq_config.write("# Author  : Y.Lemiere \n")
                uniq_config.write("# Contact : lemiere@lpccaen.in2p3.fr\n")
                uniq_config.write("# Object  : SuperNEMO Simulation configuration\n\n")
                uniq_config.write("# Create this file automatically by %s at %s \n\n" % (function_name,datetime.now()))
                uniq_config.write("#@description Main flsimulate configuration script\n\n")

                uniq_config.write('[name="flsimulate" type="flsimulate::section"]\n')
                uniq_config.write('#@config Basic system setup\n\n')

                uniq_config.write('#@description Number of events to simulate\n')
                uniq_config.write('numberOfEvents : integer = %s \n\n' % nb_event)

                uniq_config.write('#@description Progression rate on simulated events\n')
                uniq_config.write('moduloEvents   : integer = 1000000 \n\n')

                uniq_config.write('#@description Activate simulation\n')
                uniq_config.write('doSimulation : boolean = true\n\n')

                uniq_config.write('[name="flsimulate.simulation" type="flsimulate::section"]\n')
                uniq_config.write('#@config Simulation setup\n\n')

                uniq_config.write('#@description URN of the simulation setup (registered)\n')
                uniq_config.write('simulationSetupUrn : string = "%s"\n\n'%snemo_cfg.get('SIMU_CFG','urn_blessed_snemo'))

                uniq_config.write('#@description File with input seeds for embedded random number generators\n')
                uniq_config.write('rngSeedFile : string as path = "@sys_path:config.d/seeds.d/%s"\n\n'%seeds_conf_file)

                uniq_config.write('[name="flsimulate.variantService" type="flsimulate::section"]\n')
                uniq_config.write('#@config Variants setup\n\n')

                uniq_config.write('#@description Input variant profile configuration file (manual)\n')
                uniq_config.write('profile : string as path = "@sys_path:config.d/variant.d/%s"\n\n'%variant)

                uniq_config.write('[name="flsimulate.services" type="flsimulate::section"]\n')
                uniq_config.write('#@config Services setup\n\n')
                uniq_config.close()
        #End of flsimulate_next config file preparation


                short_output_filename = simu_file_name+"_"+str(iterator)+".brio"
                short_metadata_filename = simu_file_name+"_"+str(iterator)+".meta"

                uniq_output_filename   = snemo_cfg.get('PRODUCTION_CFG','output_rel_path')+"/"+short_output_filename
                uniq_metadata_filename = snemo_cfg.get('PRODUCTION_CFG','output_rel_path')+"/"+short_metadata_filename

        #Shell script for job submission
                uniq_launch.write("#!/bin/bash\n")
                uniq_launch.write("# Author  : Y.Lemiere\n")
                uniq_launch.write("# Date    : %s\n\n" % datetime.now())
                uniq_launch.write("# Contact : lemiere@lpccaen.in2p3.fr\n")
                uniq_launch.write("# Object  : SuperNEMO Uniq Simulation launcher\n\n")

                uniq_launch.write('if [ "x$WORKING_PATH" != "x" ];\nthen\n echo "INFO : WORKING_PATH exist : " ${WORKING_PATH} >>  ${WORKING_PATH}/%s\nelse\n  echo "ERROR : WORKING_PATH is empty"\n exit 1\nfi\n' % (uniq_short_log_filename))

                uniq_launch.write('if [ "x$SW_PATH" != "x" ];\nthen\n echo "INFO : SW_PATH exist : " ${SW_PATH} >>  ${WORKING_PATH}/%s\nelse\n  echo "ERROR : SW_PATH is empty"\n exit 1\nfi\n' % (uniq_short_log_filename))


                #uniq_launch.write("WORKING_PATH=$1 \n")
                uniq_launch.write("date >>  ${WORKING_PATH}/%s " %uniq_short_log_filename)
                uniq_launch.write("\n\n#*************** COMMAND **************\n")

                uniq_launch.write('${SW_PATH}/%s  -d "sys_path.resources@${WORKING_PATH}" -o %s -c @sys_path:%s -m %s \n' % (sw_file,short_output_filename,uniq_short_config_filename,short_metadata_filename))

                uniq_launch.write("if [ $? -eq 0 ];\nthen\n echo 'INFO : successfully finished'>>  ${WORKING_PATH}/%s\nelse\n  echo 'ERROR : simulation failed'>>  ${WORKING_PATH}/%s\n exit 1\nfi\n" % (uniq_short_log_filename,uniq_short_log_filename))
                uniq_launch.write("#*************** END OF CMD **************\n\n")

                uniq_launch.write("mv %s ${WORKING_PATH}/%s \n\n" % (short_output_filename,uniq_output_filename) )
                uniq_launch.write("if [ $? -eq 0 ];\nthen\n echo 'INFO : data copy done'>>  ${WORKING_PATH}/%s\nelse\n  echo 'ERROR : data copy failed'>>  ${WORKING_PATH}/%s\n exit 1\nfi\n\n" % (uniq_short_log_filename,uniq_short_log_filename))

                uniq_launch.write("mv %s ${WORKING_PATH}/%s \n\n" % (short_metadata_filename,uniq_metadata_filename) )
                uniq_launch.write("if [ $? -eq 0 ];\nthen\n echo 'INFO : metadata copy done'>>  ${WORKING_PATH}/%s\nelse\n  echo 'ERROR : metadata copy failed'>> ${WORKING_PATH}/%s\n exit 1\nfi\n\n" % (uniq_short_log_filename,uniq_short_log_filename))

                uniq_launch.write("python ${WORKING_PATH}/%s \n"%short_check_filename)
                uniq_launch.write("echo queue : $QUEUE\n")
                uniq_launch.write("echo job : $JOB_ID\n")
                uniq_launch.write("cat /proc/cpuinfo | grep -m 1 bogomips\n")

                uniq_launch.close()
                os.system("chmod 555 %s" % uniq_launch_filename)
                #End of Shell script
                job_name="job_"+simu_file_name+"_"+str(iterator)
                #job_path=CURRENT_SYS_PATH
                log_file.write("INFO : [%s] : JOB %s job_name %s uniq_launch_filename %s\n"%(function_name,iterator,job_name,uniq_short_launch_filename))




                uniq_log.write("INFO : Prepare script using ${WORKING_PATH}\n")
                uniq_log.write("INFO : 'export WORKING_PATH=%s \n"%CURRENT_OUTPUT_PATH)
                uniq_log.write("INFO : 'export SW_PATH=%s' \n"%SW_PATH)
                uniq_log.write("INFO : Ready for uniq job submission, so let's go !\n")
                uniq_log.close()



                check_file.write("iterator=iterator+1\n")
                check_file.write("job_name='%s' \n" %job_name)
                check_file.write("uniq_log_filename=WORKING_PATH+'/%s' \n" %(uniq_short_log_filename))
                check_file.write("result=os.system('qstat -j %s > /dev/null 2>&1' % job_name)\n")
                check_file.write("\
if result != 0:\n\
   print ('INFO  : %s finished' % job_name)\n\
else:\n\
   print ('WARNING : %s not yet finished' % job_name)\n\
   running_iterator=running_iterator+1\n\n\
")

                check_file.write("grep_result=os.system('grep successfully %s > /dev/null' % uniq_log_filename)\n")
                check_file.write("\
if grep_result != 0:\n\
   print ('WARNING  : %s not running but no sucess' % job_name)\n\
   #running_iterator=running_iterator+1\n\
else:\n\
   print ('INFO  : %s  successfully finished' % job_name)\n\
   success_iterator=success_iterator+1\n\
")

                check_file.write("grep_result=os.system('grep failed %s > /dev/null' % uniq_log_filename)\n")
                check_file.write("\
if grep_result != 0:\n\
   print ('INFO  : %s no error found' % job_name)\n\
   #running_iterator=running_iterator+1\n\
else:\n\
   print ('WARNING : %s  FAILED' % job_name)\n\
   error_iterator=error_iterator+1\n\n\
")


        log_file.write("DEBUG : [%s] : All uniq launcher done successfully "%function_name)

        check_file.write("print('INFO  : running : %s / %s' % (running_iterator,iterator))\n")
        check_file.write("print('INFO  : error   : %s /%s'  %(error_iterator,iterator))\n")
        check_file.write("print('INFO  : success   : %s /%s'  %(success_iterator,iterator))\n\n")

        check_file.write("log_filename=WORKING_PATH+'%s' \n" % (short_log_file_name))
        check_file.write("log_file=open(log_filename,'a') \n")
        check_file.write("log_file.write('INFO  : running :  %s / %s \\n'  %(running_iterator,iterator)) \n")
        check_file.write("log_file.write('INFO  : error :  %s / %s \\n'    %(error_iterator,iterator))\n")
        check_file.write("log_file.write('INFO  : success :  %s / %s \\n'  %(success_iterator,iterator))\n\n")


  #   #### To correct with
#         line='UpdateElement -project="supernemo" -processingStep="production" -entity="demo"'
#         line+=' -experiment="'+experiment_name+'"'
#     #line+=' --simu_id="'+simu_file_name+"_"+str(iterator)+'"'
#         line+=' -simu_id="'+simu_file_name+'"'
#         line+=' -separator=, -updateField="checking_status"'
#         line+=' -updateValue="checked"'

#     #%s.write('INFO  : DB updated with')\n\
#         check_file.write("line='%s'\n" % line)
#         check_file.write("\n\
# if running_iterator == 0 and error_iterator == 0 and success_iterator == iterator:\n\
#     print ('INFO  : DB updated with : %s' % line)\n\
#     log_file.write('INFO  : DB updated with : %s'%line) \n\
#     client = pyAMI.client.Client('supernemo')\n\
#     client.execute(line)\n\
# else:\n\
#     print ('Simulation not finished ! Can not update supernemo DB')\n\
#     log_file.write('WARNING : Simulation is not finished ! Can not update SuperNEMO DB')\n")

        db_file=snemo_cfg.get('PRODUCTION_CFG','sys_rel_path')+snemo_cfg.get('PRODUCTION_CFG','log_rel_path')+"/"+"db.log"
        new_db_file=snemo_cfg.get('PRODUCTION_CFG','sys_rel_path')+snemo_cfg.get('PRODUCTION_CFG','log_rel_path')+"/"+"db2.log"
        check_file.write("\n\
if success_iterator == iterator:\n\
    log_file.write('BACKUP : OK\\n')\n\
    db_request_file=WORKING_PATH+'/%s'\n\
    new_db_request_file=WORKING_PATH+'/%s'\n" %(db_file,new_db_file))
        check_file.write("\n\
    val1='unchecked'\n\
    val2='checked'\n")

        check_file.write("\n\
    open(new_db_request_file,'w').write(\n\
       open(db_request_file).read().replace(val1,val2))\n\n")
        check_file.write("\n\
    os.system('mv %s %s'%(new_db_request_file,db_request_file))\n\n")
        check_file.write("\n\
    log_file.write('INFO  : db file updated')\n")

        

        check_file.close()
        os.system("chmod 555 %s" % check_filename)

    except:
        print("\033[91mERROR\033[00m : [%s] : Do not create sh script successfully"%function_name)
        sys.exit(1)

    
    if debug:
        print ("DEBUG : --------------------------------------")

