#!/usr/bin/env python3
import os
import sys
import socket

locdir = input("Working Directory path: ")
mdp_file = input("Mdp file full name: ")
ini_confprefix = input("Config file prefix ex. sys: ")
ini_frame = int(input("Beginning frame number: "))
frame_skip = int(input("Frame Stride: "))
fin_frame = int(input("Final frame number (inclusive): "))
ndx_file = input("Ndx file full name: ")
top_file = input("Top file full name: ")
output_prefix = input("Job file output prefix ex. em_sys: ")
job_file_nm = input("Job file name prefix: ")
walltime = input("Walltime in 00:00:00 format: ")
xtra_file = input("Other files needed (space between names): ")
output_extns = input("Output extensions (ex. *.gro *.xvg *.xtc)")
cur_frame = ini_frame
print(locdir,mdp_file,ini_confprefix,ini_frame,frame_skip,fin_frame,ndx_file,top_file,output_prefix)
while cur_frame <= fin_frame:
    file_name = job_file_nm + str(cur_frame) + '.job'
    file = open( file_name , 'w')
    #print(job_file_nm + str(cur_frame) + ".job")

    # Header
    file.write('#PBS -A PAA0004\n')
    file.write('#PBS -N Pulling_of_avo\n')
    walltime_tot = '#PBS -l walltime=' + walltime+',nodes=1:ppn=12\n'
    file.write(walltime_tot)
    file.write('#PBS -S /bin/bash\n')
    file.write('#PBS -j oe\n')
    #print('#PBS -A PAA0004\n','#PBS -N Pulling_of_avo\n','#PBS -l walltime=',walltime,',nodes=1:ppn=12\n','#PBS -S /bin/bash\n','#PBS -j oe\n',sep="")
    file.write("\n")
    # Random stuff + cp's and cd's
    locdir_tot = 'locdir=' + locdir
    file.write('set -vx\n')
    file.write("\n")
    file.write(locdir_tot+'\n')
    file.write("\n") 
    file.write('st=\'date+%s\'\n')
    file.write("\n")
    #print('set -vx\n', 'locdir=', locdir,"\n", "st=\'date+%s\'",sep="")
    
    file.write('cd ' '$locdir\n')
    file.write("\n")
    #print('cd', '$locdir')
    
    cp_tot = "cp" + " " + mdp_file + " " + ini_confprefix + str(cur_frame) + '.gro' + " " + ndx_file + " " + top_file + " " + xtra_file + " "+"$TMPDIR"
    file.write(cp_tot+'\n')
    file.write("\n")
    #print(cp_tot) 
    
    file.write('cd $TMPDIR\n')
    file.write("\n")
    #print('cd $TMRDIR\n')

    file.write('module load gromacs/5.1\n')
    file.write("\n")
    #print('module load gromacs/5.1\n')

    # calling grompp
    grompp_tot = "gmx grompp "+ "-f " + mdp_file + " -p "+ top_file +" -c " + ini_confprefix + str(cur_frame) + ".gro " + "-o " + output_prefix + str(cur_frame) + ".tpr " + "-n "+ ndx_file
    file.write(grompp_tot + '\n')
    file.write("\n")
    #print(grompp_tot)

    # calling mdrun
    mdrun_tot = "mpiexec gmx_mpi mdrun -s " + output_prefix + str(cur_frame) + ".tpr" + " -deffnm " + output_prefix + str(cur_frame)+ ' -pf pullf-' + str(cur_frame)  + '.xvg' + ' -px pullx-' + str(cur_frame) + '.xvg'  
    file.write(mdrun_tot + '\n')
    file.write("\n")
    #print(mdrun_tot)

    # calling cp to get output files
    cp_tot = 'cp ' + output_extns + ' $locdir'    
    file.write(cp_tot + '\n')
    file.write("\n")
    #print(cp_tot)

    # exiting program
    file.write('|| exit 1\n')
    file.write("\n")
    #print('|| exit 1\n')
    
    # exiting messages
    file.write('echo -----------------------------------------------------')
    file.write('echo \" Finished simulation\" ')
    #print('echo -------------------------------------------------')
    #print('echo \" Finished simulation\" ')
    cur_frame += frame_skip
    file.close()
    
    
    
    
    # end


