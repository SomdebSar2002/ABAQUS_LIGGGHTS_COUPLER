import vtk
import csv
import math

def extract_cell_centers_with_ids(dataset):
    cell_centers_filter = vtk.vtkCellCenters()
    cell_centers_filter.SetInputData(dataset)
    cell_centers_filter.Update()
    cell_centers = cell_centers_filter.GetOutput()
    points = cell_centers.GetPoints()

    centers_with_ids = []
    for i in range(points.GetNumberOfPoints()):
        center = points.GetPoint(i)
        centers_with_ids.append((i, center))

    return centers_with_ids

def extract_stress_average(dataset):
    stress_array = dataset.GetCellData().GetArray("normal_stress_average")
    stress_dict = {}
    for i in range(stress_array.GetNumberOfTuples()):
        stress_dict[i] = stress_array.GetValue(i)
    return stress_dict

def read_vtk_file(filename):
    reader = vtk.vtkPolyDataReader()
    reader.SetFileName(filename)
    reader.Update()
    return reader.GetOutput()

def read_vtu_file(filename):
    reader = vtk.vtkXMLUnstructuredGridReader()
    reader.SetFileName(filename)
    reader.Update()
    return reader.GetOutput()

def euclidean_distance(coord1, coord2):
    return math.sqrt(sum((c1 - c2) ** 2 for c1, c2 in zip(coord1, coord2)))

def find_nearest_vtu_center(vtk_center, vtu_centers):
    min_distance = float('inf')
    nearest_vtu_id = -1
    
    for vtu_id, vtu_center in vtu_centers:
        distance = euclidean_distance(vtk_center, vtu_center)
        if distance < min_distance:
            min_distance = distance
            nearest_vtu_id = vtu_id
    
    return nearest_vtu_id

def write_results_to_csv_and_dict(vtk_centers, vtu_centers, vtk_stress, output_file):
    results_dict = {}
    
    with open(output_file, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        header = ["vtk_cell_id", "vtu_cell_id", "vtk_stress_average"]
        csvwriter.writerow(header)

        for vtk_id, vtk_center in vtk_centers:
            nearest_vtu_id = find_nearest_vtu_center(vtk_center, vtu_centers)
            stress_average = vtk_stress[vtk_id]
            row = [vtk_id, nearest_vtu_id, stress_average]
            csvwriter.writerow(row)
            results_dict[vtk_id] = {
                "vtu_cell_id": nearest_vtu_id,
                "vtk_stress_average": stress_average
            }
    
    return results_dict

# Example usage
vtk_file = 'input.vtk'
vtu_file = 'input.vtu'
output_file = 'cell_mapping_with_stress.csv'

# Read the VTK and VTU files
vtk_data = read_vtk_file(vtk_file)
vtu_data = read_vtu_file(vtu_file)

# Extract cell centers and their IDs
vtk_centers_with_ids = extract_cell_centers_with_ids(vtk_data)
vtu_centers_with_ids = extract_cell_centers_with_ids(vtu_data)

# Extract stress average from VTK file
vtk_stress_average = extract_stress_average(vtk_data)

# Write the results to a CSV file and a dictionary
results_dict = write_results_to_csv_and_dict(vtk_centers_with_ids, vtu_centers_with_ids, vtk_stress_average, output_file)

print(f"Results have been written to {output_file}")
print("Results dictionary:")
print(results_dict)
