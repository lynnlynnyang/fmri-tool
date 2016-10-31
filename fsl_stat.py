# coding: utf-8
import sys
import os
from glob import glob
from os.path import join
from argparse import ArgumentParser
#Path_current=sys.argv[0]
#N_iter=sys.argv[1]
#Name_Rmapfile=sys.argv[2]
# parse input arguments

parser = ArgumentParser()
parser.add_argument("-c", dest="control_dir", help="Path of control data",action='store',default='ctrl')
parser.add_argument("-e", dest="exp_dir", help="Path of experiement data",action='store',default='exp')
parser.add_argument("-n", dest="N_iter", help="Number of iteration",action='store',default=100,type=int)
args = parser.parse_args()

print(args.N_iter)
Path_current='/home/tyhuang/FACEmars'
#current_path = os.getcwd()
N_iter=args.N_iter
Name_Rmapfile='Rmap_beswarrest.nii'

# 分別讀取 Path_current下面的cont與exp資料夾內的MARS結果資料夾，直接從各資料夾中讀取名稱為 Name_Rmapfile(Rmap_beswarrest.nii)的檔案
list_control = glob(join(args.control_dir,'*.nii'))
list_control.extend(glob(join(args.control_dir,'*.nii.gz')))
list_experim = glob(join(args.exp_dir,'*.nii'))
list_experim.extend(glob(join(args.exp_dir,'*.nii.gz')))

# 列出control內所有的影像路徑
if len(list_control) > 0:
    str_control = ' '.join(list_control)
    # 把所有control受試者的Rmap合併成一個四維的Rmaps
    str_OSins='fslmerge -t '+ Path_current + '/contRmaps '+ str_control
    os.system(str_OSins)
    # 做出control的One sample t-test結果
    str_OSins='randomise -i %s/contRmaps -o %s/contTwottst -1  -n %d --T2'%(Path_current ,Path_current ,N_iter)
    os.system(str_OSins)
    print(str_OSins)

# 列出Expriment內所有的影像路徑
if len(list_experim) > 0:
    str_experim = ' '.join(list_experim)
    # 把所有Expriment受試者的Rmap合併成一個四維的Rmaps
    str_OSins='fslmerge -t '+ Path_current + '/expRmaps '+ str_experim
    os.system(str_OSins)
    # 做出Expriment的One sample t-test結果
    str_OSins='randomise -i %s/expRmaps  -o %s/contTwottst -1  -n %d --T2'%(Path_current ,Path_current ,N_iter)
    os.system(str_OSins)
    twosample = True
    print(list_experim)






if twosample:
    # 把兩個群組的Rmaps合併成一個，並且由design.mat決定群組
    str_OSins='fslmerge -t allRmaps '+ Path_current + '/contRmaps ' + Path_current + '/expRmaps '
    os.system(str_OSins)

    # 若兩組資料只是單純的兩群不同受試者比較Two-Sample Unpaired T-test，而非Two-Sample Paired T-test (Paired Two-Group Difference)
    # 可以用 design_ttest2 檔案名稱 群組A數目 群組B數目 來建立design.mat以及design.con
    # design.mat是GLM用來分辨不同群組的矩陣。design.con是不同群組之間的contrast(譬如說A >B 或A<B)
    str_OSins='design_ttest2 %s/design %d %d'%(Path_current , len(list_control ),len(list_experim ))
    os.system(str_OSins)

    # 執行兩群組之間的Two sample t-test
    str_OSins='randomise -i %s/allRmaps -o %s/resultTwottst -d design.mat -t design.con --T2 -n %d'%(Path_current,Path_current  ,N_iter)
    os.system(str_OSins)
