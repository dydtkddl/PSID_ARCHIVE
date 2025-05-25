import rdkit
from rdkit import Chem
from rdkit.Chem import Descriptors, AllChem
import CoolProp.CoolProp as CP
import psi4
from ase.build import molecule
from thermo import Chemical

def calculate_properties(smiles, name):
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

        # 6. 압축성
        compressibility = CP.PropsSI('Z', 'T', 298.15, 'P', 101325, name)
        result["Compressibility factor"] = compressibility

        # 7. 헨리 상수
        henry_constant = CP.PropsSI('Hmolar', 'T', 298.15, 'P', 101325, name)
        result["Henry's constant (mol/m^3/Pa)"] = henry_constant
    except Exception as e:
        result["CoolProp properties"] = f"Error: {str(e)}"

    try:
        # Thermo를 사용한 물성 계산
        chem = Chemical(name)
        result["Boiling point (K)"] = chem.Tb
        result["Melting point (K)"] = chem.Tm
    except Exception as e:
        result["Thermo properties"] = f"Error: {str(e)}"

    # ASE를 사용한 분자 구조
    try:
        ase_molecule = molecule(name)
        result["ASE molecular structure"] = ase_molecule
    except Exception as e:
        result["ASE molecular structure"] = f"Error: {str(e)}"

    return result