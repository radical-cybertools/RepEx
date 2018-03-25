#!/usr/bin/env python

from radical.entk import AppManager, ResourceManager
from SyncEx import SynchronousExchange
import os, time
import radical.utils as ru
# ------------------------------------------------------------------------------
# Set default verbosity


os.environ['RADICAL_SAGA_VERBOSE']   = 'INFO'
os.environ['RP_ENABLE_OLD_DEFINES']  = 'True'
os.environ['RADICAL_ENMD_PROFILING'] = '1'
os.environ['RADICAL_PILOT_PROFILE']  = 'True'
os.environ['RADICAL_ENMD_PROFILE']   = 'True'
os.environ['RADICAL_ENTK_PROFILE']   = 'True'
os.environ['RADICAL_ENTK_VERBOSE']   = 'INFO'
os.environ['RP_ENABLE_OLD_DEFINES']  = 'True'
os.environ['SAGA_PTY_SSH_TIMEOUT']   = '2000'
os.environ['RADICAL_VERBOSE']        = 'INFO'
os.environ['RADICAL_PILOT_PROFILE']  = 'True'
os.environ['RADICAL_PILOT_DBURL']    = "mongodb://smush:key1209@ds117848.mlab.com:17868/db_repex_1"

#---------------------------------------#
## User settings

Replicas       = 128
Replica_Cores  = 20
Cycles         = 9    #0 cycles = no exchange
Resource       = 'xsede.supermic' #'ncsa.bw_aprun'
Pilot_Cores    = Replica_Cores * (Replicas)
#Pilot_Cores    = Replica_Cores * 32
ExchangeMethod = 'exchangeMethods/RandEx.py' #/path/to/your/exchange/method
MD_Executable  = '/usr/local/packages/amber/16/INTEL-140-MVAPICH2-2.0/bin/sander.MPI'  #'/u/sciteam/mushnoor/amber/amber14/bin/sander.MPI' #/path/to/your/MD/Executable

#MD_Executable = '/u/sciteam/mushnoor/amber/amber14/bin/sander.MPI'
timesteps      = 1000 #Number of timesteps between exchanges

#---------------------------------------#
                                                
if __name__ == '__main__':

    res_dict = {
                'resource': Resource,
                'walltime': 30,
                'cores': Pilot_Cores,
                'access_schema': 'gsissh',
                #'queue': 'debug',
                'queue': 'workq',
                'project': 'TG-MCB090174',
                #'project': 'bamm',
                }

    uid = ru.generate_id('radical.repex.run')
    logger = ru.get_logger('radical.repex.run')
    prof = ru.Profiler(name=uid)
    prof.prof('Create_Workflow_0', uid=uid)

    with open('logfile.log', 'a') as logfile:
        logfile.write( '%.5f' %time.time() + ',' + 'CreateWorkflow0' + '\n')

                       

    synchronousExchange=SynchronousExchange()
    

    rman                    = ResourceManager(res_dict)
    appman                  = AppManager(autoterminate=False, port=33068)  # Create Application Manager 
    appman.resource_manager = rman  # Assign resource manager to the Application Manager   
    
        

    Exchange                = synchronousExchange.InitCycle(Replicas, Replica_Cores, MD_Executable, ExchangeMethod, timesteps)
    

    appman.assign_workflow(set([Exchange])) # Assign the workflow as a set of Pipelines to the Application Manager 

    prof.prof('Run_Cycle_0', uid=uid)

    with open('logfile.log', 'a') as logfile:
        logfile.write( '%.5f' %time.time() + ',' + 'RunCycle0' + '\n')

    appman.run() # Run the Application Manager 

    prof.prof('End_Cycle_0', uid=uid)

    with open('logfile.log', 'a') as logfile:
        logfile.write( '%.5f' %time.time() + ',' + 'EndCycle0' + '\n')



    

    
    for Cycle in range (Cycles):

        prof.prof('Create_Workflow_{0}'.format(Cycle+1), uid=uid)

        with open('logfile.log', 'a') as logfile:
            logfile.write( '%.5f' %time.time() + ',' + 'CreateWorkflow{0}'.format(Cycle+1) + '\n')
                        
        Exchange_gen            = synchronousExchange.GeneralCycle(Replicas, Replica_Cores, Cycle, MD_Executable, ExchangeMethod)
        
        appman.assign_workflow(set([Exchange_gen])) # Assign the workflow as a set of Pipelines to the Application Manager       

        prof.prof('Run_Cycle_{0}'.format(Cycle+1), uid=uid)

        with open('logfile.log', 'a') as logfile:
            logfile.write( '%.5f' %time.time() + ',' + 'RunCycle{0}'.format(Cycle+1) + '\n')
                         

        appman.run() # Run the Application Manager

        prof.prof('End_Cycle_{0}'.format(Cycle+1), uid=uid)

        with open('logfile.log', 'a') as logfile:
            logfile.write( '%.5f' %time.time() + ',' + 'EndCycle{0}'.format(Cycle+1) + '\n')

    appman.resource_terminate()

    mdtasks  = synchronousExchange.mdtasklist
    extasks  = synchronousExchange.extasklist
    print mdtasks

    print extasks
    #appman.resource_terminate()

    
