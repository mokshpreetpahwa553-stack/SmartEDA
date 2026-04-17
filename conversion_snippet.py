from column_type_detective import conversion_score
import pandas as pd
from colorama import init,Fore

init(autoreset=True)
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


#functions to return snippets for conversions:
#is dataframe name and col is column name

#to numeric
def to_numerical(col_name):
    return f'df["{col_name}"] = pd.to_numeric(df["{col_name}"],errors="coerce")'

#to datetime
def to_datetime(col_name):
    return f'df["{col_name}"] = pd.to_datetime(df["{col_name}"],errors="coerce")'

#to categorial
def to_categorical(col_name):
    return f'df["{col_name}"] = df["{col_name}"].astype("category")'

#to text(str)
def to_text(col_name):
    return f'df["{col_name}"] = df["{col_name}"].astype("str")'


#to bool
def to_bool(col_name):
    return f'df["{col_name}"] = df["{col_name}"].astype("bool")'


func_map={
    "numerical": to_numerical,
    "categorical": to_categorical,
    "datetime": to_datetime,
    "text": to_text,
    "bool": to_bool
}
#pandas dtypes identification
#for numeric
pandas_numeric=["int64", "int32", "int16", "int8", "uint64", "uint32", "uint16", "uint8", "float64","float32"]

#for boolean
pandas_bool=["bool","boolean"]

#for datetime
pandas_datetime=["datetime64[ns]","datetime64[ns, tz]","datetime64[ns, UTC]","datetime64[us]"]

#for text(str)
pandas_text=["str","object"]

#for categorical
pandas_category=["category"]

def conv_snip(df): #df is dataframe
    for col in df.columns:
        score,high=conversion_score(df[col])
        print(f"\n{Fore.MAGENTA}{col}:")
        print(f"{Fore.YELLOW}Detected dtype: {Fore.LIGHTBLUE_EX}{high[0]}")
        pandas_dtype=str(df[col].dtype).lower()
        print(f"{Fore.YELLOW}Pandas dtype: {Fore.LIGHTBLUE_EX}{pandas_dtype}")

        conv_dtype=conversion_type[high[0]]

        #for numerical dtypes
        if conv_dtype=='numerical':
            if pandas_dtype in pandas_numeric:
                print(f"{Fore.GREEN}No conversion needed")
            else:
                print(f"{col}={col}.str.replace(r'[$€£,% ]','',regex=True) #removing currency symbols, commas and other  signs")
                print(f"{Fore.LIGHTRED_EX}Convert using: {func_map[conv_dtype](col)}")

        #for categorical dtype
        elif conv_dtype=='categorical':
            if pandas_dtype in pandas_category:
                print(f"{Fore.GREEN}No conversion needed")
            else:
                print(f"{Fore.LIGHTRED_EX}Convert using: {func_map[conv_dtype](col)}")
        
        #for datetime dtype
        elif conv_dtype=='datetime':
            if pandas_dtype in pandas_datetime:
                print(f"{Fore.GREEN}No conversion needed")
            else:
                print(f"{Fore.LIGHTRED_EX}Convert using: {func_map[conv_dtype](col)}")
        
        #for boolean dtype
        elif conv_dtype=='bool':
            if pandas_dtype in pandas_bool:
                print(f"{Fore.GREEN}No conversion needed")
            else:
                print(f"{Fore.LIGHTRED_EX}Convert using: {func_map[conv_dtype](col)}")

        #for text(str) dtype
        elif conv_dtype=='text':
            if pandas_dtype in pandas_text:
                print(f"{Fore.GREEN}No conversion needed")
            else:
                print(f"{Fore.LIGHTRED_EX}Convert using: {func_map[conv_dtype](col)}")
        

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

    conv_snip(df)
    
   
