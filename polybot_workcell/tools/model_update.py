from gladier import GladierBaseTool, generate_flow_definition


def Update_Model(**data):
    import pandas as pd
    import csv
    import os
    import json
    """
    Description: Predictive ML model reads the filename with the previous Lab measurements 
    and the experimental inputs

    Parameters:
        file_name: the complete path and name of the csv file with the Lab values

    Returns:
        df: a pandas data frame with the next suggested experiments


    """
    file_name = data.get('csv_name')
    df = pd.DataFrame()

    # extract the reading date, time, and data (into dataframe)
    DATA = False
    with open(file_name, newline="") as csvfile:
        print(f"opened {file_name}")
        csv.QUOTE_NONNUMERIC = True
        reader = csv.reader(csvfile)
        i = 0
        for row in reader:
            i += 1
            row = [x.strip() for x in row]
            if i == 3: 
                reading_date, reading_time = row[0].split(" ")
            if len(row) > 0 and row[0] == "Plate #":
                df = pd.DataFrame(columns=row)
                DATA = True
                continue
            if DATA == True:
                df.loc[len(df.index) + 1] = row

    timestamp_list = df.columns[3:].to_list()

    # extract file basename 
    basename = os.path.basename(file_name) 
    blob = df.to_dict()
    t = {}
    t.update({"timestamp_list" : timestamp_list, "reading_date": reading_date, "reading_time": reading_time, "basename": basename})
    t.update({"pandas" : blob})
    blob = json.dumps(blob)
    
    return blob #df, timestamp_list, reading_date, reading_time, basename 

@generate_flow_definition
class Model_Update(GladierBaseTool):
    funcx_functions = [Update_Model]
    required_input = [
        'funcx_endpoint_compute'
    ]
