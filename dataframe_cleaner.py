from column_type_detective import conversion_score
import pandas as pd

#dictionary for conversion type as my code identify 8 dataypes
#so we map each to 5 major data types
conversion_type={
    "bool": "bool",
    "datetime": "datetime",
    "phone": "categorical",
    "email": "categorical",
    "ID": "categorical",
    "numerical": "numerical",
    "text": "text", #str
    "categorical": "categorical",
    }

#now codes for real time conversions to make clean dataset
#we will pass copy of real dataset in this so our original dataset dont get modified
def to_numerical_conv(df,col):
    df[col]=df[col].astype(str)
    df[col]=df[col].str.replace(r'[$€£,% ]','',regex=True )
    df[col]=pd.to_numeric(df[col],errors='coerce')

def to_datetime_conv(df,col):
    df[col]=pd.to_datetime(df[col],errors='coerce')

def to_categorical_conv(df,col):
    df[col]=df[col].astype(str)
    df[col]=df[col].astype("category")

def to_text_conv(df,col):
    df[col]=df[col].astype(str)

def to_bool_conv(df,col):
    df[col]=df[col].astype(str)
    df[col]=df[col].astype("bool")

#this maps to converti column in datatypes to make it clean
conversion={
    'numerical': to_numerical_conv,
    'categorical': to_categorical_conv,
    'datetime': to_datetime_conv,
    'text': to_text_conv,
    'bool': to_bool_conv
}

#pandas dtypes identification
#for numeric
pandas_numeric=["int64", "int32", "int16", "int8", "uint64", "uint32", "uint16", "uint8", "float64","float32"]

#for boolean
pandas_bool=["bool","boolean"]

#for datetime
pandas_datetime=["datetime64[ns]","datetime64[ns, tz]","datetime64[ns, UTC]"]

#for text(str)
pandas_text=["str","object"]

#for categorical
pandas_category=["category"]

def clean_dataframe(df): #df is dataframe
    df_copy=df.copy() #making copy of original dataset
    df_copy=df_copy.dropna() #dropping rows with nan values(even with 1), to make dataset more real and cleaner

    for col in df.columns:
        score,high=conversion_score(df[col])
        pandas_dtype=str(df[col].dtype).lower()
        
        conv_dtype=conversion_type[high[0]]

        #for numerical dtypes
        if conv_dtype=='numerical':
            if pandas_dtype not in pandas_numeric:
                conversion[conv_dtype](df_copy,col)                

        #for categorical dtype
        elif conv_dtype=='categorical':
            if pandas_dtype not in pandas_category:
               conversion[conv_dtype](df_copy,col)
                   

        #for datetime dtype
        elif conv_dtype=='datetime':
            if pandas_dtype not in pandas_datetime:
                conversion[conv_dtype](df_copy,col) 

        #for boolean dtype
        elif conv_dtype=='bool':
            if pandas_dtype not in pandas_bool:
                conversion[conv_dtype](df_copy,col) 

        #for text(str) dtype
        elif conv_dtype=='text':
            if pandas_dtype not in pandas_text:
               conversion[conv_dtype](df_copy,col) 

    return df_copy #returns cleaned copt=y of dataframe    
        

#--------MAIN-----------
if __name__ =='__main__':
    while True:
        try:
            filename=input("Enter filename: ")
            dot_idx=filename.find(".")   #finding index od . in filename
            if filename[dot_idx+1:]=='csv':  #for csv
                df=pd.read_csv(filename)
                break
            elif filename[dot_idx+1:]=='xlsx':  #for excel
                df=pd.read_excel(filename)
                break
            elif filename[dot_idx+1:]=='json':
                df=pd.read_json(filename)
                break
            else:
                print("Only csv, xlsx and json files supported.")
        except FileNotFoundError:
            print("File not founded!")

    clean=clean_dataframe(df)
    print(clean['unit_price'])
     

    
   
