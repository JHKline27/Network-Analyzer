import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm

# Load your packet data
df = pd.read_csv('data/captured_packets.csv')

# Ensure 'timestamp' is in datetime format
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Calculate Inter-Arrival Time (in seconds)
df['inter_arrival_time'] = df['timestamp'].diff().dt.total_seconds().fillna(0)

# Descriptive statistics
print("Descriptive Statistics:")
print(df['packet_size'].describe())

# Correlation analysis
correlation = df['packet_size'].corr(df['inter_arrival_time'])
print(f"Correlation between packet size and inter-arrival time: {correlation}")

# t-Test example: Compare packet sizes for two protocols
protocol_a = df[df['protocol'] == 'TCP']['packet_size']
protocol_b = df[df['protocol'] == 'UDP']['packet_size']
t_stat, p_value = stats.ttest_ind(protocol_a, protocol_b)
print(f"t-Test: t-statistic = {t_stat}, p-value = {p_value}")

# Linear regression example
X = df['inter_arrival_time']
y = df['packet_size']
X = sm.add_constant(X)  # Adds a constant term to the predictor
model = sm.OLS(y, X).fit()
print(model.summary())

# 1. Total Traffic Analysis: Plot total packets over time
df.set_index('timestamp', inplace=True)
traffic_volume = df.resample('T').size()  # Resample to hourly
traffic_volume.plot(title='Total Traffic Volume Over Time', ylabel='Number of Packets')
plt.show()

# 2. Protocol Distribution
protocol_counts = df['protocol'].value_counts()
sns.barplot(x=protocol_counts.index, y=protocol_counts.values)
plt.title('Protocol Distribution')
plt.xlabel('Protocol')
plt.ylabel('Packet Count')
plt.show()

# 3. Inter-Arrival Time Analysis
sns.histplot(df['inter_arrival_time'], bins=50, kde=True)
plt.title('Histogram of Inter-Arrival Times')
plt.xlabel('Inter-Arrival Time (seconds)')
plt.ylabel('Frequency')
plt.show()

# 4. Top Talkers Analysis
top_talkers = df['src_ip'].value_counts().head(10)
sns.barplot(x=top_talkers.index, y=top_talkers.values)
plt.title('Top Talkers by Packet Count')
plt.xlabel('Source IP')
plt.ylabel('Packet Count')
plt.xticks(rotation=45)
plt.show()
