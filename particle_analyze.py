from ovito.io import import_file
from ovito.modifiers import *
from ovito.data import *

import glob
import os
import numpy as np

processed_id = os.getenv("process_id")
path_xyz = os.getenv("path_xyz")

md_data = np.genfromtxt(os.path.join(os.path.dirname(path_xyz), "d.dat"), dtype=None)
first_column = np.array([row[0] for row in md_data])

f = open("tmp_%s/tmp.dat" % processed_id, "w")

for xyz_file in glob.glob("tmp_%s/xyz/*.xyz" % processed_id):

    i_sim = os.path.basename(xyz_file).split(".")[0]
    mask = first_column == int(i_sim.split("_")[1])

    n_steps = md_data[mask][0][3]
    initial_temperature = md_data[mask][0][4]

    node = import_file(xyz_file)

    node.modifiers.append(ConstructSurfaceModifier())
    node.modifiers.append(CommonNeighborAnalysisModifier())
    node.modifiers.append(BondAngleAnalysisModifier())
    node.modifiers.append(CentroSymmetryModifier())

    data = node.compute()
    pos = data.particle_properties.position.array
    n_atoms = pos.shape[0]
    epot = data.particle_properties['epot'].array
    box = data.cell.matrix.diagonal()

    surface_area = node.output.attributes['ConstructSurfaceMesh.surface_area']
    solid_volume = node.output.attributes['ConstructSurfaceMesh.solid_volume']
        
    cna_others = node.output.attributes['CommonNeighborAnalysis.counts.OTHER']
    cna_fcc = node.output.attributes['CommonNeighborAnalysis.counts.FCC']
    cna_hcp = node.output.attributes['CommonNeighborAnalysis.counts.HCP']
    cna_bcc = node.output.attributes['CommonNeighborAnalysis.counts.BCC']
    cna_ico = node.output.attributes['CommonNeighborAnalysis.counts.ICO']

    bond_angle_others = node.output.attributes['BondAngleAnalysis.counts.OTHER']
    bond_angle_fcc = node.output.attributes['BondAngleAnalysis.counts.FCC']
    bond_angle_hcp = node.output.attributes['BondAngleAnalysis.counts.HCP']
    bond_angle_bcc = node.output.attributes['BondAngleAnalysis.counts.BCC']
    bond_angle_ico = node.output.attributes['BondAngleAnalysis.counts.ICO']

    csp = np.mean(node.output.particle_properties['Centrosymmetry'].array)

    print(i_sim, n_atoms, n_steps, initial_temperature, np.sum(epot), surface_area, solid_volume, cna_others, cna_fcc, cna_hcp, cna_bcc, cna_ico, bond_angle_others, bond_angle_fcc, bond_angle_hcp, bond_angle_bcc, bond_angle_ico, csp, sep="\t", file=f)
f.close()
