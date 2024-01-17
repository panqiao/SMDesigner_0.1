import os
import sys
from pathlib import Path
import re
import subprocess
import shutil

def is_r2r_installed():
    test_command = ["sudo","r2r", "--GSC-weighted-consensus", "./downloadxxx/R2R-1.0.6/demo/demo1.sto", 
                    "./downloadxxx/R2R-1.0.6/demo/intermediate/demo1.cons.sto", "3", "0.97", "0.9", "0.75", 
                    "4", "0.97", "0.9", "0.75", "0.5", "0.1"]
    try:
        # Run the test command for R2R
        subprocess.run(test_command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def install_r2r(path_install_r2r):
    try:
        # Assuming the installation script is named 'install_r2r.sh' and is in the current directory
        #print(path_install_r2r)
        subprocess.run(['sudo', path_install_r2r], check=True)
        print("R2R installation completed.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred during R2R installation: {e}")

def check_input_folder(input_folder):
    if not input_folder.exists() or not input_folder.is_dir():
        print(f"Error: The specified input folder '{input_folder}' does not exist or is not a directory.")
        return False
    #print('输入正确')
    return True
                    


def get_user_input():
    while True:
        input_folder_name = input("Enter the test input folder name 'test' or sample folder name with path: ")

        if input_folder_name == 'test':
            input_folder_test = Path(input_folder_name)
            if check_input_folder(input_folder_test):
                #print(input_folder_test)
                return input_folder_test
        elif input_folder_name.lower() == 'exit':
            print('Exit program.')
            break
        else:
            input_folder_sample = Path(input_folder_name)
            if check_input_folder(input_folder_sample):
                #print(input_folder_sample)
                #input_folder = input_folder_sample.parents[0]
                return input_folder_sample
            else:
                print("Invalid input folder. Please try again or you can type 'exit' to quit program.")



def create_output_folders(output_folders):
    print('create_output_folders start')
    #seq_struc_riboswitch_add
    for folder in output_folders:
        if not folder.exists():
            try:
                folder.mkdir(parents=True, exist_ok=True)
                print(f'Created folder: {folder}')
            except Exception as e:
                print(f'Error creating folder {folder}: {e}')

############################################################process_with_R2R


def process_files_for_r2r(input_folder, output_folder_r2r):
    print('process_files_for_r2r start')
    # ... (your existing code)
    #files_r2r = os.listdir(input_folder)
    files_r2r = [f for f in os.listdir(input_folder) if f.endswith('.sto')]
    
    if not files_r2r:
        print("No '.sto' files found in the folder. Exiting the program.")
        exit()
    else:
        print(files_r2r)

        for file in files_r2r:
            print(file)
            file_name_r2r = '.'.join(file.split('.')[0:-1])
            input_file_r2r = input_folder / file
            output_file_r2r = output_folder_r2r / f'{file_name_r2r}.cons.sto'

        # Construct the r2r command with the updated path
            command_r2r = [
                'r2r',
                '--GSC-weighted-consensus',
                str(input_file_r2r),
                str(output_file_r2r),
                '3', '0.97', '0.9', '0.75',
                '4', '0.97', '0.9', '0.75', '0.5', '0.1'
            ]

        # Execute the r2r command
            try:
                result = os.system(' '.join(command_r2r))
                if result != 0:
                    print(f"Error processing {input_file_r2r}, R2R not install")
                    break
                else:
                    print(f"Processed {input_file_r2r} successfully.")
                # ... (rest of your code)
            except Exception as e:
                print(f"Error processing {input_file_r2r}: {e}")
            # ... (error handling)
'''
def process_files_for_r2r(input_folder, output_folder_r2r):
    files_r2r = os.listdir(input_folder)
    for file in files_r2r:
        file_name_r2r = '.'.join(file.split('.')[0:-1])
        input_file_r2r = input_folder / file
        output_file_r2r = output_folder_r2r / f'{file_name_r2r}.cons.sto'
        command_r2r = f'r2r --GSC-weighted-consensus {input_file_r2r} {output_file_r2r} 3 0.97 0.9 0.75 4 0.97 0.9 0.75 0.5 0.1'
        os.system(command_r2r)
'''
############################################################process_noted_line and make structure line common
def process_files_for_seq_struc(input_folder_r2r, output_folder_seq_struc, no_struc_ribo_file):
    print('process_files_for_seq_struc start')
    files_seq_struc = [f for f in os.listdir(input_folder_r2r) if f.endswith('.cons.sto')]
    #print(files_seq_struc)
    for file_seq_struc in files_seq_struc:
        process_single_seq_struc_file(input_folder_r2r, output_folder_seq_struc, file_seq_struc, no_struc_ribo_file)
    print('process_files_for_seq_struc ended')

def process_single_seq_struc_file(input_folder_r2r, output_folder_seq_struc, file_seq_struc, no_struc_ribo_file):
    print('process_single_seq_struc_file start')
    input_file_seq_struc = input_folder_r2r / file_seq_struc
    output_file_seq_struc = output_folder_seq_struc / f'{file_seq_struc.strip()[0:-9]}.seqStruc'

    ls_uni_seq = process_seq_struc_lines(input_file_seq_struc, no_struc_ribo_file)

    with open(output_file_seq_struc, "w") as fo_seq_struc:
        for j_seq_struc in ls_uni_seq:
            line1_seq_struc = j_seq_struc + '\n'
            fo_seq_struc.write(line1_seq_struc)
    print('process_single_seq_struc_file ended')

def process_seq_struc_lines(input_file, no_struc_ribo_file):
    print('process_seq_struc_lines start')
    ls_uni_seq = []
    with open(input_file, "r",encoding='utf-8') as fi_seq_struc:
        ls_seq_struc = fi_seq_struc.readlines()

        for line_seq_struc in ls_seq_struc:
            if line_seq_struc.startswith('#'):
                a=re.findall('^#=GF ',line_seq_struc)
                e=re.findall('^#=GF NUM_COV',line_seq_struc)
                b=re.findall('^#=GS |#=GR ',line_seq_struc)
                c=re.findall('^#=GC con|#=GC col|#=GC RF',line_seq_struc)
                d=re.findall('# STOCKHOLM 1.0|//',line_seq_struc)

                if b or c or d:
                    continue
                elif a and not e:
                    continue
                else:
                    if re.findall('#=GC SS_cons',line_seq_struc):
                        if ">" not in line_seq_struc:
                            no_struc_ribo_file.write(input_file)


                    #ls_anntate=[]
                        else:
                            ls=line_seq_struc.split()
                            ls_seq='#=GC SS_cons'
                            line1=re.sub('[\{\[\(]','<',ls[-1])
                            line2=re.sub('[\}\]\)]','>',line1)
                            line3 = f'{ls_seq:<45}' + re.sub('[\_\-\:\~\,]', '.', line2)

                            ls_uni_seq.append(line3)
                    elif re.findall('#=GC cov_SS_cons',line_seq_struc):
                        ls_cov_id='#=GC cov_SS_cons'
                        ls_cov=line_seq_struc.split()[-1]
                        line_cov=f'{ls_cov_id:<45}' + ls_cov
                        ls_uni_seq.append(line_cov)
                            #fo.write(line)
            else:

                #009|FN667741.1/3471117-3471071/1-47
                #LCLP01000004.1/37559-37400/1-151            AGUUU
                if '|' not in line_seq_struc:
                    if '//' in line_seq_struc or line_seq_struc.isspace():
                        pass
                    else:
                        seq_ls1=line_seq_struc.strip().split()
                        #print(seq_ls1)
                        seq1=f'{seq_ls1[0]:<45}'+seq_ls1[-1]
                        ls_uni_seq.append(seq1)
                else:
                    ls1=line_seq_struc.strip().split('|')
                    seq=ls1[1]
                    if seq in ls_uni_seq:
                        pass
                    else:
                        seq_ls=seq.split()
                        seq=f'{seq_ls[0]:<45}'+seq_ls[-1]
                        ls_uni_seq.append(seq)
        print('process_seq_struc_lines ended')
        return ls_uni_seq
        
########################################################add_struc_info_lines from test_find_all_loop.py and is part1 of make_mu_structure2_riboswitch.py
def findloop(string,ls_loop_new,ls_loop1_new):
    print('findloop start')
    ls_loop=[]
    ls_loop1=[]
    ls_stem=[]
    ls_struc=[]
    ls_string=[]

    num9=string.index('<')
    #print('num9:',num9)
    num10=len(string)
    while num10!=1 and string[num10-1]!='>':
        num10-=1 
    num10=num10-1
    #print('num10',num10)
    ##############get first structure loop region ls_loop, get string with second struture
    while re.search('<\.+>',string):
        str5=''
        str4=''
        nu=re.search('<\.+>',string).span()
    #num9=nu[1]-nu[0]
        ls_loop.append([nu[0],nu[1]-1])
        for k in range (nu[1]-nu[0]-2):
                str4=str4+'_'
            #print(str4)
            #str5='<'+str4+'>'
            
            #str5='<'+str4+'>'
        #print(str4)
        str5='<'+str4+'>'
        string=re.sub('<\.+>', str5, string,1)
        string_strc=string
        #string_mu=

    #print('ls_loop:',ls_loop)
    #print('string:',string)
    #print(string)
    #print(ls_loop)
    ###########return stem number ls_loop1
    for i in range(len(ls_loop)):
        j=ls_loop[i][1]
        k=ls_loop[i][0]
        num7=0
        num8=0
        if i ==0:
            
            while string[j]!='<' and j<num10:
                j+=1
                if string[j]=='>':
                    num7+=1
            while k>=num9:
                k-=1
                if string[k]=='<':
                    num8+=1
            #print(num7,num8)
        elif i== len(ls_loop)-1 and i!=0:
            
            while j<num10:
                j+=1
                if string[j]=='>':
                    num7+=1
            while string[k]!='>':
                k-=1
                if string[k]=='<':
                    num8+=1
        elif 0<i<len(ls_loop)-1:
            
            while string[j]!='<':
                j+=1
                if string[j]=='>':
                    num7+=1
            while string[k]!='>':
                k-=1
                if string[k]=='<':
                    num8+=1
        num_temp=ls_loop[i][0]
        num_temp1=ls_loop[i][1] 
        #print(num_temp,num_temp1,num7,num8)
        if num7<=num8:
            num7_temp=num7
            
            while num7>0:
                num_temp-=1 
                if string[num_temp]=='<':
                    num7-=1
            while num7_temp>0:  
                num_temp1+=1
                if string[num_temp1]=='>':
                    num7_temp-=1    
            #print(num_temp,num_temp1) 
            
        else:
            num8_temp=num8
            while num8>0:
                num_temp-=1 
                if string[num_temp]=='<':
                    num8-=1
            while num8_temp>0:  
                num_temp1+=1
                if string[num_temp1]=='>':
                    num8_temp-=1    
        #print(num7,num8)
        ls_loop1.append([num_temp,num_temp1])
    
    for a in ls_loop1:
        str_re='.'*(a[1]-a[0]+1)
        #print(str_re)
        string=string[0:a[0]]+str_re+string[(a[1]+1):]
        #print(string)
    
    ls_loop_new.extend(ls_loop)
    ls_loop1_new.extend(ls_loop1)
    return(string_strc,string,ls_loop,ls_loop_new,ls_loop1,ls_loop1_new)
def mark_stem_struc(string_strc,string1,ls_loop,ls_loop1,ls_stem,ls_struc,num_cycle,num_stem,num_stem1,ls_temp):
    print('mark_stem_struc start')
    #ls_temp=[]
    if num_cycle==1:
        num9=string_strc.index('<')
    #print('num9:',num9)
        num10=len(string_strc)
        while num10!=1 and string_strc[num10-1]!='>':
            num10-=1 
        num10=num10-1
        for k in range(len(string_strc)):
            num=1
            for m in range(len(ls_loop1)):
                if ls_loop1[m][0]<=k<=ls_loop1[m][1] and string1[k] in ['>','<']:
                    
                    ls_stem.append(('s1_'+str(m)))
                    num=0
            if num==1:
                ls_stem.append(str(k))
        
        #ls_temp=[]
        #....<<<...<<<.<<__>>.<<<<<<<____>>>>>>>.>>>.<<..<<<__>>><<<__>>>..>>...>>>.
        for k in range(len(string_strc)):
            if k<num9:
                ls_struc.append('5s')
            elif k>num10:
                ls_struc.append('3s')
            elif string_strc[k]=='_':
                ls_struc.append('p')
            else:
                                
                if len(ls_loop1)==1:
                    if ls_loop1[0][0]<=k<=ls_loop[0][0]:
                        if string_strc[k]=='<':

                            num_stem+=1
                            ls_struc.append(str(num_stem)+'L')
                            ls_temp.append(str(num_stem)+'L')
                        elif string_strc[k]=='.':
                            ls_struc.append('B')
                        num_stem1=len(ls_temp)
                        #print(num_stem1)
                    elif ls_loop[0][1]<=k<=ls_loop1[0][1]:
                        if string_strc[k]=='>':                     
                            ls_struc.append(str(num_stem1)+'R')
                            num_stem1-=1
                        elif string_strc[k]=='.':
                            ls_struc.append('B')
                    

                elif len(ls_loop1)>1:
                    if num9<=k<ls_loop1[0][0] or ls_loop1[-1][1]<k<=num10:
                            ls_struc.append(str(k))

                    else:
                    
                        for m in range(len(ls_loop1)-1):
                            #if ls_loop[m][0]<k<ls_loop[m][1]:
                                #ls_struc.append('p')
                            if ls_loop1[m][0]<=k<=int(ls_loop[m][0]):
                                if string_strc[k]=='<':

                                    num_stem+=1
                                    ls_struc.append(str(num_stem)+'L')
                                    ls_temp.append(str(num_stem)+'L')

                                elif string_strc[k]=='.':
                                    ls_struc.append('B')
                                num_stem1=len(ls_temp)
                                break
                                #print(num_stem1)
                            elif ls_loop[m][1]<=k<=ls_loop1[m][1]:
                                if string_strc[k]=='>':                     
                                    ls_struc.append(str(num_stem1)+'R')
                                    num_stem1-=1
                                elif string_strc[k]=='.':
                                    ls_struc.append('B')
                                break
                            elif ls_loop1[m][1]<k<ls_loop1[m+1][0]:
                                ls_struc.append(str(k))
                                break
                        if ls_loop1[-1][0]<=k<=int(ls_loop[-1][0]):
                                if string_strc[k]=='<':

                                    num_stem+=1
                                    ls_struc.append(str(num_stem)+'L')
                                    ls_temp.append(str(num_stem)+'L')

                                elif string_strc[k]=='.':
                                    ls_struc.append('B')
                                num_stem1=len(ls_temp)
                                #print(num_stem1)
                        elif ls_loop[-1][1]<=k<=ls_loop1[-1][1]:
                            if string_strc[k]=='>':                     
                                ls_struc.append(str(num_stem1)+'R')
                                num_stem1-=1
                            elif string_strc[k]=='.':
                                ls_struc.append('B')
                            
                            
                    #....<<<...<<<.<<__>>.<<<<<<<____>>>>>>>.>>>.<<..<<<__>>><<<__>>>..>>...>>>.        
                            

                        

        #print(ls_struc)
                        
    elif num_cycle>1:
        for k in range(len(string_strc)):
            #num=1
            for m in range(len(ls_loop1)):
                if ls_loop1[m][0]<=k<=ls_loop1[m][1] and string1[k] in ['>','<']:
                    if 's' in ls_stem[k]:
                        pass
                    else:
                        stem_id='s'+str(num_cycle)+'_'+str(m)
                        ls_stem[k]=stem_id
                        
    #       string='....<<<...<<<.<<__>>.<<<<<<<____>>>>>>>.>>>.<<..<<<..>>><<<..>>>..>>...>>>.'
    #             5s  45678910001l2lppp
   #             ....<<<...<<<...........................>>>.<<....................>>...>>>.
   #             ....<<<................................................................>>>.
            
            #....<<<...<<<___________________________>>>.<<____________________>>...>>>.
            if len(ls_loop1)==1:

                if ls_loop1[0][0]<=k<=ls_loop[0][0]:
                    if string_strc[k]=='<' and (ls_struc[k]).isnumeric():

                        num_stem+=1
                        ls_struc[k]=(str(num_stem)+'L')
                        ls_temp.append(str(num_stem)+'L')
                    elif string_strc[k]=='.':
                        ls_struc[k]='B'
                    num_stem1=len(ls_temp)
                    #print(num_stem1)
                elif ls_loop[0][1]<=k<=ls_loop1[0][1]:
                    if string_strc[k]=='>' and (ls_struc[k]).isnumeric():                       
                        ls_struc[k]=(str(num_stem1)+'R')
                        num_stem1-=1
                    elif string_strc[k]=='.':
                        ls_struc[k]='B'
            elif len(ls_loop1)>1:
                
                for m in range(len(ls_loop1)-1):
                    #if ls_loop[m][0]<k<ls_loop[m][1]:
                        #ls_struc.append('p')
                    if ls_loop1[m][0]<=k<=ls_loop[m][0]:
                        if string_strc[k]=='<':

                            num_stem+=1
                            ls_struc[k]=(str(num_stem)+'L')
                            ls_temp.append(str(num_stem)+'L')
                        elif string_strc[k]=='.':
                            ls_struc[k]='B'
                        num_stem1=len(ls_temp)
                        #print(num_stem1)
                    elif ls_loop[m][1]<=k<=ls_loop1[m][1]:
                        if string_strc[k]=='>':                     
                            ls_struc[k]=(str(num_stem1)+'R')
                            num_stem1-=1
                        elif string_strc[k]=='.':
                            ls_struc[k]='B'
                if ls_loop1[-1][0]<=k<=int(ls_loop[-1][0]):
                    if string_strc[k]=='<':

                        num_stem+=1
                        ls_struc[k]=(str(num_stem)+'L')
                        ls_temp.append(str(num_stem)+'L')

                    elif string_strc[k]=='.':
                        ls_struc[k]='B'
                    num_stem1=len(ls_temp)
                    #print(num_stem1)
                elif ls_loop[-1][1]<=k<=ls_loop1[-1][1]:
                    if string_strc[k]=='>':                     
                        ls_struc[k]=(str(num_stem1)+'R')
                        num_stem1-=1
                    elif string_strc[k]=='.':
                        ls_struc[k]='B'
                                
    return(ls_stem,ls_struc,num_stem,num_stem1,ls_temp)
def make_strc_info(string):
    print('make_strc_info start')
    string1=string
    ls_loop_new=[]
    ls_loop1_new=[]
    num_cycle=0
    ls_stem=[]
    ls_struc=[]
    ls_temp=[]
    num_stem=0
    num_stem1=0
    while re.search('<\.+>',string):
        num_cycle+=1
        #string_strc,string,ls_loop,ls_loop_new,ls_loop1,ls_loop1_new
        string_strc,string,ls_loop,ls_loop_new,ls_loop1,ls_loop1_new=findloop(string,ls_loop_new,ls_loop1_new)
        
        ls_stem,ls_struc,num_stem,num_stem1,ls_temp=mark_stem_struc(string_strc,string1,ls_loop,ls_loop1,ls_stem,ls_struc,num_cycle,num_stem,num_stem1,ls_temp)
                 

    same_stem='/'.join(ls_stem)
    Mutation_struc='/'.join(ls_struc)
    #print(same_stem)
    #print(Mutation_struc)
    return(same_stem,Mutation_struc)

    
##########################################################is part2 of make_mu_structure2_riboswitch.py


    #ls:same_stem=0/1/2/3/s3_0/s3_0/s3_0/7/8/9/s2_0/s2_0/s2_0/13/s1_0/s1_0/16/17/s1_0/s1_0/20/s1_1/s1_1/s1_1/s1_1/s1_1/s1_1/s1_1/28/29/30/31/s1_1/s1_1/s1_1/s1_1/s1_1/s1_1/s1_1/39/s2_0/s2_0/s2_0/43/s2_1/s2_1/46/47/s1_2/s1_2/s1_2/51/52/s1_2/s1_2/s1_2/s1_3/s1_3/s1_3/59/60/s1_3/s1_3/s1_3/64/65/s2_1/s2_1/68/69/70/s3_0/s3_0/s3_0/74
    #ls1:Mutation_struc=5s/5s/5s/5s/21L/22L/23L/7/8/9/16L/17L/18L/13/1L/2L/p/p/2R/1R/20/3L/4L/5L/6L/7L/8L/9L/p/p/p/p/9R/8R/7R/6R/5R/4R/3R/39/18R/17R/16R/43/19L/20L/46/47/10L/11L/12L/p/p/12R/11R/10R/13L/14L/15L/p/p/15R/14R/13R/64/65/20R/19R/68/69/70/23R/22R/21R/3s

#2 represents base pairs that show at least one instance of covariation, 1 means there is at least one compatible mutation, 0 (zero) meansthere are no mutations, so no data. ? means that there are too many non-canonical base pairs.
def count_stem(line):   
    num_com=0
    num_conser=0
    num_pair=0
    num_cov=0
    for i in line:
        if i=='1':
            num_com+=1
        elif i=='0':
            num_conser+=1
        elif i=='?':
            num_pair+=1
        elif i=='2':
            num_cov+=1

    num_all_pair=num_com+num_conser+num_pair+num_cov
    stem_count=str(num_cov//2)+'_'+str(num_com//2)+'_'+str(num_conser//2)+'_'+str(num_all_pair//2)
    return(stem_count)
def process_files_for_struc_note(input_fold_seq_stuc,output_folder_seq_struc_add):
    files_seq_struc = [f for f in os.listdir(input_fold_seq_stuc) if f.endswith('.seqStruc')]
    #print(files_seq_struc)

    #files_seq_struc = os.listdir(input_fold_seq_stuc)

    for file_seq_struc in files_seq_struc:
        process_single_seq_struc_file1(input_fold_seq_stuc, output_folder_seq_struc_add, file_seq_struc)
def process_single_seq_struc_file1(input_fold_seq_stuc, output_folder_seq_struc_add, file_seq_struc):
    print('process_single_seq_struc_file1 start')
    input_file=input_fold_seq_stuc / file_seq_struc
    output_file=output_folder_seq_struc_add / (file_seq_struc[0:-9]+".seqStrucAdd")
    foo=open('no_struc_mark.txt','w')
    with open(input_file, "r") as fi_seq_struc:
        with open(output_file,'w') as fo_seq_struc:
            ls_seq={}
            ls_num=[]
            #print(ff)
            for line in fi_seq_struc.readlines():
                a=re.findall('^#=GC SS_cons|#=GC cov_SS_cons|#=GF NUM_COV',line)
                if line=="\n":
                    pass
                #elif 'refseqgene' in line:
                    #str_seq=line.split()[-1]   
                    #seq=str_seq.replace('-','')
                    #ls_seq[line.strip()]=len(seq)
                elif not a:

                    str_seq=line.split()[-1]
                    seq=str_seq.replace('.','')
                    ls_seq[line.strip()]=len(seq)
                elif a:
                    if '#=GC SS_cons' in line:
                        #fo.write(line)
                        ls_id2='#=GC SS_cons'

                        line4=f'{ls_id2:<45}'+line.strip().split()[-1]+'\n'
                        ls=line.strip().split()
                        #str1='....<<<....<<<<<<<....>>>>>>>..<<..<<<..>>><<<..>>>..>>...>>>.'
                        str1=ls[-1]
                        same_stem,Mutation_struc=make_strc_info(str1)
                        #same_stem=0/1/2/3/s3_0/s3_0/s3_0/7/8/9/s2_0/s2_0/s2_0/13/s1_0/s1_0/16/17/s1_0/s1_0/20/s1_1/s1_1/s1_1/s1_1/s1_1/s1_1/s1_1/28/29/30/31/s1_1/s1_1/s1_1/s1_1/s1_1/s1_1/s1_1/39/s2_0/s2_0/s2_0/43/s2_1/s2_1/46/47/s1_2/s1_2/s1_2/51/52/s1_2/s1_2/s1_2/s1_3/s1_3/s1_3/59/60/s1_3/s1_3/s1_3/64/65/s2_1/s2_1/68/69/70/s3_0/s3_0/s3_0/74
                        #Mutation_struc=5s/5s/5s/5s/21L/22L/23L/7/8/9/16L/17L/18L/13/1L/2L/p/p/2R/1R/20/3L/4L/5L/6L/7L/8L/9L/p/p/p/p/9R/8R/7R/6R/5R/4R/3R/39/18R/17R/16R/43/19L/20L/46/47/10L/11L/12L/p/p/12R/11R/10R/13L/14L/15L/p/p/15R/14R/13R/64/65/20R/19R/68/69/70/23R/22R/21R/3s

                        ls_ss=same_stem.split('/')
                        ls1=Mutation_struc.split('/')
                        
                        string1='#=SMD same_stem'
                        string2='#=SMD mutation_struc'
                        line1=f'{string1:<45}'+'/'.join(ls_ss)+'\n'
                        line2=f'{string2:<45}'+'/'.join(ls1)+'\n'
                            
                        #fo.write(line1)
                        #fo.write(line2)
                    elif '#=GC cov_SS_cons' in line:
                        #'#=GC cov_SS_cons                             .....?2202........2..22.22?.......................................................................................?22.2.2.2222...022?2?.........................................?2?....220.222....................................................2022?...222?....................................................?222.................'
                        #fo.write(line) 
                        ls3=line.strip().split()
                        line5_id='#=GC cov_SS_cons'
                        line5=f'{line5_id:<45}'+ls3[-1]+'\n'
                        string3='#=SMD stem_count'
                        line3=f'{string3:<45}'+count_stem(line)+"\n"
                        #fo.write(line3)
                    #else:
                        #line6=line
            ls_num_seq = sorted(ls_seq.items(),key=lambda x:x[1],reverse = False)
            #print(ls_num)
            num_seq=0
            for k in range(len(ls_num_seq)):
                if 20<ls_num_seq[k][1]:
                    num_seq+=1
                    ls2=ls_num_seq[k][0].split()
                    #print(ls)
                    seq_id=ls2[0]+'_'+str(ls_num_seq[k][1])
                    sequence=ls2[-1]
                    refseq=f'{seq_id:<45}'+sequence+'\n'
                    fo_seq_struc.write(refseq)
            fo_seq_struc.write(line4)
            fo_seq_struc.write(line1)
            fo_seq_struc.write(line5)
            #fo.write(line)
            fo_seq_struc.write(line2)
            fo_seq_struc.write(line3)
            #fo_seq_struc.write(line6)
            if num_seq==0:
                ff=file_seq_struc+'\n'
                foo.write(ff)
############################################################make mutation from test_make_mutation.py and make_mu_struc3.py 
def cov_po(b):
    if b[-1]=='l':
        d=b[0:-1]+'r'
        return(d)
    elif b[-1]=='L':
        d=b[0:-1]+'R'
        return(d)
    elif b[-1]=='r':
        d=b[0:-1]+'l'
        return(d)
    elif b[-1]=='R':
        d=b[0:-1]+'L'
        return(d)

def multi_sub(string,p,c):
    new = []
    for s in string:
        new.append(s)
    for index,point in enumerate(p):
        new[point] = c[index]
    return ''.join(new)


#::11111--11111.-------11111-111_____111-11111--------11111--11111,,,,,,,,,,,,,,,,,,,,,2222-----22______22----2222--------00000---0000,,,,,,,,.,3333333.____________333-------3333,,,,,,,,,,,,,,,,.,,,,,,44-44444___________4444444,,,,,,,0000-00000::::::::::::::::::::::
#..1??0?..000?1........?1000.10?.....?01.0001?........1?000..?0??1.....................?1?0.....?2......2?....0?1?........?0???...00?1..........?02??0?.............?0?.......?20?.......................01.??001...........100??10.......1?00.???0?......................  
#ls_str1=[aatcc-tcga,aa-tctcga]
#str4=5s/5s/5s/5s/21L/22L/23L/7/8/9/16L/17L/18L/13/1L/2L/p/p/2R/1R/20/
#str3o=????..??...............??2.
#判断共序列配对是否存在于序列中，给每条序列修正结构信息
def modi_basepair(str4,str3o,str1): 
    ls=['CG','GC','AU','UA','GU','UG','AT','TA','TG','GT']
    ls1=['1','0','?','2']
    ls_com=str4.split('/')
    ls4=[]
    for i in range(len(str3o)):
        if str3o[i] in ls1:
            #print(i)
            n=ls_com[i]
            m=cov_po(n)
            j=ls_com.index(m)
            basepair=str1[i]+str1[j]
            if basepair not in ls:
                #print(basepair)
                #print(i,j)
                ls4.append('.')
            else:
                ls4.append(str3o[i])
        else:
            ls4.append(str3o[i])
    #str3=modi_basepair(str4,str3,str1)
    str3=''.join(ls4)
    return(str3)
##count number for structure feature, dic={stem_s1_0:num_cov},dic1={stem_:num_com},dic2={stem_:cons}
def stem_cov_num(line1,line2):
    print('stem_cov_num start')
    #print(line1)
    #print(line2)
    #line1=str5='s1_1,s1_1'
    #line2=str3='?..22'

    ls=[]  #all stem_num
    ls1=[]
    ls_stem=['0','1','2','?']
    dic={}
    dic1={}
    dic2={}
    #matches = re.findall(r's[^/]+', line)
    #line1=line1.replace('/',',')
    line=re.findall(r's[^/]+',line1)
    #print(line)
    #line=[s1_0,s1_0]
    #line=1111111111111111111111111111111111112222222222220000000003333333333333344444444444444000000000
    for i in range(len(line)):
        if line[i] not in ls:
            ls.append(line[i])
    #print(ls)
        
    ls_line1=line1.split('/')
    for j in ls:
        num=0  #covariation
        num1=0  #lenth_stem
        com=0  #compatiable mutation
        conser=0
        stem=0  #consertive basepair
        for k in range(len(line2)):
            if ls_line1[k]==j:
                num1+=1
                if line2[k]=='2':
                    num+=1
                elif line2[k]=='1':
                    com+=1
                elif line2[k]=='0':
                    conser+=1
                elif line2[k]=='?':
                    stem+=1

                else:
                    pass
        
        if num1/2>1:
            dic['stem_'+j+'-'+str(int(num1/2))]=int(num/2)
            dic1['stem_'+j+'-'+str(int(num1/2))]=int(com/2)
            dic2['stem_'+j+'-'+str(int(num1/2))]=int(conser/2)
    dic=sorted(dic.items(), key=lambda item:item[1], reverse=True)
    dic1=sorted(dic1.items(), key=lambda item:item[1], reverse=True)
    dic2=sorted(dic2.items(), key=lambda item:item[1], reverse=True)
    #print(dic)
    print('stem_cov_num ended')
    return(dic,dic1,dic2)
#cov>1
def pick_stem(dic1):
#dic1={stem_s1_0-5:1,stem_s1_1-5:1,stem_s2_0-5:1}
    print('pick_stem start')
    if len(dic1)==1:
        num2=dic1[0][0].split('-')[0][5::]
        return num2
    elif len(dic1)>1:
        if dic1[0][1]!= dic1[1][1]:
            num2=dic1[0][0].split('-')[0][5::]
        #if numcov same,choose long stem
        else:
            dic_same_cov={}
            for i in range(len(dic1)):
                if dic1[i][1]==dic1[0][1]:
                    dic_same_cov[(dic1[0][0].split('-')[0])]=dic1[0][0].split('-')[1]
            dic_same_cov=sorted(dic_same_cov.items(), key=lambda item:item[1], reverse=True)
            num2=dic_same_cov[0][0][5::]
        return num2
####cov_num>1     
def mu_po(num,str5,str3,str1,str4,num1):
    print('mu_po start')
    ls_str5=str5.split('/')
    po=[]
    nt=[]
    p0=[]
    n0=[]
    p1=[]
    n2=[]
    dic={}
    ls1=['CG','GC','AU','UA','GU','UG','AT','TA','TG','GT']
    index=[]
    ls_com=str4.split('/')
    for i in range(len(str1)):
        
        if ls_str5[i]==num and str3[i]==num1 and i not in index:
            n=ls_com[i]
            n1=cov_po(n)
            m=ls_com.index(n1)
            mu1=str1[i]+str1[m]
            if mu1 in ls1:

                po.append(i)    
                po.append(m)
                index.append(m)
                nt.append(str1[m])
                nt.append(str1[i])

    num_cov=len(po)
    if num_cov==4:
        p0=po
        n0=nt
        p1.append(p0[0])
        p1.append(p0[2])
        n2.append(n0[0])
        n2.append(n0[2])
        
    elif num_cov>4:
        if (num_cov/2)%2==0:
            num1=int(num_cov/2)-2
            
        elif (num_cov/2)%2==1:
            num1=int(num_cov/2)-1
        p0.append(po[num1])
        p0.append(po[num1+1])
        p0.append(po[num1+2])
        p0.append(po[num1+3])
        n0.append(nt[num1])
        n0.append(nt[num1+1])
        n0.append(nt[num1+2])
        n0.append(nt[num1+3])
        p1.append(p0[0])
        p1.append(p0[2])
        n2.append(n0[0])
        n2.append(n0[2])
    return(p1,n2,p0,n0) 
#cov==1 
def mu_po1(num,str5,str3,str1,str4):
    print('mu_po1 start')
    #print(num)
    #print(str5)
    ls_str5=str5.split('/')
    po=[]
    nt=[]
    p0=[]
    n0=[]
    p1=[]
    n2=[]
    dic={}
    ls1=['CG','GC','AU','UA','GU','UG']
    index=[]
    ls_com=str4.split('/')
    for i in range(len(str1)):
        if ls_str5[i]==num and str3[i]=='2' and i not in index:
            #print(str5[i])
            n=ls_com[i]

            n1=cov_po(n)
            m=ls_com.index(n1)
            mu1=str1[i]+str1[m]
            if mu1 in ls1:
                po.append(i)    
                po.append(m)
                index.append(m)
                nt.append(str1[m])
                nt.append(str1[i])
    
    dic1,dic2,dic3=stem_cov_num(str5,str3)
    #print(dic1)
   #[('stem_s1_0-3', 1), ('stem_s1_1-2', 1)]
    for j in dic2:
        #print(dic2)
        if j[0].split('-')[0][5::]==num:
            print(j[0])
            num_com=int(j[1])
            #print(num_com)

    for k in dic3:
        if k[0].split('-')[0][5::]==num:
            num_conser=int(k[-1])
    if num_com>=1:
        for i in range(len(str1)):
            if ls_str5[i]==num and str3[i]=='1':
                n=ls_com[i]
                n1=cov_po(n)
                m=ls_com.index(n1)
                mu1=str1[i]+str1[m]
                if mu1 in ls1:
                    po.append(i)    
                    po.append(m)
                    #index.append(m)
                    nt.append(str1[m])
                    nt.append(str1[i])
                    break
            else:
                pass
    elif num_com==0:
        if num_conser>=1:
            for i in range(len(str1)):
                if ls_str5[i]==num and str3[i]=='0':
                    n=ls_com[i]
                    n1=cov_po(n)
                    m=ls_com.index(n1)
                    mu1=str1[i]+str1[m]
                    if mu1 in ls1:
                        po.append(i)    
                        po.append(m)
                        #index.append(m)
                        nt.append(str1[m])
                        nt.append(str1[i])
                        break
        elif num_conser==0:
            for i in range(len(str1)):
                if ls_str5[i]==num and str3[i]=='?':
                    n=ls_com[i]
                    n1=cov_po(n)
                    m=ls_com.index(n1)
                    mu1=str1[i]+str1[m]
                    if mu1 in ls1:
                        po.append(i)    
                        po.append(m)
                        #index.append(m)
                        nt.append(str1[m])
                        nt.append(str1[i])
                        break
    p1.append(po[0])
    p1.append(po[2])
    n2.append(nt[0])
    n2.append(nt[2])
    print('mu_po1 ended')
    return(p1,n2,po,nt)

#com==1
def mu_po2(num,str5,str3,str1,str4):
    print('mu_po2 start')
    ls_str5=str5.split('/')
    po=[]
    nt=[]
    p0=[]
    n0=[]
    p1=[]
    n2=[]
    dic={}
    ls1=['CG','GC','AU','UA','GU','UG']
    index=[]
    ls_com=str4.split('/')
    for i in range(len(str1)):
        if ls_str5[i]==num and str3[i]=='1' and i not in index:
            n=ls_com[i]
            n1=cov_po(n)
            m=ls_com.index(n1)
            mu1=str1[i]+str1[m]
            if mu1 in ls1:
                po.append(i)    
                po.append(m)
                index.append(m)
                nt.append(str1[m])
                nt.append(str1[i])
    dic1,dic2,dic3=stem_cov_num(str5,str3)
    #print(dic1)
    #([('stem2-3', 1), ('stem3-5', 1), ('stem0-4', 0), ('stem1-17', 0), ('stem4-7', 0)], 
#[('stem1-17', 4), ('stem4-7', 2), ('stem2-3', 1), ('stem0-4', 1), ('stem3-5', 0)], 
#[('stem1-17', 8), ('stem0-4', 3), ('stem4-7', 3), ('stem3-5', 2), ('stem2-3', 1)])
     
#111____111,,,,,,,,,,,2222______2222-333__________________333:::::
#00?....?00...........0?0?......?0?0.1??..................??1.....  
    for k in dic3:
        if k[0].split('-')[0][-1]==num:
            num_conser=int(k[-1])
    if num_conser>=1:
        for i in range(len(str1)):
            if str5[i]==num and str3[i]=='0':
                n=ls_com[i]
                n1=cov_po(n)
                m=ls_com.index(n1)
                mu1=str1[i]+str1[m]
                if mu1 in ls1:
                    po.append(i)    
                    po.append(m)
                    #index.append(m)
                    nt.append(str1[m])
                    nt.append(str1[i])
                    break
            else:
                pass
    elif num_conser==0:
        for i in range(len(str1)):
            if str5[i]==num and str3[i]=='?':
                n=ls_com[i]
                n1=cov_po(n)
                m=ls_com.index(n1)
                mu1=str1[i]+str1[m]
                if mu1 in ls1:
                    po.append(i)    
                    po.append(m)
                    #index.append(m)
                    nt.append(str1[m])
                    nt.append(str1[i])
                    break
    p1.append(po[0])
    p1.append(po[2])
    n2.append(nt[0])
    n2.append(nt[2])
    return(p1,n2,po,nt)
#conser==1
def mu_po3(num,str5,str3,str1,str4):
    print('mu_po3 start')
    ls_str5=str5.split('/')
    po=[]
    nt=[]
    p0=[]
    n0=[]
    p1=[]
    n2=[]
    dic={}
    ls1=['CG','GC','AU','UA','GU','UG']
    index=[]
    ls_com=str4.split('/')
    for i in range(len(str1)):
        if ls_str5[i]==num and str3[i]=='0' and i not in index:
            n=ls_com[i]
            n1=cov_po(n)
            m=ls_com.index(n1)
            mu1=str1[i]+str1[m]
            if mu1 in ls1:
                po.append(i)    
                po.append(m)
                index.append(m)
                nt.append(str1[m])
                nt.append(str1[i])
    dic1,dic2,dic3=stem_cov_num(str5,str3)
    #print(dic1)
    #([('stem2-3', 1), ('stem3-5', 1), ('stem0-4', 0), ('stem1-17', 0), ('stem4-7', 0)], 
#[('stem1-17', 4), ('stem4-7', 2), ('stem2-3', 1), ('stem0-4', 1), ('stem3-5', 0)], 
#[('stem1-17', 8), ('stem0-4', 3), ('stem4-7', 3), ('stem3-5', 2), ('stem2-3', 1)])
    
            #print(num_com)
    for i in range(len(str1)):
        if ls_str5[i].startswith('s') and str3[i]=='0' and i not in po and i not in index:
            n=ls_com[i]
            n1=cov_po(n)
            m=ls_com.index(n1)
            mu1=str1[i]+str1[m]
            if mu1 in ls1:
                po.append(i)    
                po.append(m)
                #index.append(m)
                nt.append(str1[m])
                nt.append(str1[i])
                break
    
    
    p1.append(po[0])
    p1.append(po[2])
    n2.append(nt[0])
    n2.append(nt[2])
    return(p1,n2,po,nt)
def process_files_make_mutation(input_folder_structure_add,output_fold_fa):
    print('process_files_make_mutation start')
    structure_files = [f for f in os.listdir(input_folder_structure_add) if f.endswith('.seqStrucAdd')]
    #print(structure_files)


    structure_files=os.listdir(input_folder_structure_add)
    for file in structure_files:

        process_single_structure_add(input_folder_structure_add,file,output_fold_fa)
def process_single_structure_add(input_folder_structure_add,file,output_fold_fa):
    print('process_single_structure_add start')
    input_file_struc=input_folder_structure_add / file
    #print(input_file_struc)
    fi=open(input_file_struc,"r")
    j=file.strip()[0:-12]+".mu.fa"
    output_file_fa=output_fold_fa / j

    fo=open(output_file_fa,"w")
    ls=fi.readlines()
    seq_mu_id=''
    ls_com=[]
    num_cov=0
    num_com=0
    num_conser=0
    dic=[]
    ls_str1=[]
    num_str1=0
    ls_seq_id=[]
    ls_seq_wild=[]
    ls_seq_mu_id=[]
    for line in ls:
        a=re.findall('^\w+\d+',line)
        b=re.findall('#=GC SS_cons',line)
        c=re.findall('#=GC cov_SS_cons',line)
        d=re.findall('#=SMD mutation_struc',line)
        e=re.findall('#=GF NUM_COV',line)
        f=re.findall('#=SMD same_stem',line)
        
        if a:

            #string.replace(oldvalue, newvalue, count)
            num_str1+=1
            ls=line.strip().split()
            seq_mu_id=ls[0]
            seq_id='>'+'w'+str(num_str1)+'_'+ls[0]+'\n'
            seq=ls[-1].replace('.','').replace('-','')+'\n'
            #fo.write(seq_id)
            #fo.write(seq)
            ls_seq_id.append(seq_id)
            ls_seq_wild.append(seq)
            ls_str1.append(ls[-1])
            ls_seq_mu_id.append(seq_mu_id)          
            
        elif b:
#(((((--((,,,,,,,,,,,,,,,<<<--------<<<<<<<______________>>>>>>>>>>,,,,.
            str2=line.strip().split()[-1]
        elif c:
#1????..??...............??2........??00?1?..............?1?00??2??.....
            str3o=line.strip().split()[-1]
            
        elif d:
            #5s/5s/5s/5s/21L/22L/23L/7/8/9/16L/17L/18L/13/1L/2L/p/p/2R/1R/20/3L/4L/5L/6L/7L/8L/9L/p/p/p/p/9R/8R/7R/6R/5R/4R/3R/39/18R/17R/16R/43/19L/20L/46/47/10L/11L/12L/p/p/12R/11R/10R/13L/14L/15L/p/p/15R/14R/13R/64/65/20R/19R/68/69/70/23R/22R/21R/3s
            str4=line.strip().split()[-1]
            ls_com=str4.split('/')

        #elif e:
#4    2    8  13
            #ls_stem=line.strip().split()
            #num_cov=int(ls_stem[-4])
            #num_com=int(ls_stem[-3])
            #num_conser=int(ls_stem[-2])
            #num_all_pair=int(ls_stem[-1])
        elif f:
            #0/1/2/3/s3_0/s3_0/s3_0/7/8/9/s2_0/s2_0/s2_0/13/s1_0/s1_0/16/17/s1_0/s1_0/20/s1_1/s1_1/s1_1/s1_1/s1_1/s1_1/s1_1/28/29/30/31/s1_1/s1_1/s1_1/s1_1/s1_1/s1_1/s1_1/39/s2_0/s2_0/s2_0/43/s2_1/s2_1/46/47/s1_2/s1_2/s1_2/51/52/s1_2/s1_2/s1_2/s1_3/s1_3/s1_3/59/60/s1_3/s1_3/s1_3/64/65/s2_1/s2_1/68/69/70/s3_0/s3_0/s3_0/74
#:::::::::::.::::1111.11111,,,,,,,,,,,,222--22222____22222--22233333333--33333_____..333333333333311111--1111:
            str5=line.strip().split()[-1]
            #dic=stem_num(str5)
            #[('3stem', 13), ('1stem', 9), ('2stem', 8)]
    #print(ls_str1)
    #print(str2)
    #print(str3)
    #print(str5)
    #ls_str1=[aatcc-tcga,aa-tctcga]
    #str4=5s/5s/5s/5s/21L/22L/23L/7/8/9/16L/17L/18L/13/1L/2L/p/p/2R/1R/20/
    #str3o=????..??...............??2.
    for m in range(len(ls_str1)):
        ##str3=????..2?...............??2.
        str3=modi_basepair(str4,str3o,ls_str1[m])
        #print(str3)
        dic1=[]  #cov
        dic2=[]  #com
        dic3=[]  #conserve
        #dic1={stem_s1_0:num_cov},dic2={stem_:num_com},dic3={stem_:cons}
        #ls_str5=str5.split('/')
        dic1,dic2,dic3=stem_cov_num(str5,str3)
        #print(dic1)
        #print(dic2)
        #print(dic3)
        num_all_pair=0
        for i in dic1:
            num_all_pair+=int(i[0].split('-')[-1])
    
#[('stem_s1_0-3', 1), ('stem_s1_1-2', 1)]
#[('stem_s1_1-2', 1), ('stem_s1_0-3', 0)]
#[('stem_s1_0-3', 1), ('stem_s1_1-2', 0)]

        if num_all_pair>2:
            print('structure work')
            

            if dic1[0][1]>1:
                num2=pick_stem(dic1)
                
                p1,n2,p0,n0=mu_po(num2,str5,str3,ls_str1[m],str4,'2')
                
            elif dic1[0][1]==1:
                num2=pick_stem(dic1)
                #print(ls_str5)
                p1,n2,p0,n0=mu_po1(num2,str5,str3,ls_str1[m],str4)
                #print(p1)
            elif dic1[0][1]==0:
                if dic2[0][1]>1:
                    num2=pick_stem(dic2)
                    p1,n2,p0,n0=mu_po(num2,str5,str3,ls_str1[m],str4,'1')
                elif dic2[0][1]==1:
                    num2=pick_stem(dic2)
                    p1,n2,p0,n0=mu_po2(num2,str5,str3,ls_str1[m],str4)
                elif dic2[0][1]==0:
                    if dic3[0][1]>1:
                        num2=pick_stem(dic3)
                        p1,n2,p0,n0=mu_po(num2,str5,str3,ls_str1[m],str4,'0')
                    elif dic3[0][1]==1:
                        num2=pick_stem(dic3)
                        p1,n2,p0,n0=mu_po3(num2,str5,str3,ls_str1[m],str4)
                    elif dic3[0][1]==0:
    #[('stem1-17', 8), ('stem0-4', 3), ('stem4-7', 3), ('stem3-5', 2), ('stem2-3', 1)]
                        num2=dic4[0][0][-1]
                        if dic4[0][1]>1:
                            p1,n2,p0,n0=mu_po(num2,str5,str3,ls_str1[m],str4,'?')
            seq_mu1=multi_sub(ls_str1[m],p1,n2)+'\n'
            seq_mu2=multi_sub(ls_str1[m],p0,n0)+'\n'
        #seq_mu1=seq_mu.replace('-','')+'\n'
            seq_mu1_id=">"+'m'+str(m+1)+'_1'+'_'+ls_seq_mu_id[m]+'\n'
            seq_mu2_id=">"+'m'+str(m+1)+'_2'+'_'+ls_seq_mu_id[m]+'\n'
            fo.write(ls_seq_id[m])
            fo.write(ls_seq_wild[m])
            fo.write(seq_mu1_id)
            fo.write(seq_mu1.replace('.','').replace('-',''))
            fo.write(seq_mu2_id)
            fo.write(seq_mu2.replace('.','').replace('-',''))
            print('mutation successfully')
        #fo.write(p1,n2,p0,n0)
        else:

            print(':no structure')
    print('single_structure_add ended')

# Main script
def main():

    input_folder = get_user_input()
    
    #print(r2r_path)
    if input_folder.name=='test':
        input_folder=input_folder/'demo'

        output_folder_r2r = Path('./test/riboswitch_cons_sto_test')
        output_folder_seq_struc = Path('./test/seq_struc_riboswitch_test/')
        output_folder_seq_struc_add=Path('./test/seq_struc_riboswitch_add_test')
        output_fold_fa=Path('./test/seq_struc_mu_test')
        no_struc_ribo_file = 'no_struc_ribo_test.txt'

        output_folders = [output_folder_r2r, output_folder_seq_struc,output_folder_seq_struc_add,output_fold_fa]
        create_output_folders(output_folders)

    # Call your function with the r2r_path parameter
        process_files_for_r2r(input_folder, output_folder_r2r)



        #process_files_for_r2r(input_folder, output_folder_r2r)
        print('R2R run finished')
        process_files_for_seq_struc(output_folder_r2r, output_folder_seq_struc, no_struc_ribo_file)
        print('common style finished')
        process_files_for_struc_note(output_folder_seq_struc,output_folder_seq_struc_add)
        print('structure feature added' )
        process_files_make_mutation(output_folder_seq_struc_add,output_fold_fa)
        print('mutation design finished')
        for folder in [output_folder_r2r, output_folder_seq_struc, output_folder_seq_struc_add]:
            if folder.exists() and folder.is_dir():
                # Check if the folder is not empty
                if not os.listdir(folder):
                    # If the folder is empty, remove it
                    folder.rmdir()
                else:
                    # If the folder is not empty, remove it along with all its contents
                    shutil.rmtree(folder)
        print('test finished')

    else:
        input_folder_sample = input_folder.parents[0]
        #print(input_folder_sample)
        output_folder_r2r = input_folder_sample.joinpath( 'r2r_cons_sto')
        #output_folder_r2r = Path(input_folder_sample+'/sample/r2r_cons_sto/')

        output_folder_seq_struc = input_folder_sample.joinpath('seq_struc')
        output_folder_seq_struc_add=input_folder_sample.joinpath('seq_struc_add')
        output_fold_fa=input_folder_sample.joinpath('seq_struc_mu')
        no_struc_ribo_file = 'no_struc.txt'

        output_folders = [output_folder_r2r, output_folder_seq_struc,output_folder_seq_struc_add,output_fold_fa]
        create_output_folders(output_folders)


    # Call your function with the r2r_path parameter
        process_files_for_r2r(input_folder, output_folder_r2r)

        #process_files_for_r2r(input_folder, output_folder_r2r)
        print('R2R run finished')
        process_files_for_seq_struc(output_folder_r2r, output_folder_seq_struc, no_struc_ribo_file)
        print('common style finished')
        process_files_for_struc_note(output_folder_seq_struc,output_folder_seq_struc_add)
        print('structure feature added' )
        process_files_make_mutation(output_folder_seq_struc_add,output_fold_fa)
        print('mutation design finished')
        

        for folder in [output_folder_r2r, output_folder_seq_struc, output_folder_seq_struc_add]:
            if folder.exists() and folder.is_dir():
                # Check if the folder is not empty
                if not os.listdir(folder):
                    # If the folder is empty, remove it
                    folder.rmdir()
                else:
                    # If the folder is not empty, remove it along with all its contents
                    shutil.rmtree(folder)



if __name__ == "__main__":
    script_path = Path(__file__).parent
    r2r_install_path = script_path / 'R2R_install.sh'
    
    try:
        if is_r2r_installed():
            print("R2R already installed.")
            main()
        else:
            print("R2R is not installed. Installing now...")
            install_r2r(r2r_install_path)
            if is_r2r_installed():
                print("R2R installed successfully.")
                print("Calling main() after installation.")
                main()
            else:
                print("Failed to install R2R.")
                print('install R2R manually')
    except Exception as e:
        print(f"An error occurred: {e}")

    
