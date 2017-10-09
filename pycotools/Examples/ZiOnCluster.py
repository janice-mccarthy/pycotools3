import os
import site
site.addsitedir('/home/b3053674/Documents/pycotools')
from pycotools import *
from zi_model_varients import Models
import pandas
import matplotlib.pyplot as plt
import seaborn
import numpy
import copy
import shutil


directory = r'/home/b3053674/Documents/Models/2017/10_Oct/Smad7Fit'
fit_dir = os.path.join(directory, 'Fit1Dir')


CONFIGURE = False
RUN = False
PLOT = True


def get_models(directory):
    """
    Get models from Models class and save as cps
    files in a directory of users choosing.

    :param directory: where to save the model varients
    :return: dict[model_id] = FullPathToModel
    """
    ## if directory not exists create it
    if not os.path.isdir(directory):
        os.makedirs(directory)

    ## get all methods of the Models class
    all_methods = dir(Models)

    ## remove magic methods
    all_model_methods = [i for i in all_methods if i[:2] != '__']
    all_model_methods = [i for i in all_methods if i != 'published_zi']

    M = Models()
    dct = {}
    for model_id in all_model_methods:
        m = getattr(Models, model_id)
        if type(m) == property:
            model_str = m.fget(M)
            cps_file = os.path.join(directory, '{}.cps'.format(model_id))
            dct[model_id] = cps_file

            ## if already exists remove
            if os.path.isfile(cps_file):
                os.remove(cps_file)

            ## write file
            with open(cps_file, 'w') as f:
                f.write(model_str)

            ## raise error if not exists
            if not os.path.isfile(cps_file):
                raise Exception
    return dct

def read_models_into_pycotools(files_dct):
    dct = {}
    for v in files_dct.values():
        dct[v] = model.Model(v)
    return dct

def read_data_file(fle):
    """
    read data into pandas dataframe for each
    data set
    """
    data = pandas.read_csv(fle)
    data = data.set_index(['Cell Type', 'Repeat'])
    time = [int(i) * 60 for i in data.columns]
    data.columns = time
    return data

def make_smad_protein_data(df):
    ## deep copy for reproducability
    data = copy.deepcopy(df)
    time = [i + 30 for i in data.columns]
    data.columns = time

    ## add 0 time point = 75% of time 30
    data[0] = 0.75 * data[30]
    data = data[sorted(data.columns)]
    return data * 100


seaborn.set_context(context='notebook')

def plot_experimental(data, title):
    for label, df in data.groupby(level=0):
        plt.figure()
        ax = df.transpose().plot()
        ax.legend(loc=(1, 0.5))
        plt.title('{}: {}'.format(title, label))
        plt.ylabel('Signal (AU)')
        plt.xlabel('Time(h)')

def format_copasi(data, data_directory, data_name, truncate_number):
    file_dct = {}
    ## iterate over cell types
    for label, df in data.groupby(level=0):
        ## nested dict for resutls collection

        file_dct[label] = {}
        ## reset index, transpose and rename index
        df = df.reset_index(drop='True')
        df = df.transpose()
        df.index.name = 'Time'

        ##iterate over each column
        for i in df.columns:
            ##create subdirectory for each cell type
            dir2 = os.path.join(data_directory, label)
            if not os.path.isdir(dir2):
                os.makedirs(dir2)

            ## get experimental repeat
            smad7 = pandas.DataFrame(df[i])
            smad7 = smad7.astype(float)
            smad7 = smad7.reset_index()

            ## relabel to match model variable
            smad7.columns = ['Time', data_name]

            ## ensure consistent time units
            smad7 = smad7.iloc[:truncate_number]

            ## write to file
            fle = os.path.join(dir2, '{}_{}_data.csv'.format(i, data_name))
            file_dct[label][i] = fle
            smad7.to_csv(fle, index=False, sep='\t')
    return file_dct

def set_initial_values(all_models, cell_type):
    new_models = []
    for mod in all_models.values():
        mod = mod.set('global_quantity', 'Smad7mRNAInitial',
                      float(smad7_mRNA_starting_values.loc[cell_type]), match_field='name',
                      change_field='initial_value')

        mod = mod.set('global_quantity', 'SkiInitial',
                      float(ski_starting_values.loc[cell_type]), match_field='name', change_field='initial_value')

        mod = mod.set('global_quantity', 'Smad7ProteinInitial',
                      float(smad7_protein_starting_values.loc[cell_type]), match_field='name',
                      change_field='initial_value')

        new_models.append(mod)
    return new_models


if CONFIGURE:
    LOG.debug('configuring')
    ## get models and save into user specified directory
    model_paths = get_models(fit_dir)

    ##get model.Model instance per model
    models = read_models_into_pycotools(model_paths)

    ## get and read experimental data
    smad7_mRNA_data_file = os.path.join(directory, 'smad7_pcr_data.csv')
    ski_data_file = os.path.join(directory, 'ski_pcr_data.csv')


    smad7_mRNA_data = read_data_file(smad7_mRNA_data_file)
    ski_data = read_data_file(ski_data_file)

    ## manafacture some smad7 protein level data from the mRNA level
    smad7_protein_data = make_smad_protein_data(smad7_mRNA_data)

    ## Create directories for data files
    smad7_protein_data_directory = os.path.join(directory, 'Smad7ProteinDataDirectory')
    ski_data_directory = os.path.join(directory, 'SkiDataDirectory')
    smad7_mRNA_directory = os.path.join(directory, 'Smad7mRNADataDirectory')

    ## format and write the data files into these directories
    smad7_protein_data_files = format_copasi(smad7_protein_data, smad7_protein_data_directory, 'Smad7Obs', truncate_number=6)
    ski_data_files = format_copasi(ski_data, ski_data_directory, 'SkiObs', truncate_number=6)
    smad7_mRNA_data_files = format_copasi(smad7_mRNA_data, smad7_mRNA_directory, 'Smad7mRNAObs', truncate_number=6)

    ## copy data files into a 'fit project directory'
    for i in [smad7_protein_data_files, ski_data_files, smad7_mRNA_data_files]:
        for j in i['Neonatal']:
            # print (i['Neonatal'][j])
            shutil.copy(i['Neonatal'][j], fit_dir)

    ## get averages of the repeated experiment as start values
    smad7_mRNA_starting_values = pandas.DataFrame(smad7_mRNA_data[0].groupby(level=0).agg(numpy.mean))
    ski_starting_values = pandas.DataFrame(ski_data[0].groupby(level=0).agg(numpy.mean))
    smad7_protein_starting_values = pandas.DataFrame(smad7_protein_data[0].groupby(level=0).agg(numpy.mean))

    ##set the initial concentrations of smad7 and ski to the average of the repeat data
    models = set_initial_values(models, 'Neonatal')

    ##save the model
    [i.save() for i in models]



## create instance of MultiModelFit.
## This is needed to setup, run and plot
PE = tasks.MultiModelFit(
    fit_dir,
    # smad7_mRNA_data_files['Neonatal'].values() + smad7_protein_data_files['Neonatal'].values() + ski_data_files['Neonatal'].values(),
    metabolites=['Ski'], global_quantities=['Smad7SF', 'SkiSF'],
    overwrite_config_file=True,
    method='genetic_algorithm', population_size=150, number_of_generations=300,
    upper_bound=1e4, run_mode='sge', copy_number=100, pe_number=1,
)
PE.write_config_file()
PE.setup()

if RUN:
    PE.run()

if PLOT:
    for m in PE:
        TCM = viz.PlotTimeCourseEnsemble(m, y=['Smad7', 'Smad7Obs', 'Ski',
                                               'Smad7_mRNA', 'Ski_mRNA',
                                               'SkiObs', 'Smad7mRNAObs'],
                                     savefig=True)
























































































#
# if ZI_PUB:
#
#     zi_path = r'/home/b3053674/Documents/pycotools/pycotools/Examples/zi_model2012.cps'
#     zi_str = Models.published_zi()
#
#     with open(zi_path, 'w') as f:
#         f.write(zi_str)
#
#
#     m = model.Model(zi_path)
#
#
#     TC = tasks.TimeCourse(m, end=1000, step_size=100, intervals=10)
#     misc.format_timecourse_data(TC.report_name)
#
#     PE = tasks.MultiParameterEstimation(m, TC.report_name,
#                                         method='genetic_algorithm',
#                                         population_size=10,
#                                         number_of_generations=10,
#                                         copy_number=2,
#                                         pe_number=2,
#                                         metabolites=[],
#                                         overwrite_config_file=True)
#
#     PE.write_config_file()
#     # PE.setup()
#     # PE.run()
#
#     viz.PlotTimeCourseEnsemble(PE, savefig=True)
#
#
#
#
#
#
#


























































