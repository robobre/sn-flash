#!/usr/local/python/python-2.7/bin/python


from datetime import date, datetime
import time
import sys
import os
import subprocess
import glob


### Simulation launcher
import cc_job_submitter

execfile("sn_simu_env.py")



def prepare_fill_db(arg1=None,arg2=None,arg3=None):

    debug=True
    function_name="prepare_fill_db"
    if debug:
       print ("\nDEBUG : Enter in %s function"%function_name)
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
    client = pyAMI.client.Client('supernemo')\n\
    client.execute(db_input)\n\
    db_request = open(db_request_file,'w')\n\
    db_request.write(db_input)\n\
else:\n\
    print ('Simulation not finished ! Can not update supernemo DB')\n\
    log_file.write('WARNING : Simulation is not finished ! Can not update SuperNEMO DB')\n")


    check_file.close()
    os.system("chmod 555 %s" % check_filename)



def prepare_launcher(arg1=None,arg2=None,arg3=None,arg4=None, arg5=None, arg6=None):

    debug=True
    function_name="prepare_launcher"


    if debug:
       print ("\nDEBUG : Enter in %s function"%function_name)
       print ("DEBUG : --------------------------------------")


    #Argument from sn_simu_mgr_next.py
    nb_of_file          = arg1
    nb_event            = arg2
    experiment_name     = arg3
    CURRENT_OUTPUT_PATH = arg4
    simu_file_name      = arg5
    variant             = arg6

    if debug:
        print("DEBUG : nb_of_file          : %s" % nb_of_file)
        print("DEBUG : nb_event            : %s" % nb_event)
        print("DEBUG : experiment_name     : %s" % experiment_name)
        print("DEBUG : CURRENT_OUTPUT_PATH : %s" % CURRENT_OUTPUT_PATH)
        print("DEBUG : simu_file_name      : %s" % simu_file_name)
        print("DEBUG : variant             : %s" % variant)

        ### To change


        ###  ./config direactory
    MAIN_CONFIG_PATH=CURRENT_OUTPUT_PATH+config_rel_path
    SEEDS_PATH= MAIN_CONFIG_PATH+seed_rel_path
    VARIANT_PATH=MAIN_CONFIG_PATH+variant_rel_path

    CONF_PATH=MAIN_CONFIG_PATH+conf_rel_path
    REL_CONF_PATH=config_rel_path+conf_rel_path
        #### ./.sys directory
    CURRENT_SYS_PATH=CURRENT_OUTPUT_PATH+sys_rel_path

    LOG_PATH=CURRENT_SYS_PATH+log_rel_path
    REL_LOG_PATH=sys_rel_path+log_rel_path



    LAUNCHER_PATH=CURRENT_SYS_PATH+launcher_rel_path
    #### ./output directory
    CURRENT_OUTDATA_PATH=CURRENT_OUTPUT_PATH+output_rel_path
    CURRENT_METADATA_PATH=CURRENT_OUTPUT_PATH+output_rel_path


    try:
        log_file_name=LOG_PATH+"/main"+".log"
        short_log_file_name=REL_LOG_PATH+"/main"+".log"
        log_file = open(log_file_name,"a")
        log_file.write("INFO : Up to now, ${RUN_SIMU_PATH}=%s \n"%CURRENT_OUTPUT_PATH)

        check_filename=LAUNCHER_PATH+JOB_CHECKER
        short_check_filename=sys_rel_path+launcher_rel_path+JOB_CHECKER
        check_file = open(check_filename,"w")

        check_file.write("#!/usr/local/python/python-2.7/bin/python\n\n")
        check_file.write("# Author  : Y.Lemiere \n")
        check_file.write("# Date    : 2016/07 \n")
        check_file.write("# Contact : lemiere@lpccaen.in2p3.fr\n")
        check_file.write("# Object  : SuperNEMO Simulation check\n")

        check_file.write("# Create this file automatically from %s at %s \n\n" % (function_name,datetime.now()))
        check_file.write("import sys\nimport tarfile\nimport os\n\n\n")
        check_file.write("import pyAMI.client\n")
        check_file.write("import pyAMI_supernemo\n\n\n")

        check_file.write("RUN_SIMU_PATH=os.environ['RUN_SIMU_PATH']\n")
        check_file.write("iterator=0 \nrunning_iterator=0\nerror_iterator=0\nsuccess_iterator=0\n\n")


        if debug:
            print("DEBUG : %s : Ready to loop for shell script production"%function_name)

    # create individual script per simulation file production
            iterator=0
            for iterator in range(int(nb_of_file)):
                #         ## To change
                log_file.write("DEBUG : %s : create launcher for file %s/%s\n"%(function_name,iterator,nb_of_file))

                ###### ici
                simu_file_name="file"
                uniq_log_filename = LOG_PATH+"/"+simu_file_name+"_"+str(iterator)+".log"
                uniq_short_log_filename = REL_LOG_PATH+"/"+simu_file_name+"_"+str(iterator)+".log"


                uniq_short_launch_filename = "/launch_"+simu_file_name+"_"+str(iterator)+".sh"
                uniq_launch_filename = LAUNCHER_PATH+uniq_short_launch_filename

                uniq_config_launch_filename= CONF_PATH+"/launch_"+simu_file_name+"_"+str(iterator)+".conf"
                uniq_short_config_filename= REL_CONF_PATH+"/launch_"+simu_file_name+"_"+str(iterator)+".conf"
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
                uniq_config.write('simulationSetupUrn : string = "%s"\n\n'%urn_blessed_snemo)

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

                uniq_output_filename = output_rel_path+"/"+short_output_filename
                uniq_metadata_filename = output_rel_path+"/"+short_metadata_filename

        #Shell script for job submission
                uniq_launch.write("#!/bin/bash\n")
                uniq_launch.write("# Author  : Y.Lemiere\n")
                uniq_launch.write("# Date    : %s\n\n" % datetime.now())
                uniq_launch.write("# Contact : lemiere@lpccaen.in2p3.fr\n")
                uniq_launch.write("# Object  : SuperNEMO Uniq Simulation launcher\n\n")

                uniq_launch.write("if [ -n '$RUN_SIMU_PATH' ];\nthen\n echo 'INFO : RUN_SIMU_PATH exist'>>  ${RUN_SIMU_PATH}/%s\nelse\n  echo 'ERROR : RUN_SIMU_PATH is empty'\n exit 1\nfi\n" % (uniq_short_log_filename))


                #uniq_launch.write("RUN_SIMU_PATH=$1 \n")
                uniq_launch.write("date >>  ${RUN_SIMU_PATH}/%s " %uniq_short_log_filename)
                uniq_launch.write("\n\n#*************** COMMAND **************\n")

                uniq_launch.write('%s%s  -d "sys_path.resources@${RUN_SIMU_PATH}" -o %s -c @sys_path:%s -m %s \n' % (SW_PATH,sw_snemo_simulation,short_output_filename,uniq_short_config_filename,short_metadata_filename))

                uniq_launch.write("if [ $? -eq 0 ];\nthen\n echo 'INFO : successfully finished'>>  ${RUN_SIMU_PATH}/%s\nelse\n  echo 'ERROR : simulation failed'>>  ${RUN_SIMU_PATH}/%s\n exit 1\nfi\n" % (uniq_short_log_filename,uniq_short_log_filename))
                uniq_launch.write("#*************** END OF CMD **************\n\n")

                uniq_launch.write("mv %s ${RUN_SIMU_PATH}/%s \n\n" % (short_output_filename,uniq_output_filename) )
                uniq_launch.write("if [ $? -eq 0 ];\nthen\n echo 'INFO : data copy done'>>  ${RUN_SIMU_PATH}/%s\nelse\n  echo 'ERROR : data copy failed'>>  ${RUN_SIMU_PATH}/%s\n exit 1\nfi\n\n" % (uniq_short_log_filename,uniq_short_log_filename))

                uniq_launch.write("mv %s ${RUN_SIMU_PATH}/%s \n\n" % (short_metadata_filename,uniq_metadata_filename) )
                uniq_launch.write("if [ $? -eq 0 ];\nthen\n echo 'INFO : metadata copy done'>>  ${RUN_SIMU_PATH}/%s\nelse\n  echo 'ERROR : metadata copy failed'>> ${RUN_SIMU_PATH}/%s\n exit 1\nfi\n\n" % (uniq_short_log_filename,uniq_short_log_filename))

                uniq_launch.write("python ${RUN_SIMU_PATH}/%s \n"%short_check_filename)
                uniq_launch.write("echo queue : $QUEUE\n")
                uniq_launch.write("echo job : $JOB_ID\n")

                uniq_launch.close()
                os.system("chmod 555 %s" % uniq_launch_filename)
                #End of Shell script
                job_name="job_"+simu_file_name+"_"+str(iterator)
                #job_path=CURRENT_SYS_PATH
                log_file.write("JOB %s job_name %s uniq_launch_filename %s\n"%(iterator,job_name,uniq_short_launch_filename))




                uniq_log.write("INFO : Prepare script using ${RUN_SIMU_PATH}\n")
                uniq_log.write("INFO : Up to now, ${RUN_SIMU_PATH}=%s \n"%CURRENT_OUTPUT_PATH)
                uniq_log.write("INFO : Ready for uniq job submission, so let's go !\n")
                uniq_log.close()



                check_file.write("iterator=iterator+1\n")
                check_file.write("job_name='%s' \n" %job_name)
                check_file.write("uniq_log_filename=RUN_SIMU_PATH+'/%s' \n" %(uniq_short_log_filename))
                check_file.write("result=os.system('qstat -j %s > /dev/null 2>&1' % job_name)\n")
                check_file.write("\
if result != 0:\n\
   print ('INFO  : %s simulation finished' % job_name)\n\
else:\n\
   print ('WARNING : %s simulation not finished' % job_name)\n\
   running_iterator=running_iterator+1\n\n\
")

                check_file.write("grep_result=os.system('grep successfully %s > /dev/null' % uniq_log_filename)\n")
                check_file.write("\
if grep_result != 0:\n\
   print ('WARNING  : %s simulation ended with error?' % job_name)\n\
   #running_iterator=running_iterator+1\n\
else:\n\
   print ('INFO  : %s  successfully finished' % job_name)\n\
   success_iterator=success_iterator+1\n\
")

                check_file.write("grep_result=os.system('grep failed %s > /dev/null' % uniq_log_filename)\n")
                check_file.write("\
if grep_result != 0:\n\
   print ('INFO  : %s simulation finished with no error' % job_name)\n\
   #running_iterator=running_iterator+1\n\
else:\n\
   print ('WARNING : %s  FAILED' % job_name)\n\
   error_iterator=error_iterator+1\n\n\
")


        log_file.write("DEBUG : %s : All uniq launcher done successfully "%function_name)

        check_file.write("print('INFO  : running : %s / %s' % (running_iterator,iterator))\n")
        check_file.write("print('INFO  : error   : %s /%s'  %(error_iterator,iterator))\n")
        check_file.write("print('INFO  : success   : %s /%s'  %(success_iterator,iterator))\n\n")

        check_file.write("log_filename=RUN_SIMU_PATH+'/%s' \n" % (short_log_file_name))
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



        check_file.close()
        os.system("chmod 555 %s" % check_filename)

    except:
        print("ERROR : %s : Do not create sh script successfully"%function_name)
        sys.exit(1)

    #log_file.write("INFO : Prepare launcher finished, ready to process")
    if debug:
        print ("DEBUG : --------------------------------------")
#log_file.close()
#     os.system("chmod 755 %s" % check_filename)
