elem_dict = {
"H" : 	1, \
"He":	2, \
"Li":	3, \
"Be":	4, \
"B" :	5, \
"C" :	6, \
"N" :	7, \
"O" :	8, \
"F" :	9, \
"Ne":	10, \
"Na":	11, \
"Mg":	12, \
"Al":	13, \
"Si":	14, \
"P" :	15, \
"S" :	16, \
"Cl":	17, \
"Ar":	18, \
"K" :	19, \
"Ca":	20, \
"Sc":	21, \
"Ti":	22, \
"V" :	23, \
"Cr":	24, \
"Mn":	25, \
"Fe":	26, \
"Co":	27, \
"Ni":	28, \
"Cu":	29, \
"Zn":	30, \
"Ga":	31, \
"Ge":	32, \
"As":	33, \
"Se":	34, \
"Br":	35, \
"Kr":	36, \
"Rb":	37, \
"Sr":	38, \
"Y" :	39, \
"Zr":	40, \
"Nb":	41, \
"Mo":	42, \
"Tc":	43, \
"Ru":	44, \
"Rh":	45, \
"Pd":	46, \
"Ag":	47, \
"Cd":	48, \
"In":	49, \
"Sn":	50, \
"Sb":	51, \
"Te":	52, \
"I" :	53, \
"Xe":	54, \
"Cs":	55, \
"Ba":	56, \
"La":	57, \
"Ce":	58, \
"Pr":	59, \
"Nd":	60, \
"Pm":	61, \
"Sm":	62, \
"Eu":	63, \
"Gd":	64, \
"Tb":	65, \
"Dy":	66, \
"Ho":	67, \
"Er":	68, \
"Tm":	69, \
"Yb":	70, \
"Lu":	71, \
"Hf":	72, \
"Ta":	73, \
"W" :	74, \
"Re":	75, \
"Os":	76, \
"Ir":	77, \
"Pt":	78, \
"Au":	79, \
"Hg":	80, \
"Tl":	81, \
"Pb":	82, \
"Bi":	83, \
"Po":	84, \
"At":	85, \
"Rn":	86, \
"Fr":	87, \
"Ra":	88, \
"Ac":	89, \
"Th":	90, \
"Pa":	91, \
"U" :	92, \
"Np":	93, \
"Pu":	94, \
"Am":	95, \
"Cm":	96, \
"Bk":	97, \
"Cf":	98, \
"Es":	99, \
"Fm":	100, \
"Md":	101, \
"No":	102, \
"Lr":	103, \
"Rf":	104, \
"Db":	105, \
"Sg":	106, \
"Bh":	107, \
"Hs":	108, \
"Mt":	109, \
"Ds":	110, \
"Rg":	111, \
"Cn":	112, \
"Nh":	113, \
"Fl":	114, \
"Mc":	115, \
"Lv":	116, \
"Ts":	117, \
"Og":	118}
import os
import numpy as np
import tkinter
import tkinter.messagebox
from tkinter import filedialog
from tkinter import ttk
import math
import matplotlib.pyplot as plt

gui = tkinter.Tk()
gui.geometry("600x500")
gui.title("PDOS plot")

def getFolderPath():
    folder = filedialog.askdirectory()
    folderPath.set(folder)

def RunProgram():
    print("Entering RunProgram function")
    print("=====================================================================")
    global spin_available
    global BOCA_pairs
    global atomic_symbols_list
    global num_BOs_available
    global BO_available_list
    global natoms
    global norbitals
    global npairs
    global SBO_spin_up
    global SBO_spin_down
    global SBO
    global orbital_energies
    global orbital_s_spin_up
    global orbital_p_spin_up
    global orbital_d_spin_up
    global orbital_f_spin_up
    global orbital_g_spin_up
    global orbital_sum_spin_up
    global orbital_s_spin_down
    global orbital_p_spin_down
    global orbital_d_spin_down
    global orbital_f_spin_down
    global orbital_g_spin_down
    global orbital_sum_spin_down
    global orbital_s
    global orbital_p
    global orbital_d
    global orbital_f
    global orbital_g
    global orbital_sum
    global empty_s_spin_up
    global empty_p_spin_up
    global empty_d_spin_up
    global empty_f_spin_up
    global empty_g_spin_up
    global empty_sum_spin_up
    global empty_s_spin_down
    global empty_p_spin_down
    global empty_d_spin_down
    global empty_f_spin_down
    global empty_g_spin_down
    global empty_sum_spin_down
    global empty_s
    global empty_p
    global empty_d
    global empty_f
    global empty_g
    global empty_sum
    global BOCs_spin_up
    global BOCs_spin_down
    global BOCs
    global mydir
    global natoms
    global is_BOCA_path
    atomic_symbols_list = []
    mydir = folderPath.get()
    ###########Block for matching the atomic symbol
    atomvol_path = os.path.join(mydir, 'DDEC_atom_volumes.xyz')
    is_atomvol_path = os.path.isfile(atomvol_path)
    if is_atomvol_path:
        atomvol_file = open(atomvol_path, 'r')
        content = atomvol_file.readlines()
        line = content[0]
        natoms = int(line.split()[0])
        atomic_symbols = []
        for i in range(natoms):
            line = content[i+2]
            atomic_symbols.append(line.split()[0])
        print('natoms = ', natoms)
        print('atomic_symbols = ', atomic_symbols)
        atomic_numbers = []
        for elem1 in atomic_symbols:
            for elem2, value in elem_dict.items():
                if elem1 == elem2:
                    atomic_numbers.append(value)
        print("Atomic number of atoms: ", atomic_numbers)
        atomvol_file.close()
    else:
        print("DDEC_atom_volumes.xyz is not in the directory you browsed, make sure you have it in the directory you are browsing")
        tkinter.messagebox.showerror(title="ERROR", message="DDEC_atom_volumes.xyz file was not found, make sure you have it in the directory you are browsing and start the program again")
        raise SystemExit()
    ##########Block for orbitals_info.txt
    orbinfo_path = os.path.join(mydir, 'orbitals_info.txt')
    is_orbinfo_path = os.path.isfile(orbinfo_path)
    if is_orbinfo_path:
        orbinfo_file = open(orbinfo_path, 'r')
        for line in orbinfo_file:
            if line.startswith("norbitals"):
                temp_string_list = line.split()
                norbitals  = int(temp_string_list[-1])
                print("norbitals = ", norbitals)
            if line.startswith("orbital_energies_available"):
                temp_string_list = line.split()
                orbital_energies_available = temp_string_list[-1]
                if orbital_energies_available == "T":
                    print("Energies available")
                elif orbital_energies_available == "F":
                    print("A PDOS plot cannot be constructed for this type of calculation because there are no orbital eigenenergies")
                    tkinter.messagebox.showerror(title="ERROR", message="A PDOS plot cannot be generated as there are no orbital energies available.")
                    raise SystemExit()
            if line.startswith("spin_available"):
                temp_string_list = line.split()
                spin_available = temp_string_list[-1]
                if spin_available == "T":
                    print("Spin available")
                elif spin_available == "F":
                    print("Spin not available")
        orbinfo_file.close()
    else:
        print("orbitals_info.xyz is not in the directory you browsed, make sure you have it in the directory you are browsing")
        tkinter.messagebox.showerror(title="ERROR", message="orbitals_info.xyz file was not found, make sure you have it in the directory you are browsing and start the program again")
        raise SystemExit()
    ###########Loops to get orbital energies if spin polarized or spin non-polarized
    ###Initializing arrays 
    orbinfo_file = open(orbinfo_path, 'r')
    orbital_energies =  np.zeros((norbitals), dtype = float)
    content = orbinfo_file.readlines()
    ###For spin polarized
    if spin_available == 'T':
        occupancies_spin_up = np.zeros((norbitals), dtype = float)
        occupancies_spin_down = np.zeros((norbitals), dtype = float)
        for i in range(norbitals):
            line = content[i+6]
            temp_string_list = line.split()
            if (int(temp_string_list[0]) != i+1):
                print("Orbital numbers mismatched. Program will terminate.")
                quit()
            occupancies_spin_up[i] = float(temp_string_list[1])
            occupancies_spin_down[i] = float(temp_string_list[2])
            orbital_energies[i] = float( temp_string_list[3])
        #print('occupancies spin up = ', occupancies_spin_up)
        #print('occupancies spin down = ', occupancies_spin_down)
        #print('orbital energies = ', orbital_energies)
    ###For spin non-polarized
    if spin_available == 'F':
        occupancies = np.zeros((norbitals), dtype = float)
        for i in range(norbitals):
            line = content[i+6]
            temp_string_list = line.split()
            if (int(temp_string_list[0]) != i+1):
                print("Orbital numbers mismatched. Program will terminate.")
                quit()
            occupancies[i] = float(temp_string_list[1])
            orbital_energies[i] = float(temp_string_list[2])
        print('occupancies = ', occupancies)
        print('orbital energies = ', orbital_energies)
    orbinfo_file.close()
    ##########Block for pairs
    BOCA_path = os.path.join(mydir, 'BOCA.txt')
    is_BOCA_path = os.path.isfile(BOCA_path)
    if is_BOCA_path:
        BOCA_file = open(BOCA_path, 'r')
        BOCA_pairs = []
        for line in BOCA_file:
            if line.startswith('The BOCA for atom'):
                temp_string_list = line.split()
                pair = ([int(temp_string_list[4]), int(temp_string_list[7])])
                atom1 = int(temp_string_list[4])
                atom2 = int(temp_string_list[7])
                BOCA_pairs.append(pair)
        npairs = len(BOCA_pairs)
        print("BOCA pairs = ", BOCA_pairs)
        print("npairs = ",len(BOCA_pairs))
        BOCA_file.close()
        ############Initialize BOC arrays
        BOCA_file = open(BOCA_path, 'r')
        if spin_available == 'T':
            BOCs_spin_up = np.zeros((npairs, norbitals), dtype = float)
            BOCs_spin_down = np.zeros((npairs, norbitals), dtype = float)
            current_pair = 0
            line_active = False
            for line in BOCA_file:
                if line_active:
                    temp_string_list = line.split()
                    length_BOC = len(temp_string_list)
                    if length_BOC == 0:
                        line_active = False
                    else:
                        orb = int(temp_string_list[0])
                        BOCs_spin_up[current_pair-1][orb-1] = float(temp_string_list[3])
                        BOCs_spin_down[current_pair-1][orb-1] = float(temp_string_list[4])
                if line.startswith('orbital  spin'):
                    line_active = True
                    current_pair += 1
            
            BOCs = np.zeros((npairs, norbitals), dtype = float)
            BOCs = BOCs_spin_up + BOCs_spin_down
            
        ###For spin non-polarized
        if spin_available == 'F':
            BOCs = np.zeros((npairs, norbitals), dtype = float)
            current_pair = 0
            line_active = False
            for line in BOCA_file:
                if line_active:
                    temp_string_list = line.split()
                    length_BOC = len(temp_string_list)
                    if length_BOC == 0:
                        line_active = False
                    else:
                        orb = int(temp_string_list[0])
                        BOCs[current_pair-1][orb-1] = float(temp_string_list[2])
                if line.startswith('orbital  occupancy'):
                    line_active = True
                    current_pair += 1
            
    ###########Block for spdfg population
    spdfg_spin_up_path = os.path.join(mydir, 'spin_up_orbital_spdfg_populations.txt')
    is_spdfg_spin_up_path = os.path.isfile(spdfg_spin_up_path)
    spdfg_spin_down_path = os.path.join(mydir, 'spin_down_orbital_spdfg_populations.txt')
    is_spdfg_spin_down_path = os.path.isfile(spdfg_spin_down_path)
    spdfg_path = os.path.join(mydir, 'orbital_spdfg_populations.txt')
    is_spdfg_path = os.path.isfile(spdfg_path)

    
    if spin_available == 'T':
        if is_spdfg_spin_up_path and is_spdfg_spin_down_path:
            ##For spin-up
            spdfg_spin_up_file = open(spdfg_spin_up_path, 'r')
            orbital_s_spin_up = np.zeros((natoms + 1, norbitals), dtype = float)
            orbital_p_spin_up = np.zeros((natoms + 1, norbitals), dtype = float)
            orbital_d_spin_up = np.zeros((natoms + 1, norbitals), dtype = float)
            orbital_f_spin_up = np.zeros((natoms + 1, norbitals), dtype = float)
            orbital_g_spin_up = np.zeros((natoms + 1, norbitals), dtype = float)
            orbital_sum_spin_up = np.zeros((natoms + 1, norbitals), dtype = float)
            current_atom = 0
            line_active = False
            for line in spdfg_spin_up_file:
                if line_active:
                    temp_string_list = line.split()
                    length_spdfg = len(temp_string_list)
                    if length_spdfg == 0:
                        line_active = False
                    else:
                        orb = int(temp_string_list[0])
                        orbital_s_spin_up[current_atom-1][orb-1] = float(temp_string_list[2])
                        orbital_p_spin_up[current_atom-1][orb-1] = float(temp_string_list[3])
                        orbital_d_spin_up[current_atom-1][orb-1] = float(temp_string_list[4])
                        orbital_f_spin_up[current_atom-1][orb-1] = float(temp_string_list[5])
                        orbital_g_spin_up[current_atom-1][orb-1] = float(temp_string_list[6])
                        orbital_sum_spin_up[current_atom-1][orb-1] = float(temp_string_list[1])
                if line.startswith(' orbital       all'):
                    line_active = True
                    current_atom += 1
            spdfg_spin_up_file.close()
            
            ##For spin-down
            spdfg_spin_down_file = open(spdfg_spin_down_path, 'r')
            orbital_s_spin_down = np.zeros((natoms + 1, norbitals), dtype = float)
            orbital_p_spin_down = np.zeros((natoms + 1, norbitals), dtype = float)
            orbital_d_spin_down = np.zeros((natoms + 1, norbitals), dtype = float)
            orbital_f_spin_down = np.zeros((natoms + 1, norbitals), dtype = float)
            orbital_g_spin_down = np.zeros((natoms + 1, norbitals), dtype = float)
            orbital_sum_spin_down = np.zeros((natoms + 1, norbitals), dtype = float) 
            current_atom = 0
            line_active = False
            for line in spdfg_spin_down_file:
                if line_active:
                    temp_string_list = line.split()
                    length_spdfg = len(temp_string_list)
                    if length_spdfg == 0:
                        line_active = False
                    else:
                        orb = int(temp_string_list[0])
                        orbital_s_spin_down[current_atom-1][orb-1] = float(temp_string_list[2])
                        orbital_p_spin_down[current_atom-1][orb-1] = float(temp_string_list[3])
                        orbital_d_spin_down[current_atom-1][orb-1] = float(temp_string_list[4])
                        orbital_f_spin_down[current_atom-1][orb-1] = float(temp_string_list[5])
                        orbital_g_spin_down[current_atom-1][orb-1] = float(temp_string_list[6])
                        orbital_sum_spin_down[current_atom-1][orb-1] = float(temp_string_list[1])
                if line.startswith(' orbital       all'):
                    line_active = True
                    current_atom += 1
            spdfg_spin_down_file.close()
            
            orbital_s = np.zeros((natoms + 1, norbitals), dtype = float)
            orbital_p = np.zeros((natoms + 1, norbitals), dtype = float)
            orbital_d = np.zeros((natoms + 1, norbitals), dtype = float)
            orbital_f = np.zeros((natoms + 1, norbitals), dtype = float)
            orbital_g = np.zeros((natoms + 1, norbitals), dtype = float)
            orbital_sum = np.zeros((natoms + 1, norbitals), dtype = float)
            orbital_s = orbital_s_spin_up + orbital_s_spin_down
            orbital_p = orbital_p_spin_up + orbital_p_spin_down
            orbital_d = orbital_d_spin_up + orbital_d_spin_down
            orbital_f = orbital_f_spin_up + orbital_f_spin_down
            orbital_g = orbital_g_spin_up + orbital_g_spin_down
            orbital_sum = orbital_sum_spin_up + orbital_sum_spin_down
        else:
            print("spin_up_orbital_spdfg_populations.txt or spin_down_orbital_spdfg_populations.txt is not in the directory you browsed, make sure you have it in the directory you are browsing")
            tkinter.messagebox.showerror(title="ERROR", message="spin_up_orbital_spdfg_populations.txt or spin_down_orbital_spdfg_populations.txt file was not found, make sure you have it in the directory you are browsing and start the program again")
            raise SystemExit()

    ###For spin non-polarized
    if spin_available == 'F':
        if is_spdfg_path:
            spdfg_file = open(spdfg_path, 'r')
            orbital_s = np.zeros((natoms + 1, norbitals), dtype = float)
            orbital_p = np.zeros((natoms + 1, norbitals), dtype = float)
            orbital_d = np.zeros((natoms + 1, norbitals), dtype = float)
            orbital_f = np.zeros((natoms + 1, norbitals), dtype = float)
            orbital_g = np.zeros((natoms + 1, norbitals), dtype = float)
            orbital_sum = np.zeros((natoms + 1, norbitals), dtype = float) 
            current_atom = 0
            line_active = False
            for line in spdfg_file:
                if line_active:
                    temp_string_list = line.split()
                    length_spdfg = len(temp_string_list)
                    if length_spdfg == 0:
                        line_active = False
                    else:
                        orb = int(temp_string_list[0])
                        orbital_s[current_atom-1][orb-1] = float(temp_string_list[2])
                        orbital_p[current_atom-1][orb-1] = float(temp_string_list[3])
                        orbital_d[current_atom-1][orb-1] = float(temp_string_list[4])
                        orbital_f[current_atom-1][orb-1] = float(temp_string_list[5])
                        orbital_g[current_atom-1][orb-1] = float(temp_string_list[6])
                        orbital_sum[current_atom-1][orb-1] = float(temp_string_list[1])
                if line.startswith(' orbital       all'):
                    line_active = True
                    current_atom += 1
            spdfg_file.close()
        else:
            print("orbital_spdfg_populations.txt is not in the directory you browsed, make sure you have it in the directory you are browsing")
            tkinter.messagebox.showerror(title="ERROR", message="orbital_spdfg_populations.txt file was not found, make sure you have it in the directory you are browsing and start the program again")
            raise SystemExit()
    ###########Block for EMPTY spdfg population
    empty_spin_up_path = os.path.join(mydir, 'spin_up_empty_DOS.txt')
    is_empty_spin_up_path = os.path.isfile(empty_spin_up_path)
    empty_spin_down_path = os.path.join(mydir, 'spin_down_empty_DOS.txt')
    is_empty_spin_down_path = os.path.isfile(empty_spin_down_path)
    empty_DOS_path = os.path.join(mydir, 'empty_DOS.txt')
    is_empty_DOS_path = os.path.isfile(empty_DOS_path)

    if spin_available == 'T':
        ##For spin-up
        if is_empty_spin_up_path and is_empty_spin_down_path:
            empty_spin_up_file = open(empty_spin_up_path, 'r')
            empty_s_spin_up = np.zeros((natoms + 1, norbitals), dtype = float)
            empty_p_spin_up = np.zeros((natoms + 1, norbitals), dtype = float)
            empty_d_spin_up = np.zeros((natoms + 1, norbitals), dtype = float)
            empty_f_spin_up = np.zeros((natoms + 1, norbitals), dtype = float)
            empty_g_spin_up = np.zeros((natoms + 1, norbitals), dtype = float)
            empty_sum_spin_up = np.zeros((natoms + 1, norbitals), dtype = float)
            current_atom = 0
            line_active = False
            for line in empty_spin_up_file:
                if line_active:
                    temp_string_list = line.split()
                    length_spdfg = len(temp_string_list)
                    if length_spdfg == 0:
                        line_active = False
                    else:
                        orb = int(temp_string_list[0])
                        empty_s_spin_up[current_atom-1][orb-1] = float(temp_string_list[2])
                        empty_p_spin_up[current_atom-1][orb-1] = float(temp_string_list[3])
                        empty_d_spin_up[current_atom-1][orb-1] = float(temp_string_list[4])
                        empty_f_spin_up[current_atom-1][orb-1] = float(temp_string_list[5])
                        empty_g_spin_up[current_atom-1][orb-1] = float(temp_string_list[6])
                        empty_sum_spin_up[current_atom-1][orb-1] = float(temp_string_list[1])
                if line.startswith(' orbital       all'):
                    line_active = True
                    current_atom += 1
            empty_spin_up_file.close()
            
            ##For spin-down
            empty_spin_down_file = open(empty_spin_down_path, 'r')
            empty_s_spin_down = np.zeros((natoms + 1, norbitals), dtype = float)
            empty_p_spin_down = np.zeros((natoms + 1, norbitals), dtype = float)
            empty_d_spin_down = np.zeros((natoms + 1, norbitals), dtype = float)
            empty_f_spin_down = np.zeros((natoms + 1, norbitals), dtype = float)
            empty_g_spin_down = np.zeros((natoms + 1, norbitals), dtype = float)
            empty_sum_spin_down = np.zeros((natoms + 1, norbitals), dtype = float) 
            current_atom = 0
            line_active = False
            for line in empty_spin_down_file:
                if line_active:
                    temp_string_list = line.split()
                    length_spdfg = len(temp_string_list)
                    if length_spdfg == 0:
                        line_active = False
                    else:
                        orb = int(temp_string_list[0])
                        empty_s_spin_down[current_atom-1][orb-1] = float(temp_string_list[2])
                        empty_p_spin_down[current_atom-1][orb-1] = float(temp_string_list[3])
                        empty_d_spin_down[current_atom-1][orb-1] = float(temp_string_list[4])
                        empty_f_spin_down[current_atom-1][orb-1] = float(temp_string_list[5])
                        empty_g_spin_down[current_atom-1][orb-1] = float(temp_string_list[6])
                        empty_sum_spin_down[current_atom-1][orb-1] = float(temp_string_list[1])
                if line.startswith(' orbital       all'):
                    line_active = True
                    current_atom += 1
            empty_spin_down_file.close()
            
            empty_s = np.zeros((natoms + 1, norbitals), dtype = float)
            empty_p = np.zeros((natoms + 1, norbitals), dtype = float)
            empty_d = np.zeros((natoms + 1, norbitals), dtype = float)
            empty_f = np.zeros((natoms + 1, norbitals), dtype = float)
            empty_g = np.zeros((natoms + 1, norbitals), dtype = float)
            empty_sum = np.zeros((natoms + 1, norbitals), dtype = float)
            empty_s = empty_s_spin_up + empty_s_spin_down
            empty_p = empty_p_spin_up + empty_p_spin_down
            empty_d = empty_d_spin_up + empty_d_spin_down
            empty_f = empty_f_spin_up + empty_f_spin_down
            empty_g = empty_g_spin_up + empty_g_spin_down
            empty_sum = empty_sum_spin_up + empty_sum_spin_down

        else:
            print("spin_up_empty_DOS.txt or spin_down_empty_DOS.txt is not in the directory you browsed, make sure you have it in the directory you are browsing")
            tkinter.messagebox.showerror(title="ERROR", message="spin_up_empty_DOS.txt or spin_down_empty_DOS.txt file was not found, make sure you have it in the directory you are browsing and start the program again")
            raise SystemExit()
    ###For spin non-polarized
    if spin_available == 'F':
        if is_empty_DOS_path:
            empty_DOS_file = open(empty_DOS_path, 'r')
            empty_s = np.zeros((natoms + 1, norbitals), dtype = float)
            empty_p = np.zeros((natoms + 1, norbitals), dtype = float)
            empty_d = np.zeros((natoms + 1, norbitals), dtype = float)
            empty_f = np.zeros((natoms + 1, norbitals), dtype = float)
            empty_g = np.zeros((natoms + 1, norbitals), dtype = float)
            empty_sum = np.zeros((natoms + 1, norbitals), dtype = float) 
            current_atom = 0
            line_active = False
            for line in empty_DOS_file:
                if line_active:
                    temp_string_list = line.split()
                    length_spdfg = len(temp_string_list)
                    if length_spdfg == 0:
                        line_active = False
                    else:
                        orb = int(temp_string_list[0])
                        empty_s[current_atom-1][orb-1] = float(temp_string_list[2])
                        empty_p[current_atom-1][orb-1] = float(temp_string_list[3])
                        empty_d[current_atom-1][orb-1] = float(temp_string_list[4])
                        empty_f[current_atom-1][orb-1] = float(temp_string_list[5])
                        empty_g[current_atom-1][orb-1] = float(temp_string_list[6])
                        empty_sum[current_atom-1][orb-1] = float(temp_string_list[1])
                if line.startswith(' orbital       all'):
                    line_active = True
                    current_atom += 1
            empty_DOS_file.close()
        else:
                print("empty_DOS.txt is not in the directory you browsed, make sure you have it in the directory you are browsing")
                tkinter.messagebox.showerror(title="ERROR", message="empty_DOS.txt file was not found, make sure you have it in the directory you are browsing and start the program again")
                raise SystemExit()
        ############END EMPTY
        
    ##########BOs and SBO available per atom 
    num_BOs_available = []
    BO_available_list = []
    if is_BOCA_path:
        if spin_available == 'T':
            SBO_spin_up = np.zeros((natoms, norbitals), dtype = float)
            SBO_spin_down = np.zeros((natoms, norbitals), dtype = float)
            for atom in range(1, natoms+1):
                temp_set = []
                count = 0
                for pair in range(npairs):
                    if (BOCA_pairs[pair][0] == atom) or (BOCA_pairs[pair][1] == atom):
                        temp_set.append(BOCA_pairs[pair])
                        SBO_spin_up[atom-1] += BOCs_spin_up[pair]
                        SBO_spin_down[atom-1] += BOCs_spin_down[pair]
                        count += 1
                num_BOs_available.append(count)
                BO_available_list.append(temp_set)
            print("BO available list: ", BO_available_list)             
            print("num_BOs_available per atom : ", num_BOs_available)   
            SBO = np.zeros((natoms, norbitals), dtype = float)
            SBO = SBO_spin_up + SBO_spin_down

        if  spin_available == 'F':
            SBO = np.zeros((natoms, norbitals), dtype = float)
            for atom in range(1, natoms+1):
                temp_set = []
                count = 0
                for pair in range(npairs):
                    if (BOCA_pairs[pair][0] == atom) or (BOCA_pairs[pair][1] == atom):
                        temp_set.append(BOCA_pairs[pair])
                        SBO[atom-1] += BOCs[pair]
                        count += 1
                num_BOs_available.append(count)
                BO_available_list.append(temp_set)
            print("BO available list: ", BO_available_list)           
            print("num_BOs_available per atom : ", num_BOs_available)

order_label = tkinter.Label(gui, text = "Select a folder by clicking 'Browse Folder', then click 'run'. After, fill out the parts below", fg = 'blue', font=('Calibri', 12))
order_label.grid(row = 0, column = 0,  columnspan = 3)

folderPath = tkinter.StringVar()
btnFind = tkinter.Button(gui, text="Browse Folder",  bg = 'yellow', height= 2, width=12, command=getFolderPath)
btnFind.grid(row=1,rowspan = 1, column=0)

run_button = tkinter.Button(gui ,text="run",  bg = 'yellow', height= 2, width=5, command=RunProgram)
run_button.grid(row=1, rowspan = 1, column=1)

entries_list = []
atoms_for_curves_list = []  ##entries in list form without the <Entry> format
selected_curve_type_list = []
atoms_for_curves_entered_list = []
menu_selection = []
color_selection = []
curve_legend = []
axis_to_use = []
plot_options = []
y1_axis_options = []
y2_axis_options = []
x_axis_option = []
class first_gui(tkinter.Frame):
    def __init__(self, master):
        print("Entering _init_ in class first_gui")
        print("=====================================================================")
        global selected_units
        global peak_broadening_param_entry_var
        global lower_energy_data_entry_var
        global upper_energy_data_entry_var
        global num_data_points_per_curve_entry_var
        global num_data_curves_entry_var
        global folderPath 
        tkinter.Frame.__init__(self, master)
        self.master = master
        self.ncurves_frame = None
##        self.submit_curves_frame = None
        ##Text labels
        separator = tkinter.Label(self.master, text = "---------------------------------------------------------------------")
        separator.grid(row = 2, column = 0,  columnspan = 3)
        energy_units_label= tkinter.Label(self.master, text="Select Units")
        energy_units_label.grid(row = 3, column  = 0)
        select_param_label  = tkinter.Label(self.master, text = "Select peak broadening parameter value")
        select_param_label.grid(row = 4, column  = 0)
        select_param_label_def = tkinter.Label(self.master,
        text = "The default value of the peak broadening parameter sigma is  0.1 eV = 0.1/27.2114 = 0.0036749 hartrees (au)")
        select_param_label_def.grid(row = 6, column = 0,  columnspan = 3)
        separator = tkinter.Label(self.ncurves_frame, text = "---------------------------------------------------------------------")
        separator.grid(row = 7, column = 0,  columnspan = 3)
        energy_range_label = tkinter.Label(self.master, text = "What is the energy range to prepare for each data curve? (enter in same units as above) \n Recommended range in eV: -81 to 30; in Hartrees: -3 to 1 ")
        energy_range_label.grid(row = 8, rowspan = 2, column = 0, columnspan = 2)
        energy_range_label_lower = tkinter.Label(self.master, text = "lower value")
        energy_range_label_lower.grid(row = 11, column = 0)
        energy_range_label_upper = tkinter.Label(self.master, text = "upper value")
        energy_range_label_upper.grid(row = 11, column = 1)
        separator = tkinter.Label(self.ncurves_frame, text = "---------------------------------------------------------------------")
        separator.grid(row = 12, column = 0,  columnspan = 3)
        data_points_per_curve_label = tkinter.Label(self.master, text = "How many data points per curve to prepare?")
        data_points_per_curve_label.grid(row = 13, column = 0)
        separator = tkinter.Label(self.ncurves_frame, text = "---------------------------------------------------------------------")
        separator.grid(row = 14, column = 0,  columnspan = 3)
        num_data_curves_label = tkinter.Label(self.master, text = "How many data curves do you want to prepare?")
        num_data_curves_label.grid(row = 16, column = 0)
        separator = tkinter.Label(self.ncurves_frame, text = "---------------------------------------------------------------------")
        separator.grid(row = 18, column = 0,  columnspan = 3)
        list_instructions_label = tkinter.Label(self.master, text = "To enter a group of atoms use the following convention: 1-10, 14, 16-17, 19-21, 24")
        list_instructions_label.grid(row = 19, column = 0, columnspan = 3)
        
        ##Declaring Variables
        peak_broadening_param_entry_var = tkinter.DoubleVar()
        peak_broadening_param_entry_var.set(0.0036749)
        lower_energy_data_entry_var =  tkinter.DoubleVar()
        lower_energy_data_entry_var.set(-3) 
        upper_energy_data_entry_var =  tkinter.DoubleVar()
        upper_energy_data_entry_var.set(1)  
        num_data_points_per_curve_entry_var =  tkinter.IntVar()
        num_data_points_per_curve_entry_var.set(2001)
        num_data_curves_entry_var =  tkinter.IntVar()
        num_data_curves_entry_var.set(3)
        ##Radio buttons for unit selction
        selected_units = tkinter.IntVar()
        selected_units.set(2)   
        eV = ttk.Radiobutton(self.master, text="eV", value=1, variable = selected_units)
        eV.grid(row = 3, column = 1)
        au = ttk.Radiobutton(self.master, text="Hartree (au)", value=2, variable = selected_units)
        au.grid(row = 3, column = 2)
        ##Entry boxes
        peak_broadening_param_entry = tkinter.Entry(self.master, textvariable=peak_broadening_param_entry_var)
        peak_broadening_param_entry.grid(row = 4, column  = 1)
        lower_energy_data_entry = tkinter.Entry(self.master, textvariable=lower_energy_data_entry_var)
        lower_energy_data_entry.grid(row = 11, column  = 0)
        upper_energy_data_entry = tkinter.Entry(self.master, textvariable=upper_energy_data_entry_var)
        upper_energy_data_entry.grid(row = 11, column  = 1)
        num_data_points_per_curve_entry = tkinter.Entry(self.master, textvariable=num_data_points_per_curve_entry_var)
        num_data_points_per_curve_entry.grid(row = 13, column  = 1)
        num_data_curves_entry = tkinter.Entry(self.master, textvariable=num_data_curves_entry_var)
        num_data_curves_entry.grid(row = 16, column  = 1)
          ##Submit button
        submit_button = tkinter.Button(gui, text = 'Submit', command = self.create_num_curves_menu)
        submit_button.grid(row = 17, column  = 0, columnspan = 2) 

    def create_num_curves_menu(self):
        print("Entering create_num_curves_menu in class first_gui")
        print("=====================================================================")
        global num_curves
        global energy_units_ans
        global peak_broadening_param_entry_ans
        global lower_energy_data_entry_ans
        global upper_energy_data_entry_ans
        global num_data_points_per_curve_entry_ans
        global num_curves
        global curves_entry
        entries_list.clear()
        energy_units_ans = selected_units.get()
        if energy_units_ans == 1:
            print("You chose eV units")
        if energy_units_ans == 2:
            print("You chose au units")
        peak_broadening_param_entry_ans = peak_broadening_param_entry_var.get()
        lower_energy_data_entry_ans = lower_energy_data_entry_var.get()
        upper_energy_data_entry_ans = upper_energy_data_entry_var.get()
        num_data_points_per_curve_entry_ans = num_data_points_per_curve_entry_var.get()
        num_curves = num_data_curves_entry_var.get()
        print("peak broadening parameter: {}  lower energy: {}  upper energy: {}  data points per curve: {}  data curves: {}".format(peak_broadening_param_entry_ans, lower_energy_data_entry_ans, upper_energy_data_entry_ans, num_data_points_per_curve_entry_ans, num_curves))
        if self.ncurves_frame == None:
            self.ncurves_frame = tkinter.Frame(self.master)
            self.ncurves_frame.grid(row = 20, column  = 0, columnspan = 4)
            for x in range(num_curves):
                curves_entry_var = tkinter.StringVar()
                curves_label = tkinter.Label(self.ncurves_frame, text="For curve # " + str(x+1))
                curves_label.grid(row = x, column  = 0)
                curves_entry = tkinter.Entry(self.ncurves_frame, textvariable = curves_entry_var)
                entries_list.append(curves_entry)
                curves_entry.grid(row = x, column  = 1)
            submit_button = tkinter.Button(self.ncurves_frame, text="Submit curves", command = self.open_gui_2)
            submit_button.grid(row = x, column  = 2)
            clear1_button = tkinter.Button(self.ncurves_frame, text="Clear", command= self.destroy_ncurves_frame)
            clear1_button.grid(row = 1+x, column  = 0)

    def destroy_ncurves_frame(self):
        print("Entering destroy_ncurves_frame in class first_gui")
        print("=====================================================================")
        self.ncurves_frame.destroy()
        self.ncurves_frame = None
        try:
            self.submit_curves_frame.destroy()
            self.submit_curves_frame = None
            self.curves_options_frame.destroy()
            self.curves_options_frame = None
            self.graph_options_frame.destroy()
            self.graph_options_frame = None
            self.axis_options_frame.destroy()
            self.axis_options_frame = None
        except:
            print("")
        

    def parse_range(self, entries):
        print("Entering parse_range in class first_gui")
        print("=====================================================================")
        result=set()
        for part in entries.split(','):
            x=part.split('-')
            result.update(range(int(x[0]),int(x[-1])+1))
        return sorted(result)

    def open_gui_2(self):
        print("Entering open_gui_2 function in class first_gui")
        print("=====================================================================")
        global gui_2
        global flat_item_index_list
        global item_index_list
        global natoms_in_curves_list
        global atoms_for_curves_entered
        global natoms
        self.submit_curves_frame = None
        gui_2 = tkinter.Toplevel(self.master)
        gui_2.title("Select options for curves")
        gui_2.geometry("1400x500")
        self.curves_options_frame = None
        atoms_for_curves_list.clear()
        selected_curve_type_list.clear()
        atoms_for_curves_entered_list.clear()
        natoms_in_curves_list = []
        for entries in entries_list:
            atoms_for_curves_entered = entries.get()
            atoms_for_curves = self.parse_range(entries.get())
            for num in atoms_for_curves:
                if num > natoms:
                    tkinter.messagebox.showerror(title="ERROR", message="ERROR: Atom entered was larger than the number of atoms in the system. You must clear this selections and submit the number of curves again!")
                else:
                    pass
            len_atoms_for_curves = len(atoms_for_curves)
            natoms_in_curves_list.append(len_atoms_for_curves)
            atoms_for_curves_list.append(atoms_for_curves)
            atoms_for_curves_entered_list.append(atoms_for_curves_entered)
        print("atoms_for_curves_list", atoms_for_curves_list)
        print("natoms_in_curves_list", natoms_in_curves_list)
        print("atoms_for_curves_entered_list", atoms_for_curves_entered_list)
        max_empty_s = np.amax(empty_s)
        max_empty_p = np.amax(empty_p)
        max_empty_d = np.amax(empty_d)
        max_empty_f = np.amax(empty_f)
        max_empty_g = np.amax(empty_g)
        max_empty_sum = np.amax(empty_sum)
        max_empty = max(max_empty_s, max_empty_p, max_empty_d, max_empty_f, max_empty_g, max_empty_sum)
        if self.submit_curves_frame == None:
            self.submit_curves_frame = gui_2
            ### gui_2.1 
            for curve in range(num_curves):
                curves2_label = tkinter.Label(self.submit_curves_frame, text="Select an option for curve # " + str(curve+1))
                curves2_label.grid(row = curve, column  = 0)
            counter = 0
            if spin_available == 'T':
                for item in natoms_in_curves_list:
                    selected_curve_type_var = tkinter.IntVar()
                    selected_curve_type_list.append(selected_curve_type_var)
                    if item == 1:
                        spdfg_spin_up_button = ttk.Radiobutton(self.submit_curves_frame, text = "spdfg spin up", value=1, variable = selected_curve_type_var)
                        spdfg_spin_up_button.grid(row = counter, column = 1)
                        spdfg_spin_down_button = ttk.Radiobutton(self.submit_curves_frame, text = "spdfg spin down", value=2, variable = selected_curve_type_var)
                        spdfg_spin_down_button.grid(row = counter, column = 2)
                        spdfg_button = ttk.Radiobutton(self.submit_curves_frame, text = "spdfg", value=3, variable = selected_curve_type_var)
                        spdfg_button.grid(row = counter, column = 3)
                        if is_BOCA_path:
                            SBO_button = ttk.Radiobutton(self.submit_curves_frame, text = "SBO", value=4, variable = selected_curve_type_var)
                            SBO_button.grid(row = counter, column = 4)
                            BO_spin_up_button = ttk.Radiobutton(self.submit_curves_frame, text = "BO spin up", value=5, variable = selected_curve_type_var)
                            BO_spin_up_button.grid(row = counter, column = 5)
                            BO_spin_down_button = ttk.Radiobutton(self.submit_curves_frame, text = "BO spin down", value=6, variable = selected_curve_type_var)
                            BO_spin_down_button.grid(row = counter, column = 6)
                            BO_button = ttk.Radiobutton(self.submit_curves_frame, text = "BO", value=7, variable = selected_curve_type_var)
                            BO_button.grid(row = counter, column = 7)
                        if max_empty != 0:
                            empty_states_spin_up_button = ttk.Radiobutton(self.submit_curves_frame, text = "empty states spin up", value=8, variable = selected_curve_type_var)
                            empty_states_spin_up_button.grid(row = counter, column = 8)
                            empty_states_spin_down_button = ttk.Radiobutton(self.submit_curves_frame, text = "empty states spin down", value=9, variable = selected_curve_type_var)
                            empty_states_spin_down_button.grid(row = counter, column = 9)
                            empty_states_button = ttk.Radiobutton(self.submit_curves_frame, text = "empty states", value=10, variable = selected_curve_type_var)
                            empty_states_button.grid(row = counter, column = 10)
                        counter += 1
                    else:
                        spdfg_spin_up_button = ttk.Radiobutton(self.submit_curves_frame, text = "spdfg spin up", value=1, variable = selected_curve_type_var)
                        spdfg_spin_up_button.grid(row = counter, column = 1)
                        spdfg_spin_down_button = ttk.Radiobutton(self.submit_curves_frame, text = "spdfg spin down", value=2, variable = selected_curve_type_var)
                        spdfg_spin_down_button.grid(row = counter, column = 2)
                        spdfg_button = ttk.Radiobutton(self.submit_curves_frame, text = "spdfg", value=3, variable = selected_curve_type_var)
                        spdfg_button.grid(row = counter, column = 3)
                        if is_BOCA_path:
                            SBO_button = ttk.Radiobutton(self.submit_curves_frame, text = "SBO", value=4, variable = selected_curve_type_var)
                            SBO_button.grid(row = counter, column = 4)
                        if max_empty != 0:                        
                            empty_states_spin_up_button = ttk.Radiobutton(self.submit_curves_frame, text = "empty states spin up", value=8, variable = selected_curve_type_var)
                            empty_states_spin_up_button.grid(row = counter, column = 5)
                            empty_states_spin_down_button = ttk.Radiobutton(self.submit_curves_frame, text = "empty states spin down", value=9, variable = selected_curve_type_var)
                            empty_states_spin_down_button.grid(row = counter, column = 6)
                            empty_states_button = ttk.Radiobutton(self.submit_curves_frame, text = "empty states", value=10, variable = selected_curve_type_var)
                            empty_states_button.grid(row = counter, column = 7)
                        counter += 1
            if spin_available == 'F':
                for item in natoms_in_curves_list:
                    selected_curve_type_var = tkinter.IntVar()
                    selected_curve_type_list.append(selected_curve_type_var)
                    if item == 1:
                        spdfg_button = ttk.Radiobutton(self.submit_curves_frame, text = 'spdfg', value=3, variable = selected_curve_type_var)
                        spdfg_button.grid(row = counter, column = 1)
                        if is_BOCA_path:
                            SBO_button = ttk.Radiobutton(self.submit_curves_frame, text = 'SBO', value=4, variable = selected_curve_type_var)
                            SBO_button.grid(row = counter, column = 2)
                            BO_button = ttk.Radiobutton(self.submit_curves_frame, text = 'BO', value=7, variable = selected_curve_type_var)
                            BO_button.grid(row = counter, column = 3)
                        if max_empty != 0:
                            empty_states_button = ttk.Radiobutton(self.submit_curves_frame, text = "empty states", value=10, variable = selected_curve_type_var)
                            empty_states_button.grid(row = counter, column = 4)
                        counter += 1
                    else:
                        spdfg_button = ttk.Radiobutton(self.submit_curves_frame, text = 'spdfg', value=3, variable = selected_curve_type_var)
                        spdfg_button.grid(row = counter, column = 1)
                        if is_BOCA_path:
                            SBO_button = ttk.Radiobutton(self.submit_curves_frame, text = 'SBO', value=4, variable = selected_curve_type_var)
                            SBO_button.grid(row = counter, column = 2)
                        if max_empty != 0:
                            empty_states_button = ttk.Radiobutton(self.submit_curves_frame, text = "empty states", value=10, variable = selected_curve_type_var)
                            empty_states_button.grid(row = counter, column = 3)                        
                        counter += 1
            item_index_list = []
            for item in atoms_for_curves_list:
                if len(item) == 1:
                    item_index_list.append(item)
                else:
                    item_index_list.append([0])
            flat_item_index_list = [item for elem in item_index_list for item in elem]  ##list comprehension to make a flat list [[9], [0], [7]] --> [9, 0, 7]
            print("get item index for BO: ",flat_item_index_list)
            submit2_button = tkinter.Button(self.submit_curves_frame, text = 'Submit', command = self.submit_gui2)
            submit2_button.grid(row = 1 + len(natoms_in_curves_list), column  = 1)
            clear2_button = tkinter.Button(self.submit_curves_frame, text = 'Clear', command = self.destroy_submit_curves_frame)
            clear2_button.grid(row = 1 + len(natoms_in_curves_list), column  = 0)
            
    def destroy_submit_curves_frame(self):
        print("Entering destroy_submit_curves_frame function in class first_gui")
        print("=====================================================================")
        self.submit_curves_frame.destroy()
        self.submit_curves_frame = None
        
    def wait(self, event):
        print("Entering wait function")
        print("=====================================================================")
        self.wait_frame = None
        if self.wait_frame == None:
            self.wait_frame = tkinter.Frame(gui_2)
            self.wait_frame.grid(row = 2 + len(curve_type_selection_array), column  = 0, columnspan = 7)
            wait_label = tkinter.Label(self.wait_frame, text = "Wait... You may see (Not Responding) please wait.", fg = 'blue', font=('Calibri', 12))
            wait_label.grid(row = 2 + len(curve_type_selection_array), column = 0)
        
    def submit_gui2(self):
        print("Entering submit_gui2 function in class first_gui")
        print("=====================================================================")
        global curve_type_selection_array
        menu_selection.clear()
        spdfg_options = [
                    "s", 
                    "p",
                    "d",
                    "f",
                    "g",
                    "all"
                    ]
        SBO_polarized_options = [
                "SBO spin up",
                "SBO spin down",
                "SBO"
                ]
        SBO_nonpolarized_options = [
                "SBO"
                ]
        curve_type_selection_array = [var.get() for var in selected_curve_type_list]
        ## 1 for spin up spdfg, 2 for spin down spdfg, 3 for spdfg, 4 for SBO
        ## 5 for spin up BO, 6 for spin down BO, 7 for BO, 8 for empty states spin up,
        ## 9 for empty states spin down, and 10 for empty states.
        print("curve_type_selection_array (RadioButtons selections)=", curve_type_selection_array)
        BO_options = []
        if is_BOCA_path:
            for item in flat_item_index_list:
                if item != 0:
                    BO_options.append(BO_available_list[item-1])
                elif item == 0:
                    BO_options.append([])
            print("BO_options (list with the available BOs for that atom)=", BO_options)
        ##Spin polarized
        if self.curves_options_frame == None:
            self.curves_options_frame = tkinter.Frame(gui_2)
            self.curves_options_frame.grid(row =0, rowspan = int(len(curve_type_selection_array)), column  = 12)
            ### gui_2.2
            if spin_available == 'T':
                for curve, item in enumerate(curve_type_selection_array):
                    menu_selection_var = tkinter.StringVar()
                    menu_selection.append(menu_selection_var)
                    if item == 1:
                        spdfg_spin_up_menu = tkinter.OptionMenu(self.curves_options_frame, menu_selection_var, *spdfg_options)
                        spdfg_spin_up_menu.grid(row = curve, column  = 11)
                    elif item == 2:
                        spdfg_spin_down_menu = tkinter.OptionMenu(self.curves_options_frame, menu_selection_var, *spdfg_options)
                        spdfg_spin_down_menu.grid(row = curve, column  = 11)
                    elif item == 3:
                        spdfg_menu = tkinter.OptionMenu(self.curves_options_frame, menu_selection_var, *spdfg_options)
                        spdfg_menu.grid(row = curve, column  = 11)
                    elif item == 4: 
                        SBO_menu = tkinter.OptionMenu(self.curves_options_frame, menu_selection_var, *SBO_polarized_options)
                        SBO_menu.grid(row = curve, column  = 11)
                    elif item == 5:
                        BO_spin_up_menu = tkinter.OptionMenu(self.curves_options_frame, menu_selection_var, *BO_options[curve])
                        BO_spin_up_menu.grid(row = curve, column  = 11)
                    elif item == 6:
                        BO_spin_down_menu = tkinter.OptionMenu(self.curves_options_frame, menu_selection_var, *BO_options[curve])
                        BO_spin_down_menu.grid(row = curve, column  = 11)
                    elif item == 7:
                        BO_menu = tkinter.OptionMenu(self.curves_options_frame, menu_selection_var, *BO_options[curve])
                        BO_menu.grid(row = curve, column  = 11)
                    elif item == 8:
                        empty_states_spin_up_menu = tkinter.OptionMenu(self.curves_options_frame, menu_selection_var, *spdfg_options)
                        empty_states_spin_up_menu.grid(row = curve, column  = 11)
                    elif item == 9:
                        empty_states_spin_down_menu = tkinter.OptionMenu(self.curves_options_frame, menu_selection_var, *spdfg_options)
                        empty_states_spin_down_menu.grid(row = curve, column  = 11)
                    elif item == 10:
                        empty_states_menu = tkinter.OptionMenu(self.curves_options_frame, menu_selection_var, *spdfg_options)
                        empty_states_menu.grid(row = curve, column  = 11)
                submit_last_selections_button = tkinter.Button(self.curves_options_frame, text = 'Submit', command = self.submit_last_selections)
                submit_last_selections_button.grid(row = 1 + len(curve_type_selection_array), column  = 12)
                submit_last_selections_button.bind('<Button-1>', self.wait)
                clear3_button = tkinter.Button(self.curves_options_frame, text = 'Clear', command = self.destroy_curves_options_frame)
                clear3_button.grid(row = 1 + len(curve_type_selection_array), column  = 11)
            ##Spin non-polarized
            if spin_available == 'F':
                for curve, item in enumerate(curve_type_selection_array):
                    menu_selection_var = tkinter.StringVar()
                    menu_selection.append(menu_selection_var)
                    if item == 3:
                        spdfg_menu = tkinter.OptionMenu(self.curves_options_frame, menu_selection_var, *spdfg_options)
                        spdfg_menu.grid(row = curve, column  = 5)
                    elif item == 4: 
                        SBO_menu = tkinter.OptionMenu(self.curves_options_frame, menu_selection_var, *SBO_nonpolarized_options)
                        SBO_menu.grid(row = curve, column  = 5)
                    elif item == 7:
                        BO_menu = tkinter.OptionMenu(self.curves_options_frame, menu_selection_var, *BO_options[curve])
                        BO_menu.grid(row = curve, column  = 5)
                    elif item == 10:
                        empty_states_menu = tkinter.OptionMenu(self.curves_options_frame, menu_selection_var, *spdfg_options)
                        empty_states_menu.grid(row = curve, column  = 5)
                submit_last_selections_button = tkinter.Button(self.curves_options_frame, text = 'Submit', command = self.submit_last_selections)
                submit_last_selections_button.grid(row = 1 + len(curve_type_selection_array), column  = 6)
                submit_last_selections_button.bind('<Button-1>', self.wait)
                clear3_button = tkinter.Button(self.curves_options_frame, text = 'Clear', command = self.destroy_curves_options_frame)
                clear3_button.grid(row = 1 + len(curve_type_selection_array), column  = 5)
                


    def submit_last_selections(self):
        print("Entering submit_last_selections function")
        print("=====================================================================")
        global orbital_energies
        global populations_to_plot
        global menu_selection_list
        global title_entry_var
        global x_axis_entry_var
        global y_axis_entry_var
        global title_font_size_var
        global axis_labels_font_size_var
        global plot_options
        global x_values
        global y_data
        self.graph_options_frame = None
        color_selection.clear()
        curve_legend.clear()
        axis_to_use.clear()
        plot_options.clear()
        color_options = [
                    "red", 
                    "green",
                    "blue",
                    "black",
                    "brown",
                    "orange",
                    "teal",
                    "cyan",
                    "violet"
                    ]
        menu_selection_list = [var.get() for var in menu_selection]
        print("menu_selection_list (drop down menus selections)=", menu_selection_list)
        eV_per_Hartree = 27.2114
        if energy_units_ans == 1:
            orbital_energies *= eV_per_Hartree
        x_values = np.zeros((num_data_points_per_curve_entry_ans, 1), dtype = float)
        energy_increment = (upper_energy_data_entry_ans - lower_energy_data_entry_ans)/(num_data_points_per_curve_entry_ans - 1)
        for i in range(num_data_points_per_curve_entry_ans):
            x_values[i] = lower_energy_data_entry_ans + i*energy_increment

        ## 1 for spin up spdfg, 2 for spin down spdfg, 3 for spdfg, 4 for SBO
        ## 5 for spin up BO, 6 for spin down BO, 7 for BO
        populations_to_plot = np.zeros((num_curves, norbitals), dtype = float)
        temp_pop_array = np.zeros(norbitals, dtype = float)
        
        for curve in range(num_curves):
            for i in atoms_for_curves_list[curve]:
    ##      atoms_for_curves_list = [[1], [1,2,3,4], [5,6], [6]]            
    ##                i = 1; 1, 2, 3, 4;  5, 6; 6
                if curve_type_selection_array[curve] == 1:
                    if menu_selection_list[curve] == 's':
                        temp_pop_array = orbital_s_spin_up[i-1]
                    if menu_selection_list[curve] == 'p':
                        temp_pop_array = orbital_p_spin_up[i-1]
                    if menu_selection_list[curve] == 'd':
                       temp_pop_array = orbital_d_spin_up[i-1]
                    if menu_selection_list[curve] == 'f':
                        temp_pop_array = orbital_f_spin_up[i-1]
                    if menu_selection_list[curve] == 'g':
                        temp_pop_array = orbital_g_spin_up[i-1]
                    if menu_selection_list[curve] == 'all':
                        temp_pop_array = orbital_sum_spin_up[i-1]
                elif curve_type_selection_array[curve] == 2:
                    if menu_selection_list[curve] == 's':
                        temp_pop_array = orbital_s_spin_down[i-1]
                    if menu_selection_list[curve] == 'p':
                        temp_pop_array = orbital_p_spin_down[i-1]
                    if menu_selection_list[curve] == 'd':
                        temp_pop_array = orbital_d_spin_down[i-1]
                    if menu_selection_list[curve] == 'f':
                        temp_pop_array = orbital_f_spin_down[i-1]
                    if menu_selection_list[curve] == 'g':
                        temp_pop_array = orbital_g_spin_down[i-1]
                    if menu_selection_list[curve] == 'all':
                        temp_pop_array = orbital_sum_spin_down[i-1]
                elif curve_type_selection_array[curve] == 3:
                    if menu_selection_list[curve] == 's':
                        temp_pop_array = orbital_s[i-1]
                    if menu_selection_list[curve] == 'p':
                        temp_pop_array = orbital_p[i-1]
                    if menu_selection_list[curve] == 'd':
                        temp_pop_array = orbital_d[i-1]
                    if menu_selection_list[curve] == 'f':
                        temp_pop_array = orbital_f[i-1]
                    if menu_selection_list[curve] == 'g':
                        temp_pop_array = orbital_g[i-1]
                    if menu_selection_list[curve] == 'all':
                        temp_pop_array = orbital_sum[i-1]
                elif curve_type_selection_array[curve] == 4:
                    if menu_selection_list[curve] == "SBO spin up":
                        temp_pop_array = SBO_spin_up[i-1]
                    if menu_selection_list[curve] == "SBO spin down":
                        temp_pop_array = SBO_spin_down[i-1]
                    if menu_selection_list[curve] == "SBO":
                        temp_pop_array = SBO[i-1]
                elif curve_type_selection_array[curve] == 5:
                    if menu_selection_list[curve].startswith('('):
                        pair_tupleformat = eval(menu_selection_list[curve])
                        pair_listformat = [item for item in pair_tupleformat]
                        pair_index = BOCA_pairs.index(pair_listformat)
                        temp_pop_array = BOCs_spin_up[pair_index]
                elif curve_type_selection_array[curve] == 6:
                    if menu_selection_list[curve].startswith('('):
                        pair_tupleformat = eval(menu_selection_list[curve])
                        pair_listformat = [item for item in pair_tupleformat]
                        pair_index = BOCA_pairs.index(pair_listformat)
                        temp_pop_array = BOCs_spin_down[pair_index]
                elif curve_type_selection_array[curve] == 7:
                    if menu_selection_list[curve].startswith('('):
                        pair_tupleformat = eval(menu_selection_list[curve])
                        pair_listformat = [item for item in pair_tupleformat]
                        pair_index = BOCA_pairs.index(pair_listformat)
                        temp_pop_array = BOCs[pair_index]
                elif curve_type_selection_array[curve] == 8:
                    if menu_selection_list[curve] == 's':
                        temp_pop_array = empty_s_spin_up[i-1]
                    if menu_selection_list[curve] == 'p':
                        temp_pop_array = empty_p_spin_up[i-1]
                    if menu_selection_list[curve] == 'd':
                       temp_pop_array = empty_d_spin_up[i-1]
                    if menu_selection_list[curve] == 'f':
                        temp_pop_array = empty_f_spin_up[i-1]
                    if menu_selection_list[curve] == 'g':
                        temp_pop_array = empty_g_spin_up[i-1]
                    if menu_selection_list[curve] == 'all':
                        temp_pop_array = empty_sum_spin_up[i-1]
                elif curve_type_selection_array[curve] == 9:
                    if menu_selection_list[curve] == 's':
                        temp_pop_array = empty_s_spin_down[i-1]
                    if menu_selection_list[curve] == 'p':
                        temp_pop_array = empty_p_spin_down[i-1]
                    if menu_selection_list[curve] == 'd':
                        temp_pop_array = empty_d_spin_down[i-1]
                    if menu_selection_list[curve] == 'f':
                        temp_pop_array = empty_f_spin_down[i-1]
                    if menu_selection_list[curve] == 'g':
                        temp_pop_array = empty_g_spin_down[i-1]
                    if menu_selection_list[curve] == 'all':
                        temp_pop_array = empty_sum_spin_down[i-1]
                elif curve_type_selection_array[curve] == 10:
                    if menu_selection_list[curve] == 's':
                        temp_pop_array = empty_s[i-1]
                    if menu_selection_list[curve] == 'p':
                        temp_pop_array = empty_p[i-1]
                    if menu_selection_list[curve] == 'd':
                        temp_pop_array = empty_d[i-1]
                    if menu_selection_list[curve] == 'f':
                        temp_pop_array = empty_f[i-1]
                    if menu_selection_list[curve] == 'g':
                        temp_pop_array = empty_g[i-1]
                    if menu_selection_list[curve] == 'all':
                        temp_pop_array = empty_sum[i-1]
                populations_to_plot[curve] += temp_pop_array
                
        y_data = np.zeros((num_data_points_per_curve_entry_ans, num_curves), dtype = float)
        sigma = peak_broadening_param_entry_ans
        c = 1/(sigma*math.sqrt(2*math.pi))
        for orb, orbital_energy in enumerate(orbital_energies):
            for x, x_point in enumerate(x_values):
                exp_arg = (x_point - orbital_energy)**2/(2*sigma**2)
                if exp_arg > 5.0:
                    gaussian_value = 0.0
                else:
                    gaussian_value = c * np.exp(-exp_arg).item()
                for curve in range(num_curves):
                    y_data[x][curve] += gaussian_value*populations_to_plot[curve][orb]
        output = np.column_stack([x_values, y_data])
    ## 1 for spin up spdfg, 2 for spin down spdfg, 3 for spdfg, 4 for SBO
    ## 5 for spin up BO, 6 for spin down BO, 7 for BO
        menu_selection_list_modified = []
        for item in menu_selection_list:
            if ", " in item:
                item = item.replace(", ", "-")
            elif ", " not in item:
                item == item
            menu_selection_list_modified.append(item)
        atoms_for_curves_list_modified = []
        for item in atoms_for_curves_entered_list:
            if len(item) == 1:
                item  = "for atom " + item
            else:
                item = "for atoms " + item
            if "," in item:
                item = item.replace(",", ";")
            elif "," not in item:
                item == item
            atoms_for_curves_list_modified.append(item)
        header_list = []
        for selection in curve_type_selection_array:
            if selection == 1:
                header_list.append("spin-up ")
            elif selection == 2:
                header_list.append("spin-down ")
            elif selection == 3:
                header_list.append("")
            elif selection == 4:
                header_list.append("")
            elif selection == 5:
                header_list.append("spin-up BO ")
            elif selection == 6:
                header_list.append("spin-down BO ")
            elif selection == 7:
                header_list.append("BO ")
            elif selection == 8:
                header_list.append("empty spin-up ")
            elif selection == 9:
                header_list.append("empty spin-down ")
            elif selection == 10:
                header_list.append("empty ")
        header_combined = [curve_type + menu_selection + " " + atom_list for curve_type, menu_selection, atom_list \
                               in zip(header_list, menu_selection_list_modified, atoms_for_curves_list_modified)]
        if energy_units_ans == 1:
            energy_unit = "eV"
        elif energy_units_ans == 2:
            energy_unit = "Eh"
        header_combined.insert(0, "Energy in " + energy_unit)
        header = ",".join(header_combined)
        outname = os.path.join(mydir, "PDOS_program_output.csv")
        np.savetxt(outname, output, delimiter =",", header = header,  fmt ='% s')
        if self.graph_options_frame == None:
            self.graph_options_frame = tkinter.Frame(gui_2)
            self.graph_options_frame.grid(row = 3 + len(curve_type_selection_array), column  = 0, columnspan = 7)
            ##gui_2.3  entry and labels and fontsize for title and axis titles
            title_entry_var = tkinter.StringVar()
            x_axis_entry_var = tkinter.StringVar()
            y_axis_entry_var = tkinter.StringVar()
            if energy_units_ans == 1:
                x_axis_entry_var.set("Energy (eV)")
                y_axis_entry_var.set("PDOS (e/eV)")
            elif energy_units_ans == 2:
                x_axis_entry_var.set("Energy (E$_h$)")
                y_axis_entry_var.set("PDOS (e/E$_h$)")
            title_font_size_var = tkinter.IntVar()
            title_font_size_var.set(20)
            axis_labels_font_size_var = tkinter.IntVar()
            axis_labels_font_size_var.set(20)
            plot_options.append(title_entry_var)
            plot_options.append(x_axis_entry_var)
            plot_options.append(y_axis_entry_var)
            plot_options.append(title_font_size_var)
            plot_options.append(axis_labels_font_size_var)
            title_label = tkinter.Label(self.graph_options_frame, text="Title for the plot:")
            title_label.grid(row = len(curve_type_selection_array) + 2, column = 0)
            title_entry = tkinter.Entry(self.graph_options_frame, textvariable = title_entry_var)
            title_entry.grid(row = len(curve_type_selection_array) + 2, column = 1)
            x_axis_label = tkinter.Label(self.graph_options_frame, text="x axis label:")
            x_axis_label.grid(row = len(curve_type_selection_array) + 2, column = 2)
            x_axis_entry = tkinter.Entry(self.graph_options_frame, textvariable = x_axis_entry_var)
            x_axis_entry.grid(row = len(curve_type_selection_array) + 2, column = 3)
            y_axis_label = tkinter.Label(self.graph_options_frame, text="y axis label:")
            y_axis_label.grid(row = len(curve_type_selection_array) + 2, column = 4)
            y_axis_entry = tkinter.Entry(self.graph_options_frame, textvariable = y_axis_entry_var)
            y_axis_entry.grid(row = len(curve_type_selection_array) + 2, column = 5)
            title_font_size_label = tkinter.Label(self.graph_options_frame, text="font size for title:")
            title_font_size_label.grid(row = len(curve_type_selection_array) + 3, column = 0)
            title_font_size_entry = tkinter.Entry(self.graph_options_frame, textvariable = title_font_size_var)
            title_font_size_entry.grid(row = len(curve_type_selection_array) + 3, column = 1)
            axis_labels_font_size_label = tkinter.Label(self.graph_options_frame, text="font size for axis labels:")
            axis_labels_font_size_label.grid(row = len(curve_type_selection_array) + 3, column = 2)
            axis_labels_font_size_entry = tkinter.Entry(self.graph_options_frame, textvariable = axis_labels_font_size_var)
            axis_labels_font_size_entry.grid(row = len(curve_type_selection_array) + 3, column = 3)

            ##Labels and entries for the plot options
            for curve in range(num_curves):
                axis_to_use_var = tkinter.IntVar()
                curve_legend_var = tkinter.StringVar()
                color_selection_var = tkinter.StringVar()
                axis_to_use.append(axis_to_use_var)
                curve_legend.append(curve_legend_var)
                color_selection.append(color_selection_var)
                curves3_label = tkinter.Label(self.graph_options_frame, text="Select an option for curve # " + str(curve+1))
                curves3_label.grid(row = curve + len(curve_type_selection_array) + 4, column = 0)
                axis_to_use_label = tkinter.Label(self.graph_options_frame, text="Which axis to use for this curve?")
                curves3_label.grid(row = curve + len(curve_type_selection_array) + 4, column = 1)
                primary_button = ttk.Radiobutton(self.graph_options_frame, text = "Primary", value=1, variable = axis_to_use_var)
                primary_button.grid(row = curve + len(curve_type_selection_array) + 4, column = 2)
                secondary_button = ttk.Radiobutton(self.graph_options_frame, text = "Secondary", value=2, variable = axis_to_use_var)
                secondary_button.grid(row = curve + len(curve_type_selection_array) + 4, column = 3)
                off_button = ttk.Radiobutton(self.graph_options_frame, text = "Off", value=3, variable = axis_to_use_var)
                off_button.grid(row = curve + len(curve_type_selection_array) + 4, column = 4)
                curve_legend_label = tkinter.Label(self.graph_options_frame, text="Label for the curve:")
                curve_legend_label.grid(row = curve + len(curve_type_selection_array) + 4, column = 5)
                curve_legend_entry = tkinter.Entry(self.graph_options_frame, textvariable = curve_legend_var)
                curve_legend_entry.grid(row = curve + len(curve_type_selection_array) + 4, column = 6)
                colors_menu = tkinter.OptionMenu(self.graph_options_frame, color_selection_var, *color_options)
                colors_menu.grid(row = curve + len(curve_type_selection_array) + 4, column = 7)
            submit_plot_options_button = tkinter.Button(self.graph_options_frame, text = 'Submit', command = self.submit_plot_options)
            submit_plot_options_button.grid(row =curve + len(curve_type_selection_array) + 5, column  = 0)  
        
    def submit_plot_options(self):
        print("Entering submit_plot_options function")
        print("=====================================================================")
        global plot_options_list
        global axis_to_use_list
        global curve_legend_list
        global color_selection_list
        global linestyle
        linestyle = []
        self.axis_options_frame = None
        y1_axis_options.clear()
        y2_axis_options.clear()
        x_axis_option.clear()
        plot_options_list = [var.get() for var in plot_options]
        print("plot_options_list", plot_options_list)
        axis_to_use_list = [var.get() for var in axis_to_use]
        print("axis_to_use_list", axis_to_use_list)
        curve_legend_list = [var.get() for var in curve_legend]
        print("curve_legend_list", curve_legend_list)
        color_selection_list = [var.get() for var in color_selection]
        print("color_selection_list", color_selection_list)
        max_list = [max(y_data[:, curve]) for curve in range(num_curves)]
        print(max_list)
        max_number = max(max_list)
        for index, selection in enumerate(curve_type_selection_array):
            if selection == 8:
                linestyle.append("dotted")
            elif selection == 9:
                linestyle.append("dotted")
            elif selection == 10:
                linestyle.append("dotted")
            else:
                linestyle.append("solid")
        if self.axis_options_frame == None:
            self.axis_options_frame = tkinter.Frame(gui_2)
            self.axis_options_frame.grid(row = 4 + len(curve_type_selection_array), column  = 0, columnspan = 7) 
            ##gui_2.4 Enter increment and axis options
            secondary_axis = False
            for index, option in enumerate(axis_to_use_list):
                if option == 2:
                    secondary_axis = True
            x_increment_var = tkinter.DoubleVar()
            y1_start_var = tkinter.DoubleVar()
            y1_end_var = tkinter.DoubleVar()
            y1_end_var.set(math.ceil(max_number))
            y1_increment_var = tkinter.DoubleVar()
            x_axis_option.append(x_increment_var)
            y1_axis_options.append(y1_start_var)
            y1_axis_options.append(y1_end_var)
            y1_axis_options.append(y1_increment_var)
            x_increment_label = tkinter.Label(self.axis_options_frame, text="Enter the interval between ticks for x")
            x_increment_label.grid(row = index + len(curve_type_selection_array) + 8, column = 0)
            x_increment_entry = tkinter.Entry(self.axis_options_frame, textvariable = x_increment_var)
            x_increment_entry.grid(row = index + len(curve_type_selection_array) + 8, column = 1)
            y1_start_label = tkinter.Label(self.axis_options_frame, text="Enter the starting point for y1")
            y1_start_label.grid(row = index + len(curve_type_selection_array) + 9, column = 0)
            y1_start_entry = tkinter.Entry(self.axis_options_frame, textvariable = y1_start_var)
            y1_start_entry.grid(row = index + len(curve_type_selection_array) + 9, column = 1)
            y1_end_label = tkinter.Label(self.axis_options_frame, text="Enter the ending point for y1")
            y1_end_label.grid(row = index + len(curve_type_selection_array) + 9, column = 2)
            y1_end_entry = tkinter.Entry(self.axis_options_frame, textvariable = y1_end_var)
            y1_end_entry.grid(row = index + len(curve_type_selection_array) + 9, column = 3)
            y1_increment_label = tkinter.Label(self.axis_options_frame, text="Enter the interval between ticks for y1")
            y1_increment_label.grid(row = index + len(curve_type_selection_array) + 9, column = 4)
            y1_increment_entry = tkinter.Entry(self.axis_options_frame, textvariable = y1_increment_var)
            y1_increment_entry.grid(row = index + len(curve_type_selection_array) + 9, column = 5)
            if secondary_axis == True:
                y2_start_var = tkinter.DoubleVar()
                y2_end_var = tkinter.DoubleVar()
                y2_increment_var = tkinter.DoubleVar()
                y2_axis_options.append(y2_start_var)
                y2_axis_options.append(y2_end_var)
                y2_axis_options.append(y2_increment_var)
                y2_start_label = tkinter.Label(self.axis_options_frame, text="Enter the starting point for y2")
                y2_start_label.grid(row = index + len(curve_type_selection_array) + 10, column = 0)
                y2_start_entry = tkinter.Entry(self.axis_options_frame, textvariable = y2_start_var)
                y2_start_entry.grid(row = index + len(curve_type_selection_array) + 10, column = 1)
                y2_end_label = tkinter.Label(self.axis_options_frame, text="Enter the ending point for y2")
                y2_end_label.grid(row = index + len(curve_type_selection_array) + 10, column = 2)
                y2_end_entry = tkinter.Entry(self.axis_options_frame, textvariable = y2_end_var)
                y2_end_entry.grid(row = index + len(curve_type_selection_array) + 10, column = 3)
                y2_increment_label = tkinter.Label(self.axis_options_frame, text="Enter the interval between ticks for y2")
                y2_increment_label.grid(row = index + len(curve_type_selection_array) + 10, column = 4)
                y2_increment_entry = tkinter.Entry(self.axis_options_frame, textvariable = y2_increment_var)
                y2_increment_entry.grid(row = index + len(curve_type_selection_array) + 10, column = 5)
            for index, color in enumerate(color_selection_list):
                if color == "":
                    tkinter.messagebox.showerror(title="ERROR", message="ERROR: A color was not entered for curve# "+ str(index + 1) +". You must clear the axis options space and then submit again with colors selected!")
                    print("ERROR: A color was not entered")
                else:
                    pass
            submit_second_axis_options_button = tkinter.Button(self.axis_options_frame, text = 'Graph', command = self.submit_second_axis_options)
            submit_second_axis_options_button.grid(row = index + len(curve_type_selection_array) + 11, column = 1)
            clear4_button = tkinter.Button(self.axis_options_frame, text = 'Clear', command = self.destroy_axis_options_frame)
            clear4_button.grid(row = index + len(curve_type_selection_array) + 11, column = 0)
    def destroy_curves_options_frame(self):
        print("Entering destroy_curves_options_frame function in class first_gui")
        print("=====================================================================")
        self.curves_options_frame.destroy()
        self.curves_options_frame = None
        self.graph_options_frame.destroy()
        self.graph_options_frame = None
        try:
            self.axis_options_frame.destroy()
            self.axis_options_frame = None
        except:
            print("")

    def destroy_axis_options_frame(self):
        print("Entering destroy_axis_options_frame function in class first_gui")
        print("=====================================================================")
        self.axis_options_frame.destroy()
        self.axis_options_frame = None    
        
    def submit_second_axis_options(self):
        print("Entering submit_second_axis_options function")
        print("=====================================================================")
        secondary_axis = False
        y1_axis_options_list = [var.get() for var in y1_axis_options]
        y2_axis_options_list = [var.get() for var in y2_axis_options]
        x_axis_options_list = [var.get() for var in x_axis_option]
        print("x_axis_options_list", x_axis_options_list)
        print("y1_axis_options_list", y1_axis_options_list)
        print("y2_axis_options_list", y2_axis_options_list)
        for index, option in enumerate(axis_to_use_list):
            if option == 2:
                secondary_axis = True
        fig, ay1 = plt.subplots()
        ynumbers1 = np.arange(y1_axis_options_list[0], y1_axis_options_list[1] + y1_axis_options_list[2], y1_axis_options_list[2])
        ay1.set_ylim([y1_axis_options_list[0], y1_axis_options_list[1]])
        ay1.set_yticks(ynumbers1)
        ay1.tick_params(labelsize = plot_options_list[4], width = 1.5)
        if secondary_axis == True:
            ay2 = ay1.twinx()
            ynumbers2 = np.arange(y2_axis_options_list[0], y2_axis_options_list[1] + y2_axis_options_list[2], y2_axis_options_list[2])
            ay2.set_ylim([y2_axis_options_list[0], y2_axis_options_list[1]])
            ay2.set_yticks(ynumbers2)
            ay2.tick_params(labelsize = plot_options_list[4], width = 1.5)
        for index, option in enumerate(axis_to_use_list):
            if option == 1:
                curve = ay1.plot(x_values, y_data[:, index], label = curve_legend_list[index], color = color_selection_list[index], linestyle = linestyle[index])
            if option == 2:
                curve = ay2.plot(x_values, y_data[:, index], label = curve_legend_list[index], color = color_selection_list[index], linestyle = linestyle[index]) 
        fig.legend(fontsize = plot_options_list[4], loc = "lower center", bbox_transform=plt.gcf().transFigure, ncol = len(curve_type_selection_array), borderaxespad=0, edgecolor = "none")
        plt.subplots_adjust(left=None, bottom=0.19, right=None, top=None, wspace=None, hspace=None)
        ay1.set_xlabel(plot_options_list[1], fontsize = plot_options_list[4])
        ay1.set_ylabel(plot_options_list[2], fontsize = plot_options_list[4])
        plt.title(plot_options_list[0], fontsize = plot_options_list[3])
        plt.xticks(np.arange(lower_energy_data_entry_ans, upper_energy_data_entry_ans + x_axis_options_list[0], x_axis_options_list[0]))
        plt.show()

first = first_gui(gui)
gui.mainloop()
