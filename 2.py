# -*- coding: mbcs -*-
# Do not delete the following import lines
from abaqus import *
from abaqusConstants import *
import __main__
import csv
from odb2vtk import *
# def apply_stress_to_vtu_cells(stress_mapping_file, model_name):
#     # Read the stress mapping values

    
    # Apply the DiscreteField to the corresponding region in the model
def delete_existing_loads_and_surfaces(model):
    # Delete existing loads
    for load_name in model.loads.keys():
        del model.loads[load_name]
    
    # Delete existing surfaces
    for surface_name in model.rootAssembly.surfaces.keys():
        del model.rootAssembly.surfaces[surface_name]


def Macro1():
    import section
    import regionToolset
    import displayGroupMdbToolset as dgm
    import part
    import material
    import assembly
    import step
    import interaction
    import load
    import mesh
    import optimization
    import job
    import sketch
    import visualization
    import xyPlot
    import displayGroupOdbToolset as dgo
    import connectorBehavior
    openMdb(pathName='C:/Users/user/Desktop/Somdeb/doing_work.cae')
    session.viewports['Viewport: 1'].setValues(displayedObject=None)
    a = mdb.models['mesh_165000'].rootAssembly
    session.viewports['Viewport: 1'].setValues(displayedObject=a)
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=ON, bcs=ON, 
        predefinedFields=ON, connectors=ON, optimizationTasks=OFF, 
        geometricRestrictions=OFF, stopConditions=OFF)

    delete_existing_loads_and_surfaces(mdb.models['mesh_165000'])

    # session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Step-1')
    # a = mdb.models['mesh_165000'].rootAssembly
    # s1 = a.instances['mergePart-1'].faces
    # side1Faces1 = s1.getSequenceFromMask(mask=('[#f ]', ), )
    # region = a.Surface(side1Faces=side1Faces1, name='Surf-1')
    # mdb.models['mesh_165000'].Pressure(name='Load-1', createStepName='Step-1', 
    #     region=region, distributionType=UNIFORM, field='', magnitude=1.0, 
    #     amplitude=UNSET)

    job_name = 'okaho_job'
    surface_index = 0
    with open(r'C:\Users\user\Desktop\Somdeb\coupling\stress_mapping.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if 'file_name' in row and row['file_name']:
                job_name = row['file_name'].replace('.vtk', '')
            vtu_cell_id = int(row['vtu_cell_id'])
            stress_value = float(row['stress_value'])
            if stress_value != 0.0:
                # Create surface name dynamically
                surface_name = 'surf-mesh_'+str(surface_index)
                
                # Get the element from its ID
                abaqus_cell_id = vtu_cell_id + 1
                element = a.instances['mergePart-1'].elements.sequenceFromLabels(labels=[abaqus_cell_id])
                
                # Create surface
                a.Surface(face3Elements=element, name=surface_name)
                
                # Get the region of the created surface
                region = a.surfaces[surface_name]
                
                # Create load name dynamically
                load_name = 'load-mesh_'+str(surface_index)
                
                # Apply pressure load to the surface
                mdb.models['mesh_165000'].Pressure(name=load_name, createStepName='Step-1', 
                    region=region, distributionType=UNIFORM, field='', magnitude=stress_value, 
                    amplitude=UNSET)
                
                # Increment surface index
                surface_index +=1


    # mdb.models['mesh_165000'].DiscreteField(name='DiscField-1', description='', 
    #     location=ELEMENTS, fieldType=SCALAR, dataWidth=1, defaultValues=(0.0, 
    #     ), data=(('', 1, (1, ), (1.0, )), ))
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=ON)
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=OFF, bcs=OFF, 
        predefinedFields=OFF, connectors=OFF)
    # mdb.models['mesh_165000'].loads['Load-1'].setValues(
    # distributionType=DISCRETE_FIELD, field='DiscField-1')
    mdb.Job(name=job_name, model='mesh_165000', description='', type=ANALYSIS, 
        atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
        memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
        explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
        modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
        scratch='', resultsFormat=ODB, multiprocessingMode=DEFAULT, numCpus=1, 
        numGPUs=0)
    mdb.jobs[job_name].writeInput(consistencyChecking=OFF)
    mdb.jobs[job_name].submit(consistencyChecking=OFF)
    session.mdbData.summary()
    ConvertOdb2VtkP('C:/Users/user/Desktop/Somdeb/coupling/odb_vtk', job_name, 'C:/Users/user/Desktop/Somdeb/coupling/odb_vtk','10', 
    '2', '10', '10', '0','0')
   

Macro1()