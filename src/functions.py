
# We create a function to collect data from the offices column(country code, address, lat&long...).

def get_info(lista, df_, a, b):    
    append_data = []
    for i in range(len(lista)):
        try:           
            append_data.append(lista[i][0][b])             
        except:
            append_data.append("null")
    df_[a]= append_data
    return


# Dropping unnecesary columns

def drop_column(datfr, column):
    datfr = datfr.drop([column], axis = 1, inplace= True)
    return

# We delete some of the rows with missing data (the ones with more than one missing value)

def drop_nan(dfr):
    dfr.dropna(axis=0, inplace=True, thresh=7)
    dfr.reset_index(drop=True, inplace=True)
    return

# Mapping the values of City column to get to value_counts

def value_counts(df_,newcolumn, counting):
    df_[newcolumn] = df_[counting].map(df_[counting].value_counts())
    return

# Keeping only the columns with certain values

def keep_value(dfra, column, value):
    dfra = dfra[(dfra[column] > value)]
    dfra.reset_index(drop=True, inplace=True)
    return dfra




        