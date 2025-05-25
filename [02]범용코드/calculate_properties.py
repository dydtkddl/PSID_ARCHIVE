import rdkit
from rdkit import Chem
from rdkit.Chem import Descriptors, AllChem
import CoolProp.CoolProp as CP
import psi4
from ase.build import molecule
from thermo import Chemical

def calculate_boiling_and_melting_points(chemical_name, pressure):
    """
    주어진 화학물질의 특정 압력에서의 끓는점과 표준 압력에서의 녹는점을 계산합니다.
    
    :param chemical_name: 화학물질 이름 (예: 'water', 'ethanol')
    :param pressure: 압력 (Pa)
    :return: 끓는점 (K), 녹는점 (K)
    """
    chem = Chemical(chemical_name)
    boiling_point = chem.Tsat(P=pressure)
    melting_point = chem.Tm  # 표준 압력(1 atm)에서의 녹는점
    return boiling_point, melting_point
def calculate_properties(smiles, name, pressure, temperature ):
    print(f"Calculating properties for {name} (SMILES: {smiles})")
    
    result = {"name": name, "SMILES": smiles}
    
    # RDKit 분자 생성 및 3D 좌표 계산
    mol = Chem.MolFromSmiles(smiles)
    mol = Chem.AddHs(mol)
    AllChem.EmbedMolecule(mol)
    AllChem.UFFOptimizeMolecule(mol)

    # 1. 분자량
    molecular_weight = Descriptors.MolWt(mol)
    result["Molecular weight (g/mol)"] = molecular_weight

    # 2. 극성 관련 정보
    h_donors = Descriptors.NumHDonors(mol)
    h_acceptors = Descriptors.NumHAcceptors(mol)
    result["H-bond donors"] = h_donors
    result["H-bond acceptors"] = h_acceptors

    # 3. 쌍극자 모멘트 계산 (Psi4)
    try:
        conf = mol.GetConformer()
        num_atoms = mol.GetNumAtoms()
        xyz_string = f"{num_atoms}\n\n"
        for i in range(num_atoms):
            pos = conf.GetAtomPosition(i)
            symbol = mol.GetAtomWithIdx(i).GetSymbol()
            xyz_string += f"{symbol} {pos.x:.4f} {pos.y:.4f} {pos.z:.4f}\n"
        
        psi4.geometry(xyz_string)
        psi4.set_options({'basis': '6-31G(d)'})
        energy, wavefunction = psi4.energy('scf', return_wfn=True)
        dipole_moment = wavefunction.variable('SCF DIPOLE')
        result["Dipole moment (D)"] = dipole_moment
    except Exception as e:
        result["Dipole moment (D)"] = f"Error: {str(e)}"

    # 4. 분자 표면적
    mol_surface_area = Descriptors.TPSA(mol)
    result["Molecular surface area (Å^2)"] = mol_surface_area

    # CoolProp 및 Thermo를 사용한 물성 계산
    try:
        # 5. 임계 온도
        critical_temp = CP.PropsSI('Tcrit', name)
        result["Critical temperature (K)"] = critical_temp
    except Exception as e:
        result["Critical temperature (K)"] = "error"
    try:
        # 6. 압축성  상온 상압
        compressibility = CP.PropsSI('Z', 'T', 298.15, 'P', 101325, name)
        result["Compressibility factor (상온,상압)"] = compressibility
    except Exception as e:
        result["Compressibility factor (상온,상압)"] = "error"
    try:
        # 7. Hmolar 상온 상압
        Hmolar = CP.PropsSI('Hmolar', 'T', 298.15, 'P', 101325, name)
        result["Hmolar (상온,상압)"] = Hmolar
    except Exception as e:
        result["Hmolar (상온,상압)"] = "error"
    try:
        # 6. 압축성  주어진 온도, 압력
        compressibility = CP.PropsSI('Z', 'T', temperature, 'P', pressure, name)
        result[f"Compressibility factor 주어진 압력, 온도"] = compressibility
    except Exception as e:
        result[f"Compressibility factor 주어진 압력, 온도"] = "error"
    try:
        # 7. Hmolar 주어진 온도, 압력
        Hmolar = CP.PropsSI('Hmolar', 'T', temperature, 'P', pressure, name)
        result[f"Hmola 주어진 압력, 온도"] = Hmolar
    except Exception as e:
        result[f"Hmola 주어진 압력, 온도"] = "error"

    try:
        # Thermo를 사용한 물성 계산
        chem = Chemical(name)
        result["Boiling point at 1atm (K)"] = chem.Tb
        result["Melting point at 1atm (K)"] = chem.Tm
    except Exception as e:
        result["Boiling point at 1atm (K)"] = "error"
        result["Melting point at 1atm (K)"] = "error"
    try:    
        boiling_point, melting_point = calculate_boiling_and_melting_points(name,pressure)
        result["Boiling point at 주어진압력 (K)"] = boiling_point    
        result["Melting point at 주어진압력 (K)"] = melting_point    
    except:
        result["Boiling point at 주어진압력 (K)"] = "error"    
        result["Melting point at 주어진압력 (K)"] = "error"    

    # ASE를 사용한 분자 구조
    try:
        ase_molecule = molecule(name)
        result["ASE molecular structure"] = ase_molecule
    except Exception as e:
        result["ASE molecular structure"]  = "error"

    return result
##############
## 예시 코드 ## 
##############
# import calculate_properties
# import pandas as pd
# import numpy as np

# molecule_properties = []
# molecule_list = ["CO2", "O2"]
# smile_molecule_list = ["O=C=O", "O=O"]
# pressure_list = [50000, 100000,500000,1500000]
# temperature_list = [20+ 273.15]
# for smile , molecule in zip(smile_molecule_list, molecule_list):
#     for temp in temperature_list:
#         for pressure in pressure_list:
#             temporary_dict = {}
#             temporary_dict = {"molecule" : molecule }
#             temporary_dict["Temperature"]= temp
#             temporary_dict["Pressure"]=pressure
#             properties = calculate_properties.calculate_properties(smile, molecule, pressure, temp)
#             for key, value in properties.items():
#                 temporary_dict[key] = value 
#             molecule_properties.append(temporary_dict)