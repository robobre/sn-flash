# sn-flash : SuperNEMO - Falaise launcher automatic script 
Created by ylemiere 
Contact : lemiere@lpccaen.in2p3.fr
Date    : 2017, June







## Installation

## How to use it ?

1. Prepare working tree
2. Run on batch system
3. Store production on HPSS

### Display the help

```
./main_mgr.py --help
```

## Full example


+ Prepare directory tree and configure simulation production
+ Run simulation based on previous configuration
+ Store simulated directory tree with .brio files
+ Prepare directory tree and configure reconstruction based on previous simualtion production
+ Run reconstruction 
+ Store reconstruction directory tree with .brio files

### Prepare simulation 

```
$ python main_mgr.py --task simu --prepare --nb_file 5  --event_per_file 1000 --exp_name Demonstrator
```

**Answer to questions**

```
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
```

Check that /sps/nemo/scratch/simu/ylemiere/damned_sn_simu_1000 looks fine


### Run bunch of simulation 

```
$ python main_mgr.py --task simu --run  /sps/nemo/scratch/simu/ylemiere/damned_sn_simu_1000
``` 

[...]
INFO  : [run] : cc_job_submitter.qsub done...


**Check that jobs are running using qstat **
**Wait a while**

### Store simulation production on HPSS

```
$ python main_mgr.py --task simu --store /sps/nemo/scratch/simu/ylemiere/damned_sn_simu_1000
```

[...]
INFO  : [store_mc] : Expected storage path : /hpss/in2p3.fr/group/nemo/users/ylemiere/damned_sn_simu_1000

### Prepare reconstruction based on previous simulation

```
$ python main_mgr.py --task reco --prepare --input_data /hpss/in2p3.fr/group/nemo/users/ylemiere/damned_sn_simu_1000 --exp_name Demonstrator
```
OR
```
$ python main_mgr.py --task reco --prepare --input_data /sps/nemo/scratch/simu/ylemiere/damned_sn_simu_1000 --exp_name Demonstrator
```

**Answer to questions**

```
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
```

### Run bunch of simulation 

```
$ python main_mgr.py --task reco --run /sps/nemo/scratch/simu/ylemiere/damned_sn_reco_1000
```

[...]
INFO  : [run] : cc_job_submitter.qsub done...

**Check that jobs are running using qstat **
**Wait a while**

### Store reconstructed files on HPSS

```
$ python main_mgr.py --task reco --store /sps/nemo/scratch/simu/ylemiere/damned_sn_reco_1000
```


INFO  : [store_mc] : Expected storage path : /hpss/in2p3.fr/group/nemo/users/ylemiere/damned_sn_reco_1000
7389 bytes in 0 seconds through local (in) and p3p1 (out)