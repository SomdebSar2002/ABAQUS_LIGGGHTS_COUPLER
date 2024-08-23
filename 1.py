import sys
import vtk
import csv

def read_cell_mapping(file_path):
    cell_mapping = {}
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            vtk_cell_id = int(row['vtk_cell_id'])
            vtu_cell_id = int(row['vtu_cell_id'])
            cell_mapping[vtk_cell_id] = vtu_cell_id
    return cell_mapping

def read_stress_from_vtk(file_path):
    stress_dict = {}
    reader = vtk.vtkPolyDataReader()
    reader.SetFileName(file_path)
    reader.Update()
    polydata = reader.GetOutput()
    stress_array = polydata.GetCellData().GetArray("normal_stress_average")
    for i in range(stress_array.GetNumberOfTuples()):
        stress_dict[i] = stress_array.GetValue(i)
    return stress_dict

def generate_stress_mapping(cell_mapping_file, vtk_file, output_file, vtk_file_name):
    cell_mapping = read_cell_mapping(cell_mapping_file)
    vtk_stress = read_stress_from_vtk(vtk_file)

    with open(output_file, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        header = ["vtu_cell_id", "stress_value","file_name"]
        csvwriter.writerow(header)
        i = 1
        for vtk_cell_id, vtu_cell_id in cell_mapping.items():
            stress_value = vtk_stress.get(vtk_cell_id, 0.0)
            if i:
                csvwriter.writerow([vtu_cell_id, stress_value,vtk_file_name])
            else:
                csvwriter.writerow([vtu_cell_id, stress_value])
            i=0

if __name__ == '__main__':
    # Get the VTK file path from command-line arguments
    if len(sys.argv) != 3:
        print("Usage: python 1.py <vtk_file_path>")
        sys.exit(1)
    
    vtk_file_path = sys.argv[1]
    vtk_file_name = sys.argv[2]
    # vtk_file_path =r'C:\Users\user\Desktop\Somdeb\coupling\ok\mesh_86000.vtk'
    # vtk_file_name = 'mesh_86000.vtk'
    # Paths for the cell mapping file and the output file
    cell_mapping_file = 'C:/Users/user/Desktop/Somdeb/coupling/okaho/cell_mapping.csv'
    output_file = 'C:/Users/user/Desktop/Somdeb/coupling/stress_mapping.csv'

    # Generate the stress mapping for the provided VTK file
    generate_stress_mapping(cell_mapping_file, vtk_file_path, output_file, vtk_file_name)
