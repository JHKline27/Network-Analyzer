import pandas as pd

def apply_filters(df, filter_params):
    if df.empty:
        print("DataFrame is empty, no packets to filter.")
        return df

    filtered_df = df.copy()

    if filter_params['source_ip']:
        filtered_df = filtered_df[filtered_df["Source IP"].str.contains(filter_params['source_ip'], na=False)]
        

    if filter_params['destination_ip']:
        filtered_df = filtered_df[filtered_df["Destination IP"].str.contains(filter_params['destination_ip'], na=False)]
        

    if filter_params['protocol_options']:
        filtered_df = filtered_df[filtered_df["Protocol"].str.lower().isin([p.lower() for p in filter_params['protocol_options']])]
        

    if filter_params['source_port']:
        filtered_df = filtered_df[filtered_df["Source Port"] == filter_params['source_port']]
        

    if filter_params['destination_port']:
        filtered_df = filtered_df[filtered_df["Destination Port"] == filter_params['destination_port']]
        

   

    filtered_df["Packet Size"] = pd.to_numeric(filtered_df["Packet Size"], errors='coerce')
    filtered_df = filtered_df.dropna(subset=["Packet Size"])

    
    packet_size = filter_params['packet_size']
    size_comparison = filter_params['size_comparison']
    if packet_size is not None and packet_size > 0 and size_comparison:
        
        
        if size_comparison == "Greater Than":
            filtered_df = filtered_df[filtered_df["Packet Size"] > packet_size]
            
        elif size_comparison == "Less Than":
            filtered_df = filtered_df[filtered_df["Packet Size"] < packet_size]
            
        elif size_comparison == "Equal To":
            filtered_df = filtered_df[filtered_df["Packet Size"] == packet_size]

    return filtered_df
