import xml.etree.ElementTree as ET

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

# Example usage
pvtu_file = 'C:/Users/user/Desktop/Somdeb/coupling/odb_vtk/Job-4_Step-1_f010.pvtu'
vtu_files = extract_vtu_filenames_from_pvtu(pvtu_file)

for vtu_file in vtu_files:
    print(vtu_file)
