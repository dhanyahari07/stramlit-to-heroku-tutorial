import streamlit as st
import os
import pandas as pd
import zipfile
import os
import pandas as pd
import chardet
import base64 
import io
import random
import shutil
import numpy as np
from glob import glob

import sys

class DevNull:
    def write(self, msg):
        pass

sys.stderr = DevNull()

@st.cache
def generate_random_number():
    return random.randint(1,500)

x = generate_random_number()

@st.cache(suppress_st_warning=True)
def option_generator():
	option = st.selectbox('Which option you are selecting?',('Select one option from here','during class', 'after class', 'after class with time'))
	return option

@st.cache(suppress_st_warning=True)
def ch_dir1():
    	os.chdir("..")

#os.chdir("..")
os.chdir("/home/nm_dhanya/dhanya")
st.write(os.getcwd())
df = pd.DataFrame()
#path=''
#option=option_generator()


datafile = st.file_uploader("Upload namelist with Roll Number as the column title",type=['xlsx'])
if datafile is not None:
		file_details = {"FileName":datafile.name,"FileType":datafile.type}
		df  = pd.read_excel(datafile)
		#st.dataframe(df)


datafile = st.file_uploader("Upload attendance zip file, zip directly within the folder",type=['zip'])
if datafile is not None:
		#n=0
		file_details = {"FileName":datafile.name,"FileType":datafile.type}
		with open(os.path.join(os.getcwd(),datafile.name),"wb") as f:
         		f.write(datafile.getbuffer())
		#cwd=os.getcwd()+"/"
		#if(n==0):
			#n = random.randint(1,500)
			#print(n)
		with zipfile.ZipFile(os.path.join(os.getcwd(),datafile.name),"r") as zf:
    				zf.extractall('attendance_'+str(x))
		# File name 
		file = datafile.name
    
		# File location 
		location = os.getcwd()
    
		# Path 
		path = os.path.join(location, file) 
    
		# Remove the file 
		# 'file.txt' 
		os.remove(path) 

		#path=''
		path=os.getcwd()+'/attendance_'+str(x)+'/'
		#path=os.getcwd()+'/attendance/'
		st.write(path)	
		path_chdir='attendance_'+str(x)
		#path_chdir='attendance'
		#else:
		#	print("")
option = st.selectbox('Which option you are selecting?',('select an option','during class', 'after class', 'after class with time'))
#option=option_generator()
if(option=='after class'):
 try:
	 set_diff_df=[]
	 val=[]
	 name_list=df
	 name_list['Roll Number']=name_list['Roll Number'].str.strip()
	 name_list['Roll Number']=name_list['Roll Number'].str.upper()
	 reg_no_full=name_list['Roll Number']
	
	 os.chdir(path_chdir)
	 for file in os.listdir():
	   if file.endswith(".csv"):
	     #st.write(file)
	     with open(path+file, 'rb') as f:
	               result = chardet.detect(f.read())
	     data = pd.read_csv(path+file,encoding=result['encoding'],sep='\t',skiprows = 6)
	     data['Full Name']=data['Full Name'].str.upper()
	     data.sort_values("Full Name", inplace = True)
	     data.drop_duplicates(subset ="Full Name",keep ='first', inplace = True)
	     data['Reg No']=data['Full Name'].apply(lambda st: st[st.find("[")+1:st.find("]")])
	     data["Join Time"] = data["Join Time"].apply(pd.to_datetime)
	     present=data['Reg No']
	     set_diff_df.append((pd.concat([reg_no_full, present, present]).drop_duplicates(keep=False)).to_string(index=False))
	     val.append(str(data['Join Time'].iloc[0].date().day)+'-'+str(data['Join Time'].iloc[0].date().month)+'-'+str(data['Join Time'].iloc[0].date().year))
	 new_val= pd.DataFrame(list(zip(val, set_diff_df)),columns =['date', 'absentees'])
	 path_parent = os.path.dirname(os.getcwd())
	 os.chdir(path_parent)
	 os.chdir("/home/nm_dhanya/dhanya")
	 #st.write("hello")
	 #path_excel=os.getcwd()+'/consolidated.xlsx' 
	 #new_val.to_excel(path_excel,index=False)


	 #data = pd.read_excel(os.getcwd()+'/consolidated.xlsx')
	 towrite = io.BytesIO()
	 downloaded_file = new_val.to_excel(towrite, encoding='utf-8', index=False, header=True)
	 towrite.seek(0)  # reset pointer
	 b64 = base64.b64encode(towrite.read()).decode()  # some strings
	 linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="consoliated.xlsx">Download excel file</a>'
	 st.markdown(linko, unsafe_allow_html=True)
	
	 print(os.getcwd())
	 # Directory name 
	 dir = 'attendance_'+str(x)    
	 # Parent Directory 
	 location = "."  
	 # path
	 path = os.path.join(location, dir)	  
	 # removing directory
	 shutil.rmtree(path,ignore_errors = False)
 except KeyError:
    print("")
elif(option=='during class'):
 try:
	 set_diff_df=[]
	 val=[]
	 name_list=df
	 name_list['Roll Number']=name_list['Roll Number'].str.strip()
	 name_list['Roll Number']=name_list['Roll Number'].str.upper()
	 reg_no_full=name_list['Roll Number']
	 #path='/content/attendance/'
	 os.chdir(path_chdir)
	 for file in os.listdir():
	  if file.endswith(".csv"):
	    print(file)
	    with open(path+file, 'rb') as f:
	              result = chardet.detect(f.read())
	    print(file)
	    data = pd.read_csv(path+file,encoding=result['encoding'],sep='\t') 
	    data['Full Name']=data['Full Name'].str.upper()
	    data.sort_values("Full Name", inplace = True) 
	    data.drop_duplicates(subset ="Full Name",keep ='first', inplace = True)
	    data['Reg No']=data['Full Name'].apply(lambda st: st[st.find("[")+1:st.find("]")])
	    data["Timestamp"] = data["Timestamp"].apply(pd.to_datetime)
	    present=data['Reg No']
	    set_diff_df.append((pd.concat([reg_no_full, present, present]).drop_duplicates(keep=False)).to_string(index=False))
	    val.append(str(data['Timestamp'].iloc[0].date().day)+'-'+str(data['Timestamp'].iloc[0].date().month)+'-'+str(data['Timestamp'].iloc[0].date().year))
          
	 new_val= pd.DataFrame(list(zip(val, set_diff_df)),columns =['date', 'absentees']) 
	 #new_val.to_excel('/content/consolidated.xlsx',index=False)
	 path_parent = os.path.dirname(os.getcwd())
	 os.chdir(path_parent)
	 os.chdir("/home/nm_dhanya/dhanya")
	 #st.write("hello")
	 #path_excel=os.getcwd()+'/consolidated.xlsx' 
	 #new_val.to_excel(path_excel,index=False)


	 #data = pd.read_excel(os.getcwd()+'/consolidated.xlsx')
	 towrite = io.BytesIO()
	 downloaded_file = new_val.to_excel(towrite, encoding='utf-8', index=False, header=True)
	 towrite.seek(0)  # reset pointer
	 b64 = base64.b64encode(towrite.read()).decode()  # some strings
	 linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="consoliated.xlsx">Download excel file</a>'
	 st.markdown(linko, unsafe_allow_html=True)
	
	 print(os.getcwd())
	 # Directory name 
	 dir = 'attendance_'+str(x)    
	 # Parent Directory 
	 location = "."  
	 # path
	 path = os.path.join(location, dir)	  
	 # removing directory
	 shutil.rmtree(path,ignore_errors = False)
 except pd.errors.ParserError:
	 print("")
elif(option=='after class with time'):
 try:	
		
		#sentence = st.text_input('Enter the time duration in minutes you want the student to be inside the class to mark as present:')
		#int_val = st.slider('Time in minuetes', min_value=1, max_value=120, value=5, step=1)
		int_val = st.number_input('Enter the time duration in minutes you want the student to be inside the class to mark as present', min_value=1, max_value=120, value=5, step=1)
		time_val=int_val
		set_diff_df=[]
		val=[]
		name_list=df
		name_list['Roll Number']=name_list['Roll Number'].str.strip()
		name_list['Roll Number']=name_list['Roll Number'].str.upper()
		reg_no_full=name_list['Roll Number']
		#path='/content/attendance/'
		os.chdir(path_chdir)
		for file in os.listdir():
    			if file.endswith(".csv"):
    				print(file)
	    		with open(path+file, 'rb') as f:
        		      result = chardet.detect(f.read())
	    		data = pd.read_csv(path+file,encoding=result['encoding'],sep='\t',skiprows = 6) 
	    		data['Full Name']=data['Full Name'].str.upper()    
	    		data['Reg No']=data['Full Name'].apply(lambda st: st[st.find("[")+1:st.find("]")])
	    		data["Join Time"] = data["Join Time"].apply(pd.to_datetime)
	    		new = data["Duration"].str.split(" ", n = 1, expand = True)
	    		data["T1"]= new[0]
	    		data["T2"]= new[1]

	    		data["T1"].fillna("0s",inplace=True)
	    		data["T2"].fillna("0s",inplace=True)

	    		data['Activity_1']=0
	    		data['Activity_2']=0

	    		# create a list of our conditions
	    		conditions = [(data['T1'].str.contains('h')),(data['T1'].str.contains('m')),(data['T1'].str.contains('s'))]

	    		# create a list of the values we want to assign for each condition
	    		values = [(data['T1'].str.extract('(\d+)').astype(float)), (data['T1'].str.extract('(\d+)').astype(float)), ((data['T1'].str.extract('(\d+)').astype(float)))]

	    		# create a new column and use np.select to assign values to it using our lists as arguments
	    		data['Activity_1']  = np.select(conditions, values)

	    		conditions = [(data['T1'].str.contains('h')),(data['T1'].str.contains('m')),(data['T1'].str.contains('s')) ]

	    		values = [data['Activity_1'] *3600, data['Activity_1']*60, data['Activity_1'] ]

	    		data['Activity_1']  = np.select(conditions, values)

	    		# create a list of our conditions
	    		conditions = [(data['T2'].str.contains('h')),(data['T2'].str.contains('m')),(data['T2'].str.contains('s'))]

	    		# create a list of the values we want to assign for each condition
	    		values = [(data['T2'].str.extract('(\d+)').astype(float)), (data['T2'].str.extract('(\d+)').astype(float)), ((data['T2'].str.extract('(\d+)').astype(float)))]

	    		# create a new column and use np.select to assign values to it using our lists as arguments
	    		data['Activity_2']  = np.select(conditions, values)

	    		conditions = [(data['T2'].str.contains('h')),(data['T2'].str.contains('m')),(data['T2'].str.contains('s'))]

	    		values = [data['Activity_2'] *3600, data['Activity_2']*60, data['Activity_2'] ]

	    		data['Activity_2']  = np.select(conditions, values)

	    		data['total_time_spent']=data['Activity_1']+data['Activity_2']
	    		#print(data.shape)
	    		final_df=data.groupby(['Reg No'],as_index = False).sum()
	    		#print(final_df.shape)
	    		final_df.drop(['Activity_1','Activity_2'],axis=1,inplace=True)
	    		#final_df.reset_index(inplace=True)
	    		#final_df.drop_duplicates(subset ="Reg No",keep ='first', inplace = True)
	    		final_df=final_df[final_df['total_time_spent']>time_val*60]
	    		#print(final_df.shape)

	    		present=final_df['Reg No']
	    		set_diff_df.append((pd.concat([reg_no_full, present, present]).drop_duplicates(keep=False)).to_string(index=False))
	    		val.append(str(data['Join Time'].iloc[0].date().day)+'-'+str(data['Join Time'].iloc[0].date().month)+'-'+str(data['Join Time'].iloc[0].date().year))
		new_val= pd.DataFrame(list(zip(val, set_diff_df)),columns =['date', 'absentees']) 
		#new_val.to_excel('/content/consolidated.xlsx',index=False)
		path_parent = os.path.dirname(os.getcwd())
		os.chdir(path_parent)
		os.chdir("/home/nm_dhanya/dhanya")
		#st.write("hello")
		#path_excel=os.getcwd()+'/consolidated.xlsx' 
		#new_val.to_excel(path_excel,index=False)


		#data = pd.read_excel(os.getcwd()+'/consolidated.xlsx')
		towrite = io.BytesIO()
		downloaded_file = new_val.to_excel(towrite, encoding='utf-8', index=False, header=True)
		towrite.seek(0)  # reset pointer
		b64 = base64.b64encode(towrite.read()).decode()  # some strings
		linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="consoliated.xlsx">Download excel file</a>'
		st.markdown(linko, unsafe_allow_html=True)
	
		print(os.getcwd())
		# Directory name 
		dir = 'attendance_'+str(x)    
		# Parent Directory 
		location = "."  
		# path
		path = os.path.join(location, dir)	  
		# removing directory
		shutil.rmtree(path,ignore_errors = False)	
 except KeyError:
 			print("")	

path = os.getcwd()
pattern = os.path.join(path, "attendance*")

for item in glob(pattern):
    if not os.path.isdir(item):
        continue
    shutil.rmtree(item)

	

