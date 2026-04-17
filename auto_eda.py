#Automated Data Cleaning & Analysis Tool

import pandas as pd
from itertools import combinations
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from column_type_detective import conversion_score
import seaborn as sns
import plotly.express as px  # only if interactive
from colorama import Fore,init
import os
init(autoreset=True)


def plot_numeric(col_name,col,output_folder,filename):
   valid_vals=col.dropna()

   #this is for if we want boxplot and histogram fro each column of seperate pages
   '''sns.histplot(x=valid_vals,bins=10)
    plt.show()
    sns.boxplot(y=valid_vals)  #y to put values along y axis can use x to put value along x axiss
    plt.show()'''
   
   #thiss makes histogram and boxplot for a column in one page
   fig, axes = plt.subplots(nrows=2, ncols=1,figsize=(8,15))
   sns.boxplot(y=valid_vals,ax=axes[0])
   sns.histplot(y=valid_vals,bins=10,ax=axes[1])
    
   axes[0].set_title(f"Boxplot and Histogram of {col_name}")
   plt.tight_layout()
    
   #saving
   file = f"{filename}_{col_name}_numericSummary.png"
   path=os.path.join(output_folder,file)
   print(f"Saving to {path}")
   plt.savefig(path)
   plt.close()

  
   
def plot_categorial(col_name,col,output_folder,filename):
    valid_vals=col.dropna()
    #if many categories then we take only top 20
    top_20_cat=valid_vals.value_counts().head(20) #value_counts sort in descending order acc to number of times each category occurs

    sns.barplot(x=top_20_cat.values,y=top_20_cat.index).set_title(f"Bargraph of {col_name}")

    plt.tight_layout()

    #saving
    file = f"{filename}_{col_name}_categorialSummary.png"
    path=os.path.join(output_folder,file)
    print(f"Saving to {path}")
    plt.savefig(path)
    plt.close()



def plot_DateTime(col_name,col,output_folder,filename):
    valid_vals=col.dropna()
    dates=valid_vals.value_counts().sort_index()
    plt.figure(figsize=(12, 4))
    ax=sns.lineplot(x=dates.index,y=dates.values)
    ax.set_title(f"Lineplot of {col_name}")
    ax.xaxis.set_major_locator(MaxNLocator(nbins=12))    #it just decreases dates number on x axis so we get long ranges
    plt.tight_layout()
     #saving
    file = f"{filename}_{col_name}_DateTimeSummary.png"
    path=os.path.join(output_folder,file)
    print(f"Saving to {path}")
    plt.savefig(path)
    plt.close()


def plot_correlation(num_cols,output_folder,filename):
    cor_mat=num_cols.corr()    #correlation matrix
    plt.figure(figsize=(10,8))
    ax=sns.heatmap(cor_mat,annot=True,cmap="coolwarm",square=True,cbar_kws={"shrink":0.8})

    ax.set_title("Correlation heatmap")
    plt.tight_layout()

    file=f"{filename}_Correlation_heatmap.png"
    path=os.path.join(output_folder,file)
    print(f"Saving to {path}")
    plt.savefig(path)
    plt.close()


def pairwise_pearson(df_numeric_cols,output_folder):
    pair_coeff=[]
    cols=df_numeric_cols.columns

    for c1,c2 in combinations(cols,2):
        r=df_numeric_cols[c1].corr(df_numeric_cols[c2],method="pearson")
        pair_coeff.append({"col1": c1, "col2": c2, "pearson_Constant": r})
    
    print(f"{Fore.CYAN}{pd.DataFrame(pair_coeff)}")


def graphs(filename,df):

    numeric_cols=[]
    output_folder_graphs=input("Enter output folder for graphs: ")
    df_copy=df.copy() #copying original dataset
    for col in df.columns:
        d_type_dict,d_type=conversion_score(df[col])
        
        if d_type[0]=='numerical':
            df_copy[col]=df[col].astype(str).str.strip().str.replace(r'[$€£,% ]','',regex=True)  #cleaning data (removing currency and comma )
            df_copy[col]=pd.to_numeric(df_copy[col],errors='coerce')  #as heatmap and coeefiecient automatically converts data to numeric but as our data contain garbage values that can crash the program so we manually do it with errors='coerce
            numeric_cols.append(col)

            print("Plotting", col)  
            plot_numeric(col,df_copy[col],output_folder_graphs,filename)
        
        elif d_type[0]=='categorical':
            print("Plotting", col)
            plot_categorial(col,df[col],output_folder_graphs,filename)
        
        elif d_type[0]=='datetime':
            print("Plotting", col)
            plot_DateTime(col,df[col],output_folder_graphs,filename)
    
    if len(numeric_cols)>=2:
        print("\nPlotting correlation heatmap for:", numeric_cols)
        
        output_folder_correlation=input("Enter output folder for correlation: ")
        plot_correlation(df_copy[numeric_cols],output_folder_correlation,filename) #for heatmap
        print(f"{Fore.LIGHTRED_EX}PEARSON COEFFICIENT: ")
        pairwise_pearson(df_copy[numeric_cols],output_folder_correlation) #for pearson correlation
    else:
        print("There are not enough numerical columns to get correlations")



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

    graphs(filename,df)
    