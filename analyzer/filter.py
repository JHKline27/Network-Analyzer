import pandas as pd

def apply_filters(df, filter_params):
    if df.empty:
        print("DataFrame is empty, no packets to filter.")
        return df

    filtered_df = df.copy()
    
    # Debugging output
    print("Original DataFrame:")
    print(filtered_df)

    # Apply filters based on provided parameters
    if filter_params['source_ip']:
        filtered_df = filtered_df[filtered_df["Source IP"].str.contains(filter_params['source_ip'], na=False)]
        print(f"After Source IP filter ({filter_params['source_ip']}):")
        print(filtered_df)

    if filter_params['destination_ip']:
        filtered_df = filtered_df[filtered_df["Destination IP"].str.contains(filter_params['destination_ip'], na=False)]
        print(f"After Destination IP filter ({filter_params['destination_ip']}):")
        print(filtered_df)

    if filter_params['protocol_options']:
        filtered_df = filtered_df[filtered_df["Protocol"].str.lower().isin([p.lower() for p in filter_params['protocol_options']])]
        print(f"After Protocol filter ({filter_params['protocol_options']}):")
        print(filtered_df)

    if filter_params['source_port']:
        filtered_df = filtered_df[filtered_df["Source Port"] == filter_params['source_port']]
        print(f"After Source Port filter ({filter_params['source_port']}):")
        print(filtered_df)

    if filter_params['destination_port']:
        filtered_df = filtered_df[filtered_df["Destination Port"] == filter_params['destination_port']]
        print(f"After Destination Port filter ({filter_params['destination_port']}):")
        print(filtered_df)

    packet_size = filter_params['packet_size']
    size_comparison = filter_params['size_comparison']  # New parameter for comparison

    if size_comparison == "Greater Than":
        filtered_df = filtered_df[filtered_df["Packet Size"] > packet_size]
    elif size_comparison == "Less Than":
        filtered_df = filtered_df[filtered_df["Packet Size"] < packet_size]
    elif size_comparison == "Equal To":
        filtered_df = filtered_df[filtered_df["Packet Size"] == packet_size]

    return filtered_df
