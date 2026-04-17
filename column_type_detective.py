import pandas as pd
from colorama import init,Fore

def conversion_score(col):
    score={}
    total_not_nan_values=col.count()
    if total_not_nan_values==0: #if no non-nulll value exists
        return {"EMPTY": 1}

    #for boolean
    c1=col.astype(str).str.strip().str.lower()
    allowed=['yes','no','true','false','y','n','t','f','0','1']
    s1=(c1.isin(allowed).sum() / total_not_nan_values) 
    score['bool']=s1
    
    #for date time
    c2=col.astype(str).str.strip()
    date_regexs=[r'^\d{1,2}[-/]\d{1,2}[-/]\d{4}$',
                r'^\d{4}[-/]\d{1,2}[-/]\d{1,2}$',
                r'^\d{2}/\d{2}/\d{4} \d{1,2}:\d{2}:\d{2} (AM|PM)$']
    
    best=0.0
    for date_regex in date_regexs:
        s2=(c2.str.match(date_regex,na=False).sum()/ total_not_nan_values) 
        if s2>best:
            best=s2
    score['datetime']=best
        

    #for phone numbers
    c3=col.astype(str).str.strip()
    c3_clean= c3.str.replace(r'[^\d]', '', regex=True)  #phonenumbers might contain hyphens in between
    s3= c3_clean.str.match(r'^[0-9]{7,15}$',na=False).sum() / total_not_nan_values
    score['phone']=s3

    #for emails
    c4=col.astype(str).str.strip()
    email_regex= r'^[^@\s]+@[^@\s]+\.[^@\s]+$'
    '''^ and $ mean “start” and “end” of the string.

    [^@\s]+ = one or more characters that are not @ or whitespace.

    @ = literal at symbol.

    \. = literal dot
    '''
    total_emails_match=c4.str.match(email_regex,na=False).sum() #na=False: treat NaN as *False* (not a match), not as NaN
    s4=(total_emails_match / total_not_nan_values)
    score['email']=s4

    #for ids
    c5=col.astype(str).str.strip()
    unique_ratio=c5.nunique() / total_not_nan_values #if unique ratio ==1 then most probaly it is ids
    if unique_ratio==1:
        score['ID']=1
    else:
        contains_only_chars_nums=c5.str.match(r'^[a-zA-Z0-9]+$',na=False).sum() / total_not_nan_values #contains only alphanumeric also false on spaces bcs only alphanumeric allowed
        s5=(0.9*unique_ratio) + (0 * contains_only_chars_nums)
        score['ID']=s5


    #for numeric
    c6=col.astype(str).str.strip()
    c6_clean=c6.str.replace(r'[$€£,% ]','',regex=True)  #replacing currency sight with empty strings so amounts counted as numeric
    c6_num=pd.to_numeric(c6_clean,errors='coerce')
    total_converted=c6_num.count()   #total non nan values
    s6=(total_converted / total_not_nan_values) 
    score['numerical']=s6


    #for free text
    c7=col.astype(str).str.strip()
    unique_ratio=c7.nunique() / total_not_nan_values
    avg_len=c7.str.len().sum() / total_not_nan_values
    has_punctuations_ratio=c7.str.contains(r'[,\-\.;!? ]',na=False).sum() / total_not_nan_values
    if unique_ratio<=0.2:
        unique_score=0.0
    elif unique_ratio>=0.4:
        unique_score=1.0
    else:
        unique_score=(unique_ratio-0.2) / (0.4-0.2)

    if avg_len<=5:
        len_score=0.0
    elif avg_len>=10:
        len_score=1.0
    else:
        len_score=(avg_len-20) / (30-20)

    if has_punctuations_ratio<=0.2:
        punc_score=0.0
    elif has_punctuations_ratio>=0.5:
        punc_score=1.0
    else:
        punc_score=(has_punctuations_ratio-0.2) / (0.5-0.2)

    s7= (0.4*unique_score) + (0.3 * len_score) + (0.3 * punc_score)
    score['text']=s7

    #for categorial
    c8=col.astype(str).str.strip()
    unique_ratio=c8.nunique() / total_not_nan_values
    avg_len=c8.str.len().sum() / total_not_nan_values

    #it is just a madeup formula
    if unique_ratio<=0.1: #very less unique ratio
        unique_score=1.0
    elif unique_ratio>=0.3: #medium to higher unique ratio
        unique_score=0.0
    else:
        unique_score=(0.3-unique_ratio) / (0.3-0.1)

    if avg_len<=20:  #if avg_len<15 it probably be categorial, single,male,female,outstanding kinds
        len_score=1.0
    elif avg_len>25:  #if it exceeds 20 chars then it is free text description
        len_score=0.0
    else:
        len_score=(25-avg_len) / (25-20.0)
    
    s8=0.6 * unique_score + 0.4 * len_score
    score['categorical']=s8


    #for url
    c9=col.astype(str).str.strip()
    url_regex=r'^https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&/=]*)$'
    s9=c9.str.match(url_regex,na=False).sum() / total_not_nan_values
    score['URL']=s9

    highest=max(score.items(),key=lambda x:x[1])
    return score,highest


if __name__=="__main__":
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
        
        


    









