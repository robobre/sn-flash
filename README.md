# sn-flash : SuperNEMO - Falaise launcher automatic script 

> Author  : Yves Lemière
> Contact : lemiere@lpccaen.in2p3.fr
> Date    : 2017, June



## Note

-[x] Tested at CCLYON
-[] Tested using another batch system
-[] Fill Database



## Installation

## How to use it ?

1. Prepare working tree
2. Run on batch system
3. Store production on HPSS@CCLYON

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

*Answer to questions to configure your production (default use GUI)*

```
DEBUG : [prepare_tree] : working tree starting by /path/on/sps/at/lyon/ylemiere/damned_sn_simu_1000
             |-> CONFIG PATH            : /path/on/sps/at/lyon/ylemiere/damned_sn_simu_1000/config.d
             |      |-> VARIANT PATH    : /variant.d/
             |      |      `-> file name:  variant.profile
             |      |-> SEED PATH    : /seeds.d/
             |      `-> CONF PATH       : /conf.d/
             |->  OUTPUT DATA PATH      : /path/on/sps/at/lyon/ylemiere/damned_sn_simu_1000/output_files.d
             `->  SYS PATH              : /path/on/sps/at/lyon/ylemiere/damned_sn_simu_1000/.sys
                    |-> LOG PATH        : /log.d/
                    |      `-> file name:  main.log
                    `-> LAUNCHER PATH   : /launcher.d/
[...]

INFO : [main_mgr.py] : You can process that cmd :
python main_mgr.py --task simu --run PATH
```

Check that /path/on/sps/at/lyon/ylemiere/damned_sn_simu_1000 looks fine


### Run bunch of simulation 

```
$ python main_mgr.py --task simu --run   /path/on/sps/at/lyon/ylemiere/damned_sn_simu_1000
``` 

> CCLYON Batch system will start *soon*. Check batch status using `qstat` command
> And Wait a while



### Store simulation production on HPSS

```
$ python main_mgr.py --task simu --store  /path/on/sps/at/lyon/ylemiere/damned_sn_simu_1000
```

+ For a blessed production, storage path has to be define by a blessed path.
+ For a user production, storage path on HPSS will be ` /path/on/hpss/at/lyon/${USER}/`

```
[...]
INFO  : [store_mc] : Expected storage path : /path/on/hpss/at/lyon/ylemiere/damned_sn_simu_1000
```


### Prepare reconstruction based on previous simulation

You can reconstruct simulated data based on simulation production on /sps or /hpss.

```
$ python main_mgr.py --task reco --prepare --input_data  /path/on/hpss/at/lyon/ylemiere/damned_sn_simu_1000 --exp_name Demonstrator
```
or
```
$ python main_mgr.py --task reco --prepare --input_data  /path/on/sps/at/lyon/ylemiere/damned_sn_simu_1000 --exp_name Demonstrator
```

*Answer to questions*

```
INFO : [prepare_tree] : Based on SD production :/path/on/hpss/at/lyon/ylemiere/damned_sn_simu_1000s
             |-> CONFIG PATH            : /path/on/sps/at/lyon/ylemiere/damned_sn_reco_1000/config.d
             |      `-> CONF PATH       : /conf.d/
             |->  OUTPUT DATA PATH      : /path/on/sps/at/lyon/ylemiere/damned_sn_reco_1000/output_files.d
             `->  SYS PATH              : /path/on/sps/at/lyon/ylemiere/damned_sn_reco_1000/.sys
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
$ python main_mgr.py --task reco --run /path/on/sps/at/lyon/ylemiere/damned_sn_reco_1000
```

To check the running jobs on batch system, use `qstat` command



### Store reconstructed files on HPSS

```
$ python main_mgr.py --task reco --store /path/on/sps/at/lyon/ylemiere/damned_sn_reco_1000
```

```
INFO  : [store_mc] : Expected storage path : /path/on/hpss/at/lyon/ylemiere/damned_sn_reco_1000
7389 bytes in 0 seconds through local (in) and p3p1 (out)
```