#!/usr/bin/env python3

import logging
from pathlib import Path
from argparse import ArgumentParser
from rpl_wei.wei_workcell_base import WEI
from pathlib import Path

def main():
    wf_path = Path('/home/rpl/workspace/polybot_workcell/polybot_workcell/workflows/demo.yaml')

    wei_client = WEI(wf_config = wf_path.resolve(), workcell_log_level=logging.ERROR, workflow_log_level=logging.ERROR)

    payload={
        }

    run_info = wei_client.run_workflow(payload=payload)
    print(run_info)

if __name__ == "__main__":
    main()
