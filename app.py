import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import warnings

# Suppress warnings
warnings.filterwarnings('ignore', category=FutureWarning)

# Streamlit App Title
st.title("SME Financial Insights Dashboard")

# Upload Dataset
uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    
    # Check required columns before renaming and mapping
    required_columns = ['Type_SME', 'Established_year', 'Sector', 'SME_Size']
    if not all(col in data.columns for col in required_columns):
        st.error("Uploaded CSV is missing required columns. Please check the file format.")
    else:
        # Data Cleaning & Mapping
        data.rename(columns={'Type_SME': 'SME_Type', 'Established_year': 'Established_Year'}, inplace=True)
        
        est_year_mapping = {1: 'Within 5 years', 2: '5-10 years', 3: 'More than 10 years'}
        sme_type_mapping = {1: 'Micro', 2: 'Small', 3: 'Medium', 4: 'Large'}
        sector_mapping = {1: 'Healthcare', 2: 'Technology', 3: 'Services', 4: 'Agriculture', 5: 'Construction'}
        sme_size_mapping = {1: '1-9', 2: '10-49', 3: '50-249', 4: '250-999', 5: '1000+'}
        
        data['Established_Year'] = data['Established_Year'].map(est_year_mapping)
        data['SME_Type'] = data['SME_Type'].map(sme_type_mapping)
        data['Sector'] = data['Sector'].map(sector_mapping)
        data['SME_Size'] = data['SME_Size'].map(sme_size_mapping)
        
        st.write("### Data Overview")
        st.dataframe(data.head())
        
        # Data Visualization
        st.write("### Distribution of SME Types")
        fig, ax = plt.subplots()
        data['SME_Type'].value_counts().plot(kind='bar', color='skyblue', ax=ax)
        ax.set_title("SME Type Distribution")
        ax.set_xlabel("SME Type")
        ax.set_ylabel("Count")
        st.pyplot(fig)
        
        # Correlation Heatmap
        financial_metrics = [col for col in data.columns if any(prefix in col for prefix in ['FL', 'FR', 'RA', 'MDA', 'FDM', 'FA'])]
        if financial_metrics:
            correlation_matrix = data[financial_metrics].corr()
            st.write("### Correlation Between Financial Metrics")
            fig, ax = plt.subplots(figsize=(12, 8))
            sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5, ax=ax)
            st.pyplot(fig)
        else:
            st.warning("No financial metric columns found in the dataset.")
        
        # Financial Metric Selection
        if financial_metrics:
            selected_metric = st.selectbox("Select Financial Metric", financial_metrics)
            
            # Box Plot: Sector-Specific Financial Profiles
            st.write("### Sector-Specific Financial Profiles")
            fig, ax = plt.subplots()
            sns.boxplot(x='Sector', y=selected_metric, data=data, palette='Set1', ax=ax)
            ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
            st.pyplot(fig)
            
            # Box Plot: SME Size Impact on Financial Metrics
            st.write("### Impact of SME Size on Financial Metrics")
            fig, ax = plt.subplots()
            sns.boxplot(x='SME_Size', y=selected_metric, data=data, palette='Set2', ax=ax)
            ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
            st.pyplot(fig)
            
            # Box Plot: Financial Health by SME Type
            st.write("### Financial Health by SME Type")
            fig, ax = plt.subplots()
            sns.boxplot(x='SME_Type', y=selected_metric, data=data, palette='Set3', ax=ax)
            ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
            st.pyplot(fig)
        
        st.write("Upload your SME financial data to explore insights!")
