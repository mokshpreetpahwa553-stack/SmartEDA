import pandas as pd
from column_type_detective import conversion_score
from conversion_snippet import conv_snip
from data_profiler import run_quality_report
from dataframe_cleaner import clean_dataframe
from auto_eda import graphs
from colorama import init,Fore
import os

#MAIN FILE
while True:
    try:
        filename=input("Enter filename: ")
        dot_idx=filename.find(".")   #finding index od . in filename
        ext=filename[dot_idx:]
        if ext=='.csv':  #for csv
            df=pd.read_csv(filename,nrows=1000000)
            break
        elif ext=='.xlsx':  #for excel
            df=pd.read_excel(filename)
            break
        elif ext=='.json':
            df=pd.read_json(filename)
            break
        else:
            print("Only csv, xlsx and json files supported.")
    except FileNotFoundError:
        print("File not founded!")

while True:
    print("\nMENU:\n" 
          "1. Get quality report\n"
          "2. Get columns dataTypes\n"
          "3. Get code snippets to convert columns in correct dataTypes\n"
          "4. Clean dataframe(Remove NaNs and convert columns to their correct datatype)\n"
          "5. Get graphs and correlation heatmap\n"
          "6. QUIT")
    
    opt=input("Enter option: ")

    if opt=='1':
        run_quality_report(df)      

    elif opt=='2':
        init(autoreset=True)
        print(f"{Fore.LIGHTBLUE_EX}#{filename}")
        print(f"\n{Fore.MAGENTA}Total Columns: {df.shape[1]}")
        print(f"\n{Fore.GREEN} COLUMN ANALYSIS:")
        print("________________________________________________________\n")
        for col in df.columns:
            score_dict,highest_dtype=conversion_score(df[col])
            if (highest_dtype[1] * 100) < 70:
                print(f"{Fore.CYAN}{col} : {Fore.WHITE}Cannot evidently detect datatype")
                print(f"{col} -> {score_dict}")
            else:
                print(f"{Fore.CYAN}{col} : {Fore.YELLOW}{highest_dtype[0]} ({highest_dtype[1] * 100:.2f}% confidence)") 
            print(f"{Fore.LIGHTRED_EX}SAMPLE: {Fore.WHITE}{list(df[col].dropna().head(3))}\n")   #dropna will filter all non-null values and head(3) will show first 3 values as samples'''
        
    elif opt=='3':
        conv_snip(df)
    
    elif opt=='4':
        clean_df=clean_dataframe(df)
        choice=input("Press 'o' to show cleaned database here or 's' to save in same extension as input file: ").lower()

        if choice=='o':
            print(clean_df)
        else:  # to save cleaned dataframe
            output_folder=input("Enter output folder name: ")  
            output_filename=input("Enter output file name: ")

            if not output_filename:
                output_filename=f"clean_{filename}"
            
            valid_extensions= ['.csv','.xlsx','.json']
            while True:
                extension=input("Enter extension of dataset: ")
                if not extension:
                    extension=ext
                    break

                elif extension not in valid_extensions:
                    print("Only .csv, .xlsx, .json files supproted")

                else:
                    break
            
            output_path = os.path.join(output_folder, f"{output_filename}{extension}")

            if extension=='.csv':
                clean_df.to_csv(output_path,index=False)
                print(f"{filename}{extension} saved to {output_folder}")
            elif extension=='.xlsx':
                clean_df.to_excel(output_path,index=False)
                print(f"{filename}{extension} saved to {output_folder}")
            elif extension=='.json':
                clean_df.to_json(output_path,index=False)
                print(f"{filename}{extension} saved to {output_folder}")
            else:
                print("Something went wrong! Try again")


    elif opt=='5':
        graphs(filename,df)
    
    elif opt=='6':
        print("Goodbyeee👋")
        break

    else:
        print("Enter options(1-6)")
    