from gladier import GladierBaseClient, generate_flow_definition, GladierBaseTool


def Tecan_Read(**data):
    """
    Extracts raw data from Mangelan asc file into a csv file

    :param str filename: filename of Mangelan asc file to convert

    output: path of new csv file (str)

    """
    import os
    from pathlib import Path
    import pandas as pd
    import csv
    delimiter='\t'
    data = {'wavelength': []}
    column_names = set()
    filepath = data.get('local_path')
    filename = data.get('proc_folder') + "/" +  data.get("remote_file")

    with open(os.path.join(filepath, filename), 'r', encoding="utf-16-le") as input_file:
        for line in input_file:
            line = line.strip()

            if line.startswith('*'):
                fields = line[2:].replace('nm', '').split(delimiter)
                data['wavelength'].extend(fields)
            elif line.startswith('C'):
                columns = line.split(delimiter)
                column_name = columns[0]
                column_values = columns[1:]
                data[column_name] = column_values
                column_names.add(column_name)

    if os.path.exists(filename):
        asc_basename = os.path.splitext(os.path.basename(filename))[0]
        csv_filename = asc_basename + ".csv"
        csv_filepath = filename.replace(os.path.basename(filename), csv_filename)

    with open(csv_filepath, 'w', newline='') as output_file:
        csv_writer = csv.writer(output_file)
        csv_writer.writerow(['wavelength'] + sorted(column_names))
        num_rows = max(len(data['wavelength']), max(len(values) for values in data.values() if isinstance(values, list)))
        for i in range(num_rows):
            row = [data[column][i] if i < len(data[column]) else '' for column in ['wavelength'] + sorted(column_names)]
            csv_writer.writerow(row)

    return csv_filepath


@generate_flow_definition
class Tecan_Read(GladierBaseTool):
    funcx_functions = [Tecan_Read]
    required_input = [
        'funcx_endpoint_compute'
    ]
