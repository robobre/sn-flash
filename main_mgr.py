#!/usr/bin/env python3


# Author  : Y.Lemiere
# Date    : 2017/03
# Contact : lemiere@lpccaen.in2p3.fr
# Object  : SuperNEMO Falaise soft manager

from datetime import date, datetime
import time
import sys
import os
import subprocess



import sn_tree_mgr

def usage():

    print("\nHow to use it :")
    print("-----------------\n")
    print("Examples")
    print("python main_mgr.py --task simu --prepare --nb_file 10 --event_per_file 100 --exp_name Demonstrator")
    print("python main_mgr.py --task simu --run /sps/nemo/scratch/simu/ylemiere/damned_simu_1")
    print("python main_mgr.py --task simu --store /sps/nemo/scratch/simu/ylemiere/damned_simu_1")
##    print("python main_mgr.py --task reco --input_data='/abs_dir/run_1'\n\n")
    print("python main_mgr.py --task reco --prepare --input_data /abs_dir/run_1 --exp_name Demonstrator\n\n")
    print("-----------------\n")

    print("List of option")
    print("--task [simu/reco]\n")
    print(" if simu [--prepare,--run,--store]\n")
    print("        --prepare")
    print("          |-> --input_variant_file PATH/FILE_NAME (optionnal)")
    print("          |-> --nb_file NUMBER")
    print("          |-> --event_per_file NUMBER")
    print("          `-> --exp_name  (Demonstrator, ...)")    
    print("        --run")
    print("          `-> INPUT_PATH")
    print("        --store")
    print("          `-> INPUT_PATH")
    print(" if reco [--prepare,--run,--store]\n")
    
    
    
    

    print("-----------------")
    return 1




if __name__ == '__main__':
    start_time= datetime.now()
    debug=True

    if debug:
        print ("**************************************************************")
        print ("*** Welcome SuperNEMO Falaise launcher automatic script    ***")
        print ("**************************************************************")



    try:
        APP_NAME=sys.argv[0]
        input_data_path=None
        variant_file=None

        simulation=False
        reconstruction=False
        production=False
        prepare_tree=False
        store_tarball=False
        run_prod=False


        if len(sys.argv) < 2:
            usage()
            sys.exit(1)

        if len(sys.argv) >= 2:
            i=0
            for arg in sys.argv[1:]:
                i=i+1
                if arg == "--input_variant_file" or arg == "-ivf":
                    variant_file=sys.argv[i+1]
                if arg == "--nb_file" or arg == "-nf":
                    nb_file=sys.argv[i+1]
                elif arg == "--event_per_file" or arg == "-ne":
                    nb_event=sys.argv[i+1]
                elif arg == "--input_data" or arg == "-idata":
                    input_data_path=sys.argv[i+1]
                elif arg == "--exp_name" or arg == "-exp":
                    exp_name=sys.argv[i+1]
                elif arg == "--task":
                    task=sys.argv[i+1]
                    if task=="simu":
                        simulation=True
                        reconstruction=False
                    if task=="reco":
                        simulation=False
                        reconstruction=True
                elif arg == "--prepare":
                    prepare_tree=True
                    run_prod=False
                elif arg == "--run":
                    prepare_tree=False
                    run_prod=True
                    input_data_path=sys.argv[i+1]
                elif arg == "--store":
                    store_tarball=True
                    input_data_path=sys.argv[i+1]
                elif arg == "--production" or arg == "-pro":
                    production=True
                elif arg == "--help" or arg == "-h":
                    usage()
                    sys.exit(1)
               
        else:
            print ("\033[91mERROR\033[00m : [%s] : No input args" % APP_NAME)
            usage()
            sys.exit(1)
        
    except AssertionError as inst:
       print("\033[91mERROR\033[00m : [%s] " % inst.args)
       usage()
       sys.exit(1)



    if debug:
        print("DEBUG : [%s] : arguments :" %APP_NAME )
        print("DEBUG :  task  == ",)
        if simulation == True and reconstruction == False:
            print("Simulation")
            if prepare_tree == True:
                print("              |-> Prepare working tree")
                print("              |-> variant_file     : %s "%variant_file)
                print("              |-> nb of file       : %s "%nb_file)
                print("              |-> event per file   : %s "%nb_event)            
                print("              `-> experiment       : %s "%exp_name)
            if run_prod == True:
                print("              |-> Running existing working tree")
                print("              `-> Input data path : %s "%input_data_path)            
            if store_tarball == True:
                print("              `-> Store existing simu. tarball")
        if reconstruction == True and simulation == False:
            print("reconstruction")
            if prepare_tree == True:
                print("              |-> Prepare working tree")
                print("              |-> SD data path     : %s "%input_data_path)
                print("              `-> experiment       : %s "%exp_name)

                

        
    #SIMULATION PURPOSE
    
    if prepare_tree == True:
      #  try:
            print("\n")
            #sn_simu_mgr_next.prepare_tree(nb_file,nb_event,exp_name,production,variant_file)
            if simulation == True and reconstruction == False:
                print("DEBUG : [%s] : sn_tree_mgr.prepare('simulation',exp_name,production,variant_file,nb_file,nb_event)"%APP_NAME)
                sn_tree_mgr.prepare_tree('a','simulation',exp_name, production, variant_file,nb_file,nb_event)
                print("\n")
                print("INFO : [%s] : You can process that cmd :\n python main_mgr.py --task simu --run PATH"%APP_NAME)
                print("\n")
            if simulation == False and reconstruction == True:
                if input_data_path == None:
                    print("\033[91mERROR\033[00m : [%s] : No SD files path!"%APP_NAME)
                    usage()
                    sys.exit(1)
                                
                    
                print("DEBUG : [%s] : sn_tree_mgr.prepare('reconstruction',exp_name, production)"%APP_NAME)
                sn_tree_mgr.prepare_tree(input_data_path,'reconstruction',exp_name, production)
                print("\n")
                print("INFO : [%s] : You can process that cmd :\n python main_mgr.py --task reco --run PATH"%APP_NAME)
                print("\n")
                
       # except:
       #     print("\033[91mERROR\033[00m : [%s] : Can not execute prepare_tree"%APP_NAME)
       #     sys.exit(1)


    if run_prod == True:
        try: 
            print("INFO : start : sn_tree_mgr.run_prod(input_data_path,FARM_LOCATION)")
            FARM_LOCATION="CCLYON"
            sn_tree_mgr.prepare_db(input_data_path)
            sn_tree_mgr.run(input_data_path,FARM_LOCATION)
        except:
            print("\033[91mERROR\033[00m : [%s] : Can not execute run_prod"%APP_NAME)
            sys.exit(1)
    if store_tarball == True:
        try: 
            print("DEBUG : [%s] : Store simulation tarball on HPSS@CCLYON" % APP_NAME)
            FARM_LOCATION="CCLYON"
            #sn_tree_mgr.publish_production(input_data_path,simulation, production)

            status = sn_tree_mgr.check_production_status(input_data_path)

            if status == True:
                sn_tree_mgr.prepare_tarball(input_data_path)
                sn_tree_mgr.store(input_data_path,FARM_LOCATION,production)
            else:
                print("\033[33mWARNING\033[00m : [%s] : Not ready to be stored on HPSS@CCLYON"%APP_NAME)

        except:
            print("\033[91mERROR\033[00m : [%s] : Can not store files on HPSS@CCLYON"%APP_NAME)
            sys.exit(1)


    





