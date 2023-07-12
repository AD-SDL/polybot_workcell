from gladier import GladierBaseClient, generate_flow_definition

from tecan_read import Tecan_Read
# from tecan_proc import Tecan_Proc
# from gather_data import GatherMetaData
# from model_update import Update_Model
import os

@generate_flow_definition()#modifiers={'publishv2_gather_metadata' : {'payload': '$.GatherMetadata.details.result[0]'}})
class polybot_Flow(GladierBaseClient):
    globus_group = 'dda56f31-53d1-11ed-bd8b-0db7472df7d6'
    gladier_tools = [
       'gladier_tools.globus.transfer.Transfer',
       Tecan_Read,
        # Tecan_Proc,
        #Update_Model,
    #     GatherMetaData,
    #    'gladier_tools.publish.Publishv2'
    ]

def tecan_flow( local_path, fname):
        remote_folder = "/C/Users/cnmuser/Desktop/Polybot/tecan_code/uv_vis_data"
        globus_compute_local = 'f352ef00-268a-4552-8a57-4772f51b54e4'
        flow_input = {
            'input': {
                'transfer_source_endpoint_id':'829262a0-1f5b-11ee-abf2-63e0d97254cd', #Tecan Transfer endpoint
                'transfer_source_path': os.path.join(remote_folder, fname), # Tecan file location
                'transfer_destination_endpoint_id':'2204acb8-1f65-11ee-abf2-63e0d97254cd', #Batman Transfer endpoint
                'transfer_destination_path': os.path.join(local_path, fname),
                'transfer_recursive': False,
                'compute_endpoint': globus_compute_local, #Batman compute endpoint
                'proc_folder': local_path,
                'file_name': fname,
                # 'publishv2': {
                #     'dataset': remote_folder,
                #     'index': '4e2884b0-e585-4913-8a33-4be155ebb06c',
                #     'project': 'cnm',
                #     'source_collection': '829262a0-1f5b-11ee-abf2-63e0d97254cd',
                #     'source_collection_basepath': '/',
                #     'destination_collection': '2204acb8-1f65-11ee-abf2-63e0d97254cd',
                #     'metadata': {},
                #     'ingest_enabled': True,
                #     'transfer_enabled':True,
                #     'destination':str("/portal/cnm"),
                #     'visible_to' : ['public']
                #    }
                }
            }

        # Create the Client
        publishFlow = polybot_Flow()
        label = 'PolybotTestFlow'
        # Run the flow
        print(flow_input)
        flow = publishFlow.run_flow(flow_input=flow_input,label=label)
        # Track progress
        action_id = flow['action_id']
        publishFlow.progress(action_id)
     
        
if __name__ == "__main__":
  local_path = "/home/rpl/workspace/polybot_workcell/demo_data/"
  fname = "ECP_demo_batch_1.asc"

  tecan_flow(local_path = local_path, fname = fname)
