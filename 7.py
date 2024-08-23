import os
import sys
import xml.etree.ElementTree as ET
import vtk

def extract_vtu_filenames_from_pvtu(pvtu_file):
    # Parse the PVTU file
    tree = ET.parse(pvtu_file)
    root = tree.getroot()

    # Extract the VTU file names from the Piece elements
    vtu_files = []
    for piece in root.findall(".//Piece"):
        vtu_file = piece.get("Source")
        if vtu_file:
            vtu_files.append(vtu_file)
    
    return vtu_files

def read_vtk_cell_center(vtk_file, cell_id):
    # Read the VTK file
    reader = vtk.vtkPolyDataReader()
    reader.SetFileName(vtk_file)
    reader.Update()
    
    polydata = reader.GetOutput()
    cell = polydata.GetCell(cell_id)
    points = cell.GetPoints()
    center = [0.0, 0.0, 0.0]
    for i in range(points.GetNumberOfPoints()):
        p = points.GetPoint(i)
        center = [center[j] + p[j] for j in range(3)]
    center = [c / points.GetNumberOfPoints() for c in center]
    
    return center

def read_vtu_cell_center(vtu_file, cell_id):
    # Read the VTU file
    reader = vtk.vtkXMLUnstructuredGridReader()
    reader.SetFileName(vtu_file)
    reader.Update()
    
    unstructured_grid = reader.GetOutput()
    cell = unstructured_grid.GetCell(cell_id)
    points = cell.GetPoints()
    center = [0.0, 0.0, 0.0]
    for i in range(points.GetNumberOfPoints()):
        p = points.GetPoint(i)
        center = [center[j] + p[j] for j in range(3)]
    center = [c / points.GetNumberOfPoints() for c in center]
    
    return center

def calculate_translation_vector(vtk_file, vtk_cell_id, vtu_file, vtu_cell_id):
    vtk_center = read_vtk_cell_center(vtk_file, vtk_cell_id)
    vtu_center = read_vtu_cell_center(vtu_file, vtu_cell_id)
    
    translation_vector = [vtk_center[i] - vtu_center[i] for i in range(3)]
    
    return translation_vector

def translate_vtu(input_vtu, output_vtu, translation_vector):
    # Read the VTU file
    reader = vtk.vtkXMLUnstructuredGridReader()
    reader.SetFileName(input_vtu)
    reader.Update()
    
    # Get the output of the reader
    unstructured_grid = reader.GetOutput()

    # Create a transform filter
    transform = vtk.vtkTransform()
    transform.Translate(translation_vector)

    transform_filter = vtk.vtkTransformFilter()
    transform_filter.SetInputData(unstructured_grid)
    transform_filter.SetTransform(transform)
    transform_filter.Update()

    # Write the translated VTU file
    writer = vtk.vtkXMLUnstructuredGridWriter()
    writer.SetFileName(output_vtu)
    writer.SetInputData(transform_filter.GetOutput())
    writer.Write()

def translate_vtus_in_pvtu(pvtu_file, vtk_file, vtk_cell_id, vtu_cell_id):
    vtu_files = extract_vtu_filenames_from_pvtu(pvtu_file)
    
    pvtu_dir = os.path.dirname(pvtu_file)
    translated_vtu_files = []

    # Calculate translation vector based on the first VTU file
    first_vtu_file = os.path.join(pvtu_dir, vtu_files[0])
    translation_vector = calculate_translation_vector(vtk_file, vtk_cell_id, first_vtu_file, vtu_cell_id)

    for vtu_file in vtu_files:
        input_vtu = os.path.join(pvtu_dir, vtu_file)
        output_vtu = os.path.join(pvtu_dir, vtu_file)
        translate_vtu(input_vtu, output_vtu, translation_vector)
        translated_vtu_files.append(output_vtu)
    
    return translated_vtu_files

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print("Usage: python 3.py <pvtu_file_path> <vtk_file_path> <vtk_cell_id> <vtu_cell_id>")
        sys.exit(1)
    
    pvtu_file_path = sys.argv[1]
    vtk_file_path = sys.argv[2]
    vtk_cell_id = int(sys.argv[3])
    vtu_cell_id = int(sys.argv[4])

    translate_vtus_in_pvtu(pvtu_file_path, vtk_file_path, vtk_cell_id, vtu_cell_id)
