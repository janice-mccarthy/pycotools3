# PyCoTools

Package was developed by Ciaran Welsh (c.welsh2@newcastle.ac.uk) at Newcastle University, UK. 

## Installation 
Use:
    `pip install PyCoTools` 
        
## Version 
        
This package was developed on Python 2.7 and Copasi version 19. This is a beta version of PyCoTools that is being actively developed. If you happen to find any bugs please feel free to get in contact. 

## jupyter notebook tutorial
The tutorials are being actively developed. Some of them are available under the [tutorials] (https://github.com/CiaranWelsh/PyCoTools/tree/CopasiVersion19/PyCoTools/PyCoToolsTutorial)


## pycopi

The `pycopi` module is a set of python classes for interfacing with copasi via python. 

This can be used when a user wantes to setup an anaysis not native to COPASI, as exemplified by the `pydentify2` module.


    Features include:
        - `GetModelQuantites`     - Class to retrieving information about model 
                                  and model entities
        
        - `Reports`               - Automate the setting up of specific and commonly used reports
        
        - `ParameterEstimation`   - Automate the setting up of a parameter estimation in copasi. 
                                
                                  - Run a parameter estiamtion through copasi Via python and visualize 
                                  the results
        
        - `ExperimentMapper`      - Automate the process of mapping model species to experimental data. 
                                    Used by ParameterEstimation class
        
        - `TimeCourse`            - Simulate a time course using Copasi. Parse this data into python 
                                    and plot it optionally. 
        
        - `PhaseSpace`            - Produce plots in phase space.
        
        - `Scan`                  - Automate the process of setting up a parameter scan. All three 
                                    scan, repeat and random number generation) are supported. 
        
        - `Run`                   - Submit copasi file to CopasiSE. Unticks all 'executable boxes' then ticks 
                                  the executable box of interest. 
       
        - `InsertParameters`      - Take parameters from pandas.DataFrame, python dict or from csv/txt files (output from copasi) 
                                  put them into the model. Note: A known bug exists where if you have parameter 
                                  sets in your copasi file then these get changed instead of the active parameters. 
                                  
## PEAnalysis

The `PEAnalysis` module provides a number of convenient classes for visualizing and analysing parameter estimation data. The module can be used with any PE data regardless of origin but has been developed with copasi in  mind.
    
    Features Include:
        
        - `ParsePEData`           - Read data from a single parameter estimation file (Copasi output) 
                                  or a folder of parameter estimation files
        
        - `WritePEData`           - Output Parameter estiation data back to file in more convenient format
        
        - `TruncateData`          - Parameter estimations often find local minima. These can be truncated 
                                  from further analysis by either specifying how many percent (i.e. top 1%)
                                  or what value you would like to use as cut-off, i.e <1e2). 
                                  This class is used implicitely within the plotting classes and an 
                                  interface is provided as an option.
        
        - `Histogram`         - Plot histogram for each parameter in your estiation file
        
        - `Scatters`          - Plot all combinations of scatter graph
        
        - `Boxplots`          - visualize variance with box plots
        
        - `RssVsIteration`    - evaluate optimization performance with plot of (ordered) 
                                        likelihood Vs iteration. The flatter the graph the better. 
        - `Pca`               - Principle component analysis on PE data

	- `LinearRegression`  - Lasso regression on PE data 
 
## Pydentify     

The `pydentify` module uses the `pycopi` module to fully automate the process outlined by Schaber 2012: Easy Identifiability Analysis in Copasi. 
   
    Features Include:
        
        - `ProfileLikelihood`     - Setup and run profile likleihood for a model around current parameters
                                
                                  - Optionally take parameters from a file (copasi output file for example) 
                                    and perform profile likelihood around these parameters
                                
                                  - Optionally take multiple sets of parameters from parameter estimation output 
                                    file and perform profile likelihoods around each of them. 
                                
                                  - Optionally run on a cluster (sun grid engine is implemented but modular 
                                    nature of the code means this bit can be replaced by code for any job scheduler)

        - `Plot`                  - Plotting facilities for profile likleihood output. 
        
                                  - Chi2 based confidence interval is automatically calculated and 
                                    plotted as red dotted line for determining identifiability status.

                                  - Choose the x and y variables
                                    
  


