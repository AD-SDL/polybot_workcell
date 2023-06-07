from gladier import GladierBaseTool, generate_flow_definition
import pandas as pd
import numpy as np
import os
from rdkit import Chem
from rdkit.Chem import AllChem
from sklearn.ensemble import RandomForestRegressor
from sklearn.externals import joblib

inventory = ["CCCC", "CCCCCC", "CCC", "CCCCCCC", "CCCCO"]

def smile_to_bits(smile):
  mol = Chem.MolFromSmiles(smile)
  return AllChem.GetMorganFingerprintAsBitVect(mol, 2, nBits=1024, useChirality=True)  

def get_vectors(smiles):
  bits = []
  for smile in smiles:
    try:
      bits.append(np.asarray(smile_to_bits(smile)))
    except:
      bits.append(np.zeros(1024))
  return bits

def bits_to_df(smiles, prefix):
  df = pd.DataFrame(get_vectors(smiles))
  columns = [f'{prefix}_{i}' for i in df.columns]
  df.columns = columns
  return df

def create_predictions_dataset(inventory):
    """Given the inventory as a list we want to create a dataset of all possible combinatios 
       and ratios of the first molecule of the list with the remaining ones.
       This dataset is the input to the trained predictive model.    

    Parameters:
        inventory: SMIILES list of molecules available in Chemspeed

    Returns:
        df: a pandas dataframe with all the possible pairs of the inventory

    """
    data_all=[]
    for smiles in inventory:        
        data_all.append(create_predictions_dataset(inventory, smiles))
    dataset = pd.concat(data_all, axis=0)
    return dataset

def create_predictions_dataset(inventory, smiles2):
    percentage_1 = np.array([50,55, 60, 65, 70, 75, 80, 85, 90, 95, 100])/100
    percentage_2 = (1 - percentage_1)
    percentage_3 = (np.zeros(len(percentage_1)))
    smiles1 = inventory[0] # the first molecule of the inventory is going to be the standarized one
    validation = pd.concat([pd.DataFrame(np.repeat(smiles1, len(percentage_1),axis=0), columns=['smiles1']),
                            pd.DataFrame(np.repeat(smiles2, len(percentage_1),axis=0), columns=['smiles2']),
    pd.DataFrame(percentage_3, columns=['smiles3']) ,
    pd.DataFrame(percentage_1, columns=['percentage_1']), 
    pd.DataFrame(percentage_2, columns=['percentage_2']),
    pd.DataFrame(percentage_3, columns=['percentage_3'])], axis=1)

    validation_1 =  bits_to_df(validation.smiles1, 'bit_1')
    validation_2 =  bits_to_df(validation.smiles2, 'bit_2')
    validation_3 =  bits_to_df(validation.smiles3, 'bit_3')
    validation_dataset = pd.concat([validation.smiles2, validation_1,validation[['percentage_1']], validation_2,validation[['percentage_2']], validation_3,validation[['percentage_3']]], axis=1) 
    return validation_dataset

def train_model(model, X_train, y_train):
    regr_rf = joblib.load('random_forest_model.pkl')
    regr_rf.fit(X_train, y_train)
    joblib.dump(regr_rf, 'random_forest_model.pkl')    
    return regr_rf

def predict(model, dataset):
    preds = model.predict(dataset)
    dataset['preds'] = preds
    df =df.sort_values(by=['preds']).head(6)
    return dataset

def Update_Model(**data):
    import pandas as pd
    import csv
    import os
    import json
    
    """
    Description: Predictive ML model reads the filename with the previous Lab measurements 
    and the experimental inputs

    Parameters:
        inventory: list of smiles with the molecules available in Chemspeed
        tecan_filename: the complete path and name of the csv file with the Lab values
        experimental_filename: the complete path and name of the csv file with the experimental conditions
        e.g., smilesA, smilesB, smilesC, %A, %B, %C
        ml_model_checkpoints: pretrained ML model checkpoints

    Returns:
        df: a pandas dataframe with the next suggested experiments

    """
    file_name = data.get('csv_name')
    df = pd.DataFrame()
    experimental_df = pd.DataFrame() # df with combined the tecan results and the initial experiment parameters (i.e., smiles + ratios)
    model = joblib.load('random_forest_model.pkl')
    X_train, y_train = experimental_df.iloc[:, :-1], experimental_df.iloc[ :, -1]
    train_model(model, X_train, y_train)
    dataset = create_predictions_dataset(inventory)
    df = predict(model, dataset)
    return df # this file should go to chemspeed


@generate_flow_definition
class Model_Update(GladierBaseTool):
    funcx_functions = [Update_Model]
    required_input = [
        'funcx_endpoint_compute'
    ]
