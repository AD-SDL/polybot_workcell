from gladier import GladierBaseClient, generate_flow_definition

from tecan_read import Tecan_Read
from tecan_proc import Tecan_Proc
from gather_data import GatherMetaData
from model_update import Update_Model
import os

@generate_flow_definition(modifiers={'publishv2_gather_metadata' : {'payload': '$.GatherMetadata.details.result[0]'}})
class C2Flow(GladierBaseClient):
    globus_group = 'dda56f31-53d1-11ed-bd8b-0db7472df7d6'
    gladier_tools = [
       'gladier_tools.transfer.Transfer',
        Tecan_Read,
        Tecan_Proc,
        #Update_Model,
        GatherMetaData,
       'gladier_tools.publish.Publishv2'
    ]

def tecan_flow(exp_name, plate_n, time, local_path, fname):
        experiment_label = exp_name + "_" + plate_n + "_" + time
        remote_folder = os.path.join("C:\Users\cnmuser\Desktop\Polybot\tecan_code\uv_vis_data", experiment_label)
        local_funcx = 'NONE' #TODO: FIND FUNCX ID
        flow_input = {
            'input': {
                'transfer_source_endpoint_id':'829262a0-1f5b-11ee-abf2-63e0d97254cd', #Tecan endpoint
                'transfer_source_path': os.path.join(local_path, fname), # Tecan file location
                'transfer_destination_endpoint_id':'2204acb8-1f65-11ee-abf2-63e0d97254cd', #Batman enpoint
                'trasnfer_destination_path': os.path.join(remote_folder, fname),
                'transfer_reqursive': False,
                'funcx_endpoint_compute': local_funcx, #Batman funcx
                'funcx_endpoint_non_compute': local_funcx, #Batman funcx
                'exp_name':exp_name,
                'plate_n':plate_n,
                'proc_folder':remote_folder,
                'file_name': fname,
                'csv_file': fname.split('.')[0] +".asc",
                'csv_file_corr': fname +"_corr.asc",
                'time': time,
                # 'make_input': local_path,
                # 'local_path': local_path,
                # 'remote_file': fname,

                'publishv2': {
                    'dataset': remote_folder,
                    'index': '4e2884b0-e585-4913-8a33-4be155ebb06c',
                    'project': 'cnm',
                    'source_collection': '829262a0-1f5b-11ee-abf2-63e0d97254cd',
                    'source_collection_basepath': '/',
                    'destination_collection': '2204acb8-1f65-11ee-abf2-63e0d97254cd',
                    'metadata': {},
                    'ingest_enabled': True,
                    'transfer_enabled':True,
                    'destination':str("/portal/cnm"),
                    'visible_to' : ['public']
                   }
                # 'pilot': {
                #     'dataset': str(folder_path.expanduser()),
                #     'index': '4e2884b0-e585-4913-8a33-4be155ebb06c',
                #     'project': 'bio',
                #     'transfer_source_endpoint_id': '95038e17-339b-4462-9c9f-a8473809af25',
                #     'source_collection_basepath': '/',
                #     'metadata': {},
                #     'destination':str(dest_path)
                #    }
                }
            }

        # Create the Client
        publishFlow = C2Flow()
        label = 'BioTestFlow'
        # Run the flow
        flow = publishFlow.run_flow(flow_input=flow_input,label=label)
        # Track progress
        # action_id = flow['action_id']
        # publishFlow.progress(action_id)
     
        
if __name__ == "__main__":
  local_path = "/home/rpl/workspace/polybot_workcell/demo_data/ECP_demo_batch_1.asc"
  fname = "ECP_demo_batch_1.asc"
  exp_name = "first_exp"
  

  tecan_flow(exp_name = exp_name, plate_n = 1, time = "time", local_path = local_path, fname = fname)
