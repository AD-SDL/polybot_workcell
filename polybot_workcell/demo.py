#!/usr/bin/env python3

import logging
from pathlib import Path
from argparse import ArgumentParser
from rpl_wei import Experiment
from pathlib import Path

from time import sleep

def main():
    wf_path = Path('/home/rpl/workspace/polybot_workcell/polybot_workcell/workflows/demo.yaml')

    exp = Experiment("127.0.0.1","8000","CNM Experiment")
    exp.register_exp()

    flow_info = exp.run_job(wf_path.resolve(), simulate = False)
    print(flow_info)
    flow_status =exp.query_job(flow_info['job_id'])
    print(flow_status)

    while flow_status["status"] != "finished":
        flow_status = exp.query_job(flow_info["job_id"])
        print(flow_status)
        sleep(1)
    print(flow_status)

    # payload={
    #     }

    # run_info = wei_client.run_workflow(payload=payload)
    # print(run_info)

if __name__ == "__main__":
    main()
