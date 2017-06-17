#!/usr/local/python/python-2.7/bin/python


# Author  : Y.Lemiere
# Date    : 2017/03
# Contact : lemiere@lpccaen.in2p3.fr
# Object  : SuperNEMO Simulation manager

from datetime import date, datetime
import time
import sys
import os
import subprocess


import sn_simu_mgr_next

def usage():
    print("How to use it :\n")
    print("-----------------")
    print("python main_mgr.py --task simu --prepare --nb_file 10 --event_per_file 100 --exp_name Demonstrator")
    print("python main_mgr.py --task simu --run /sps/nemo/scratch/simu/ylemiere/damned_simu_1")
    print("python main_mgr.py --task simu --store /sps/nemo/scratch/simu/ylemiere/damned_simu_1")
    print("python main_mgr.py --task reco --input_data='/abs_dir/run_1'")
    print("-----------------")
    return 1




if __name__ == '__main__':
    start_time= datetime.now()
    debug=True

    if debug:
        print ("******************************************")
        print ("*** Welcome in wonderful 'main_mgr'    ***")
        print ("******************************************")



    try:
        APP_NAME=sys.argv[0]
        input_data_path=None
        
        simulation=False
        reconstruction=False
        production=False
        prepare_mc_tree=False
        store_mc_tarball=False
        run_mc=False
        if len(sys.argv) < 2:
            usage()
            sys.exit(1)

        if len(sys.argv) > 2:
            i=0
            for arg in sys.argv[1:]:
                i=i+1
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
                        print("task = %s"%task)
                        simulation=True
                        reconstruction=False
                    if task=="reco":
                        simulation=False
                        reconstruction=True
                elif arg == "--prepare":
                    prepare_mc_tree=True
                    run_mc=False
                elif arg == "--run":
                    prepare_mc_tree=False
                    run_mc=True
                    input_data_path=sys.argv[i+1]
                elif arg == "--store":
                    store_mc_tarball=True
                    input_data_path=sys.argv[i+1]
                elif arg == "--production" or arg == "-pro":
                    production=True
                elif arg == "--help" or arg == "-h":
                    usage()
                    sys.exit(1)
               
        else:
            print "%s : ERROR : No input args" % APP_NAME
            usage()
            sys.exit(1)
        
    except AssertionError as inst:
       print("ERROR : %s " % inst.args)
       usage()
       sys.exit(1)



    if debug:
        print("DEBUG : %s : List of arguments" %APP_NAME )
        print "INFO :  task  == ",
        if simulation == True and reconstruction == False:
            print("Simulation")
            if prepare_mc_tree == True:
                print("              |-> Prepare working tree")
                print("              |-> nb of file       : %s "%nb_file)
                print("              |-> event per file   : %s "%nb_event)            
                print("              `-> experiment       : %s "%exp_name)
            if run_mc == True:
                print("              |-> Running existing working tree")
                print("              `-> Input data path : %s "%input_data_path)            
            if store_mc_tarball == True:
                print("              `-> Store existing simu. tarball")
        if reconstruction == True and simulation == False:
            print("reconstruction")
            print("                  `-> input data     : %s "%input_data_path)            


        

    if simulation == True and reconstruction == False:
        if prepare_mc_tree == True:
            try: 
                print("INFO : start : sn_simu_mgr.prepare_mc(nb_file,nb_event,exp_name,production)")
                sn_simu_mgr_next.prepare_mc_tree(nb_file,nb_event,exp_name,production)
                print("INFO : You can process that cmd :\n python main_mgr.py --task simu --run PATH")
            except:
                print("ERROR : %s : Can not execute prepare_mc"%APP_NAME)
                sys.exit(1)
        if run_mc == True:
            try: 
                print("INFO : start : sn_simu_mgr.run_mc(input_data_path,FARM_LOCATION)")
                FARM_LOCATION="CCLYON"
                sn_simu_mgr_next.run_mc(input_data_path,FARM_LOCATION)
            except:
                print("ERROR : %s : Can not execute run_mc"%APP_NAME)
                sys.exit(1)
        if store_mc_tarball == True:
            try: 
                print("INFO : %s : Store simulation tarball on HPSS@CCLYON" % APP_NAME)
                FARM_LOCATION="CCLYON"
                sn_simu_mgr_next.publish_production(input_data_path,simulation, production)
                #sn_simu_mgr_next.prepare_tarball(input_data_path)
                #sn_simu_mgr_next.store_mc(input_data_path,FARM_LOCATION,production)
            except:
                print("ERROR : %s : Can not store files on HPSS@CCLYON"%APP_NAME)
                sys.exit(1)


    


    if simulation == False and reconstruction == True:
        try: 
            print("INFO : %s Try to start reco process" % APP_NAME)
        except:
            print("ERROR : %s Can not execute reco process"%APP_NAME)
            sys.exit(1)





