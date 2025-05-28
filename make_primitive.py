import pymatgen
from pymatgen.core import Structure
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
print(1)
structure = Structure.from_file("LAFRAN01_clean.cif")

print(1)
# 대칭 기반 primitive cell 추출
sga = SpacegroupAnalyzer(structure, symprec=1e-3)
print(1)
primitive = sga.find_primitive()
# primitive = structure.get_primitive_structure()
print(1)
primitive.to(filename="LAFRAN01_primitive.cif")
print(f"원자 수: {len(structure)} → {len(primitive)} (primitive cell)")
