# sn-flash : SuperNEMO - Falaise launcher automatic script 
Created by ylemiere 
Contact : lemiere@lpccaen.in2p3.fr
Date    : 2017, June







## Installation

## How to use it 

- [] Prepare working tree
- [] Run on batch system
- [] Store production on HPSS

### Display the help

```
./main_mgr.py --help
```

## Full example

### Command to prepare simulation 

```
[CMD 0] python main_mgr.py --task simu --prepare --nb_file 5  --event_per_file 1000 --exp_name Demonstrator
```

**Answer to questions**


*DEBUG : [prepare_tree] : working tree starting by /sps/nemo/scratch/simu/ylemiere/damned_sn_simu_1000
             |-> CONFIG PATH            : /sps/nemo/scratch/simu/ylemiere/damned_sn_simu_1000/config.d
             |      |-> VARIANT PATH    : /variant.d/
             |      |      `-> file name:  variant.profile
             |      |-> SEED PATH    : /seeds.d/
             |      `-> CONF PATH       : /conf.d/
             |->  OUTPUT DATA PATH      : /sps/nemo/scratch/simu/ylemiere/damned_sn_simu_1000/output_files.d
             `->  SYS PATH              : /sps/nemo/scratch/simu/ylemiere/damned_sn_simu_1000/.sys
                    |-> LOG PATH        : /log.d/
                    |      `-> file name:  main.log
                    `-> LAUNCHER PATH   : /launcher.d/
[...]
INFO : [main_mgr.py] : You can process that cmd :
python main_mgr.py --task simu --run PATH*

Check that /sps/nemo/scratch/simu/ylemiere/damned_sn_simu_1000 looks fine


```
[CMD 1] python main_mgr.py --task simu --run  /sps/nemo/scratch/simu/ylemiere/damned_sn_simu_1000
``` 

[...]
INFO  : [run] : cc_job_submitter.qsub done...


**Check that jobs are running using qstat **
**Wait a while**


[CMD 2] python main_mgr.py --task simu --store /sps/nemo/scratch/simu/ylemiere/damned_sn_simu_1000
[...]
INFO  : [store_mc] : Expected storage path : /hpss/in2p3.fr/group/nemo/users/ylemiere/damned_sn_simu_1000


[CMD 3] python main_mgr.py --task reco --prepare --input_data /hpss/in2p3.fr/group/nemo/users/ylemiere/damned_sn_simu_1000 --exp_name Demonstrator

OR
[CMD 3'] python main_mgr.py --task reco --prepare --input_data /sps/nemo/scratch/simu/ylemiere/damned_sn_simu_1000 --exp_name Demonstrator

**Answer to questions**


INFO : [prepare_tree] : Based on SD production : /hpss/in2p3.fr/group/nemo/users/ylemiere/damned_sn_simu_1000s
             |-> CONFIG PATH            : /sps/nemo/scratch/simu/ylemiere/damned_sn_reco_1000/config.d
             |      `-> CONF PATH       : /conf.d/
             |->  OUTPUT DATA PATH      : /sps/nemo/scratch/simu/ylemiere/damned_sn_reco_1000/output_files.d
             `->  SYS PATH              : /sps/nemo/scratch/simu/ylemiere/damned_sn_reco_1000/.sys
                    |-> LOG PATH        : /log.d/
                    |      `-> file name:  main.log
                    `-> LAUNCHER PATH   : /launcher.d/
DEBUG : [prepare_tree] : Working tree produced ! 

[...]

INFO : [main_mgr.py] : You can process that cmd :
 python main_mgr.py --task reco --run PATH


[CMD 4] python main_mgr.py --task reco --run /sps/nemo/scratch/simu/ylemiere/damned_sn_reco_1000

[...]
INFO  : [run] : cc_job_submitter.qsub done...

**Check that jobs are running using qstat **
**Wait a while**


[CMD 5] python main_mgr.py --task reco --store /sps/nemo/scratch/simu/ylemiere/damned_sn_reco_1000

INFO  : [store_mc] : Expected storage path : /hpss/in2p3.fr/group/nemo/users/ylemiere/damned_sn_reco_1000
7389 bytes in 0 seconds through local (in) and p3p1 (out)