import pandas as pd
from column_type_detective import conversion_score
from colorama import init, Fore, Back, Style

init(autoreset=True)

def run_quality_report(df):  

        #WE MODIFIED quality_report.py TO CALCULATE INSIGHTS FOR ALL NUMERIC VALUES
    rows,columns=df.shape
    bad_cols_name=[] #will contain name and % of colums with > 5% missing values

    outliers_number_with_cols=[] #will contain number of outlierss in each column of outliers(> 3 std dev)
    invalid_emails=0 #number of invalid emails

    print(f"{Fore.MAGENTA}Rows: {rows} | Columns: {columns}")
    print(f"{Fore.GREEN}📊 Columns summary")

    for col in df.columns:   #getting columns name
        actual_size=df[col].size #actual size of current column
        true_size=df[col].count() #size of current col excluding NANs only including actual values

        completion_per= (true_size/actual_size) * 100 #completion percentage in columns = true_size(excluding nan)/actual_size(inclusing nan) * 100
        if(completion_per<95):
            bad_cols_name.append((col,completion_per))

        if col == 'email': 
            df['email']=df['email'].fillna('')  #defaulting nan or empty values
            for e in df['email']:
                idx_at=e.find('@')
                #checking condition: if email is empty, it contains space, no @, or not dot after @ 
                if e == '' or idx_at==-1 or ' ' in e or '.' not in e[idx_at+1:]:
                    invalid_emails+=1

        unique_vals=df[col].unique().size
        print(f"- {col}: {completion_per:.2f}% complete, {unique_vals} unique values")

    print(f"\n{Fore.YELLOW}⚠️ OVERALL ISSUES FOUND:{Style.RESET_ALL}")
    print(f"- {len(bad_cols_name)} with >5% missing data")
    for i in range(len(bad_cols_name)):
        c=bad_cols_name[i]
        print(f"{c[0]} -> {c[1]}%")

    '''Step 1: df.duplicated()

    Scans every row vs every other row

    Returns boolean Series: True if row is duplicate of any previous row

    First occurrence = False, later copies = True

    Compares ALL columns by default (order_id + customer_id + dates + everything)

    Step 2: .sum()

    Counts True values = total duplicate rows'''       
    duplicate_rows=df.duplicated().sum()  #it gives number of duplicated rows in dataset
    print(f"- {duplicate_rows} duplicate rows detected")
    print(f"- {invalid_emails} invalid emails format")


    print(f"\n{Fore.YELLOW}📈 INSIGHTS FOR EACH NUMERIC COLUMN")

    numeric_dtypes=[]
    for col in df.columns:
        dictt,dtype=conversion_score(df[col]) #running through to get datatypes that are numeric
        if dtype[0]=='numerical':    
            numeric_dtypes.append(col)

    if len(numeric_dtypes)==0:  #no numeric datatypes
        print("There are no numerical datatypes")
    
    else:
        print(numeric_dtypes)
        for col in numeric_dtypes: #iterating over all numeric columns to get insights
            print(f"{Fore.RED}> {col}")
            conv=df[col].astype(str).str.strip()
            conv_clean=conv.str.replace(r'[$€£,]','',regex=True)  #replacing currency sight with empty strings so amounts counted as numeric
            conv_num=pd.to_numeric(conv_clean,errors='coerce')

            print(f"MAX VALUE: {max(conv_num)}")
            print(f"MIN VALUE: {min(conv_num)}")
            m=conv_num.mean()
            std_dev=conv_num.std()
            outlier_threshold=3*std_dev 
            total_outliers=0
            for value in conv_num:
                if abs(value-m) > outlier_threshold: #here we use outlier formula studied in prac stats
                    total_outliers+=1
            print(f"TOTAL OUTLIERS(>3*std_dev): {total_outliers}")

            

if __name__=='__main__':
    while True:
        try:
            filename=input("Enter filename: ")
            dot_idx=filename.find(".")   #finding index od . in filename
            ext=filename[dot_idx+1:].lower()
            if ext=='csv':  #for csv
                df=pd.read_csv(filename)
                break
            elif ext=='xlsx':  #for excel
                df=pd.read_excel(filename)
                break
            elif ext=='json':
                df=pd.read_json(filename)
                break
            else:
                print("Only csv, xlsx and json files supported.")
        except FileNotFoundError:
            print("File not founded!")

    run_quality_report(df)