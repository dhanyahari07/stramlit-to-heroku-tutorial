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

@st.cache(suppress_st_warning=True)
def working_dir():
    return os.getcwd()


#os.chdir("..")
pwd_val=working_dir()
os.chdir(pwd_val)
#st.write(os.getcwd())
df = pd.DataFrame()
#path=''
#option=option_generator()

st.markdown("<h1 style='text-align: center; color: black;'>Department of Computer Science and Engineering</h1>", unsafe_allow_html=True)
st.markdown("<br><br>", unsafe_allow_html=True)

datafile = st.file_uploader("Upload namelist with Roll Number as the column title",type=['xlsx'])
if datafile is not None:
    file_details = {"FileName":datafile.name,"FileType":datafile.type}
    df  = pd.read_excel(datafile,engine="openpyxl")
    #st.dataframe(df)

val_namelist={'Roll Number':['CB.EN.U4CSE19001','CB.EN.U4CSE19002','CB.EN.U4CSE19003','CB.EN.U4CSE19004','CB.EN.U4CSE19005']}
new_val_namelist=pd.DataFrame.from_dict(val_namelist)
#new_val_namelist= pd.DataFrame(list(zip(val, df_namelist)),columns =['Sl No', 'Roll Number'])
path_parent = os.path.dirname(os.getcwd())
os.chdir(path_parent)
os.chdir(pwd_val)
towrite = io.BytesIO()
downloaded_file = new_val_namelist.to_excel(towrite, encoding='utf-8', index=False, header=True)
towrite.seek(0)  # reset pointer
b64 = base64.b64encode(towrite.read()).decode()  # some strings
linko= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="sample_namelist.xlsx">sample  namelist excel file</a>'
st.markdown(linko, unsafe_allow_html=True)


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
    #st.write(path)
    path_chdir='attendance_'+str(x)
    #path_chdir='attendance'
    #else:
    #       print("")
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
        directory=os.getcwd()
        for root,dirs,files in os.walk(directory):
            for file in files:
                #st.write(os.path.join(root, file))
                if file.endswith(".csv"):
                    #st.write(file)
                    with open(os.path.join(root, file), 'rb') as f:
                        result = chardet.detect(f.read())
                    data = pd.read_csv(os.path.join(root, file),encoding=result['encoding'],sep='\t',skiprows = 6)
                    data['Full Name']=data['Full Name'].str.upper()
                    data.sort_values("Full Name", inplace = True)
                    data.drop_duplicates(subset ="Full Name",keep ='first', inplace = True)
                    data['Reg No']=data['Full Name'].apply(lambda st: st[st.find("[")+1:st.find("]")])
                    data["Join Time"] = data["Join Time"].apply(pd.to_datetime)
                    present=data['Reg No']
                    set_diff_df.append((pd.concat([reg_no_full, present, present]).drop_duplicates(keep=False)).to_string(index=False))
                    #val.append(str(data['Join Time'].iloc[0].date().day)+'-'+str(data['Join Time'].iloc[0].date().month)+'-'+str(data['Join Time'].iloc[0].date().year))
                    val.append(data['Join Time'].iloc[0])
        new_val= pd.DataFrame(list(zip(val, set_diff_df)),columns =['date', 'absentees'])
        new_val['date']=pd.to_datetime(new_val['date'],format='%Y-%m-%d')
        new_val.sort_values(by=['date'],inplace=True)
        new_val['date']=new_val['date'].dt.strftime('%d/%m/%Y')


        path_parent = os.path.dirname(os.getcwd())
        os.chdir(path_parent)
        os.chdir(pwd_val)
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
        st.error("You have entered during class dump")
elif(option=='during class'):
    try:
        set_diff_df=[]
        val=[]
        #df= pandas.read_csv("file.csv",header= None)

        name_list=df
        #name_list= df.iloc[(df.loc[df[0]=='Full Name'].index[0]):, :].reset_index(drop = True)
        name_list['Roll Number']=name_list['Roll Number'].str.strip()
        name_list['Roll Number']=name_list['Roll Number'].str.upper()
        reg_no_full=name_list['Roll Number']
        #path='/content/attendance/'
        os.chdir(path_chdir)
        directory=os.getcwd()
        for root,dirs,files in os.walk(directory):
            for file in files:
                #for file in os.listdir():
                if file.endswith(".csv"):
                    print(file)
                    with open(os.path.join(root, file), 'rb') as f:
                        result = chardet.detect(f.read())
                    #print(file)
                    data = pd.read_csv(os.path.join(root, file),encoding=result['encoding'],sep='\t')
                    for i in range(10):
                        if(data.columns[0]!="Full Name"):
                            data = pd.read_csv(path+file,encoding=result['encoding'],sep='\t',skiprows=i)
                        else:
                            break
                    #data = pd.read_csv(path+file,encoding=result['encoding'],sep='\t')
                    #data=data.iloc[(df.loc[df[0]=='Full Name'].index[0]):, :].reset_index(drop = True)
                    data['Full Name']=data['Full Name'].str.upper()
                    data.sort_values("Full Name", inplace = True)
                    data.drop_duplicates(subset ="Full Name",keep ='first', inplace = True)
                    data['Reg No']=data['Full Name'].apply(lambda st: st[st.find("[")+1:st.find("]")])
                    data["Timestamp"] = data["Timestamp"].apply(pd.to_datetime)
                    present=data['Reg No']
                    set_diff_df.append((pd.concat([reg_no_full, present, present]).drop_duplicates(keep=False)).to_string(index=False))
                    #val.append(str(data['Timestamp'].iloc[0].date().day)+'-'+str(data['Timestamp'].iloc[0].date().month)+'-'+str(data['Timestamp'].iloc[0].date().year))
                    val.append(data['Timestamp'].iloc[0].date())


        new_val= pd.DataFrame(list(zip(val, set_diff_df)),columns =['date', 'absentees'])
        new_val['date']=pd.to_datetime(new_val['date'],format='%Y-%m-%d')
        new_val.sort_values(by=['date'],inplace=True)
        new_val['date']=new_val['date'].dt.strftime('%d/%m/%Y')



        path_parent = os.path.dirname(os.getcwd())

        os.chdir(path_parent)
        os.chdir(pwd_val)
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
        st.error("You have entered after class dump")
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
        directory=os.getcwd()
        for root,dirs,files in os.walk(directory):
            for file in files:
                #for file in os.listdir():
                if file.endswith(".csv"):
                    print(file)
                with open(os.path.join(root, file), 'rb') as f:
                    result = chardet.detect(f.read())
                data = pd.read_csv(os.path.join(root, file),encoding=result['encoding'],sep='\t',skiprows = 6)
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
                val.append(data['Join Time'].iloc[0])
        new_val= pd.DataFrame(list(zip(val, set_diff_df)),columns =['date', 'absentees'])
        new_val['date']=pd.to_datetime(new_val['date'],format='%Y-%m-%d')
        new_val.sort_values(by=['date'],inplace=True)
        new_val['date']=new_val['date'].dt.strftime('%d/%m/%Y')



        #path_parent = os.path.dirname(os.getcwd())
        os.chdir(path_parent)
        os.chdir(pwd_val)
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
        st.error("You have entered during class dump")

path = os.getcwd()
pattern = os.path.join(path, "attendance*")

for item in glob(pattern):
    if not os.path.isdir(item):
        continue
    shutil.rmtree(item)
st.markdown("<br><br>", unsafe_allow_html=True)
st.text("\n\n For any queries contant - Dhanya N.M.** nm_dhanya@cb.amrita.edu **")
