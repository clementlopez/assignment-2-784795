from multiprocessing import Pool, TimeoutError, Process
import time
import os

def run_process(process):                                                             
    os.system('python {}'.format(process))

if __name__ == '__main__':
    processes = []
    processes.append('app.py')
    processes.append('mysimbdp-batchingestmanager.py')
    pool = Pool(processes=2)
    pool.map(run_process, processes)