import os
from pathlib import Path
import re



def check_input_folder(input_folder):
    if not input_folder.exists() or not input_folder.is_dir():
        print(f"Error: The specified input folder '{input_folder}' does not exist or is not a directory.")
        exit()

def create_output_folders(output_folders):
    #seq_struc_riboswitch_add
    for folder in output_folders:
        if not folder.exists():
            folder.mkdir()

def process_files_for_r2r_draw1(input_folder,output_folder):
	files=os.listdir(input_folder)
	for file in files:
		fi_input=input_folder/file
		fo_output=output_folder/file
		fi=open(fi_input,'r')
		fo=open(fo_output,'w')
		for line in fi.readlines():
			if line.startswith('//'):
				line_add='#=GF R2R SetDrawingParam autoBreakPairs true'+'\n'
				fo.write(line_add)
				fo.write('//')
				break
			else:
				fo.write(line)

def make_meta_file(input_folder1,input_folder2,output_folder):
	files=os.listdir(input_folder1)
	for file in files:
		if file.endswith('.cons.sto'):
			fi_input=input_folder1/file
			file1=file.split('.')[0]+'.sto'
			fi_input2=input_folder2/file1
			fi=open(fi_input,'r')
			n=0
			for line in fi.readlines():
				
				
				if line.startswith('//'):
					break
				elif line.startswith('#'):
					continue
				else:
					try:
						split_line=line.split()
						if split_line:
							n+=1
							file_name=file.split('.')[0]+'_'+str(n)+'.r2r_meta'
							fo_output=output_folder/file_name
							with open(fo_output,'w',encoding='utf-8') as fo:
							
								lines=str(fi_input2)+'\t'+'oneseq'+'\t'+split_line[0]
								if n==1:
									first_line=str(fi_input)+'\n'
									fo.write(first_line)
									fo.write(lines)
								else:
									fo.write(lines)
							
						else:
							#print(f'line is enmpty after splitting:{line}')
							continue
					except Exception as e:
						print(f"Error processing line: {line}. Error: {e}")
				
	                    #print()


def process_files_for_r2r_pdf(input_folder,output_folder):
	#r2r --disable-usage-warning /home/lijuanh/projects/def-jonatp/lijuanh/riboswitch_mu_design/meta/RF00442_6.r2r_meta RF00442_Guanidine1_Methylobacterium_4.pdf
	files=os.listdir(input_folder)
	for file in files:
		if file.endswith('.r2r_meta'):
			print(file)
			fi_input=input_folder/file
			#fi=open(fi_input,'r')
			fo_file=file.split('.')[0]+'.pdf'
			fo_output=output_folder/fo_file
			#fo=open(fo_output,'w')
			command_r2r_draw = f'r2r --disable-usage-warning {fi_input} {fo_output}'
			os.system(command_r2r_draw)
				#os.system(command_r2r_draw)

def main_r2r_test(input_folder):

    input_folder1=input_folder/'demo'
    #test/riboswitch_cons_sto_test
    input_folder=Path('./SMDesignerTest/riboswitch_cons_sto_test')

    r2r_draw1 = Path('./SMDesignerTest/r2r_cons_add_test')
    r2r_meta=Path('./SMDesignerTest/r2r_meta_test')
    r2r_pdf = Path('./SMDesignerTest/r2r_meta_pdf_test/')
    #input_folder=Path('riboswitch_sto1/')
    #./test/riboswitch_cons_sto_test
    

    output_folders = [r2r_draw1,r2r_meta,r2r_pdf]
    create_output_folders(output_folders)
    

    process_files_for_r2r_draw1(input_folder, r2r_draw1)
    print('r2r add GF')
    make_meta_file(r2r_draw1,input_folder1,r2r_meta)
    print('r2r making meta file')

    process_files_for_r2r_pdf(r2r_meta, r2r_pdf)
    #print('pdf work')
def main_r2r_sample(input_folder):

	input_folder_sample=input_folder.parents[0]
	input_folder1_sample=input_folder_sample / 'r2r_cons_sto'
	r2r_draw1=input_folder_sample.joinpath('r2r_cons_add')
	r2r_meta=input_folder_sample.joinpath('r2r_meta')
	r2r_pdf=input_folder_sample.joinpath('r2r_meta_pdf')
	output_folders = [r2r_draw1,r2r_meta,r2r_pdf]
	create_output_folders(output_folders)
	process_files_for_r2r_draw1(input_folder1_sample,r2r_draw1)
	make_meta_file(r2r_draw1,input_folder,r2r_meta)
	process_files_for_r2r_pdf(r2r_meta,r2r_pdf)







