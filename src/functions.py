

# We create a function to collect data from the offices column(country code, address, lat&long...).

def get_info(lista, a, b):    
    append_data = []
    for i in range(len(lista)):
        try:           
            append_data.append(lista[i][0][b])             
        except:
            append_data.append("null")
    df[a]= append_data
    return








        