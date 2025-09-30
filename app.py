"""
ROOTS - Farm Accounting Software
Complete Streamlit Application
Author: Created for Farm Management
Version: 1.0
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import io

# ====================
# PAGE CONFIGURATION
# ====================
st.set_page_config(
    page_title="ROOTS - Farm Accounting",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ====================
# CUSTOM CSS STYLING
# ====================
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        color: #2e7d32;
        text-align: center;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #558b2f;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
    }
    .metric-card {
        background-color: #f1f8e9;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #2e7d32;
    }
    .profit {
        color: #2e7d32;
        font-weight: bold;
    }
    .loss {
        color: #c62828;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# ====================
# SESSION STATE INITIALIZATION
# ====================
if 'excel_file' not in st.session_state:
    st.session_state.excel_file = None

# ====================
# FUNCTION: CREATE SAMPLE EXCEL
# ====================
def create_sample_excel():
    """Create a sample Excel file with all the required sheets and sample data"""
    output = io.BytesIO()
    
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # SHEET 1: MASTER_Farm_Profile
        df_farm = pd.DataFrame({
            'Farm_ID': ['F001'],
            'Farmer_Name': ['Sample Farmer'],
            'Location': ['Agra, UP'],
            'Total_Area_Acres': [12],
            'Soil_Type': ['Loamy'],
            'Irrigation_Source': ['Tubewell'],
            'Contact': ['9876543210'],
            'Bank_Account': ['XXXX1234']
        })
        df_farm.to_excel(writer, sheet_name='MASTER_Farm_Profile', index=False)
        
        # SHEET 2: MASTER_Season
        df_season = pd.DataFrame({
            'Season_ID': ['S001', 'S002', 'S003'],
            'Season_Name': ['Rabi', 'Kharif', 'Zaid'],
            'Start_Month': ['October', 'June', 'March'],
            'End_Month': ['March', 'September', 'June']
        })
        df_season.to_excel(writer, sheet_name='MASTER_Season', index=False)
        
        # SHEET 3: MASTER_Crops
        df_crops = pd.DataFrame({
            'Crop_ID': ['C001', 'C002', 'C003', 'C004', 'C005', 'C006', 'C007', 'C008', 'C009', 'C010'],
            'Crop_Name': ['Wheat', 'Rice', 'Maize', 'Gram', 'Moong', 'Mustard', 'Sunflower', 'Berseem', 'Potato', 'Onion'],
            'Category': ['Cereals', 'Cereals', 'Cereals', 'Pulses', 'Pulses', 'Oilseeds', 'Oilseeds', 'Fodder', 'Major Veg', 'Major Veg'],
            'Sub_Category': ['Bread Wheat', 'Basmati', 'Hybrid', 'Desi', 'Summer', 'Raya', 'Hybrid', 'Legume', 'Tuber', 'Bulb'],
            'Unit_Measure': ['Quintals'] * 10
        })
        df_crops.to_excel(writer, sheet_name='MASTER_Crops', index=False)
        
        # SHEET 4: Crop_Season_Master - Multiple crops for comparison
        df_crop_season = pd.DataFrame({
            'Crop_Season_ID': ['CS001', 'CS002', 'CS003'],
            'Farm_ID': ['F001', 'F001', 'F001'],
            'Season_ID': ['S001', 'S001', 'S002'],
            'Crop_ID': ['C001', 'C004', 'C002'],
            'Variety': ['PBW 826', 'Desi Gram', 'Pusa Basmati'],
            'Area_Acres': [5, 3, 4],
            'Sowing_Date': ['2024-11-10', '2024-11-15', '2024-06-20'],
            'Expected_Harvest': ['2025-04-15', '2025-03-30', '2024-10-15'],
            'Status': ['Active', 'Active', 'Completed'],
            'Created_Date': ['2024-11-01', '2024-11-01', '2024-06-01']
        })
        df_crop_season.to_excel(writer, sheet_name='Crop_Season_Master', index=False)
        
        # SHEET 5: PRE_PROD_Land_Preparation
        df_land_prep = pd.DataFrame({
            'Land_Prep_ID': ['LP001', 'LP002', 'LP003', 'LP004', 'LP005', 'LP006'],
            'Crop_Season_ID': ['CS001', 'CS001', 'CS001', 'CS002', 'CS002', 'CS003'],
            'Date': ['2024-11-01', '2024-11-03', '2024-11-05', '2024-11-05', '2024-11-07', '2024-06-10'],
            'Operation_Type': ['Ploughing', 'Planking', 'Laser Leveling', 'Ploughing', 'Planking', 'Ploughing'],
            'Quantity': [2, 2, 5, 2, 2, 2],
            'Unit': ['times', 'times', 'acres', 'times', 'times', 'times'],
            'Rate_Per_Unit': [400, 150, 500, 400, 150, 400],
            'Total_Cost': [800, 300, 2500, 800, 300, 800],
            'Payment_Mode': ['Cash', 'Cash', 'UPI', 'Cash', 'Cash', 'Cash'],
            'Payment_Status': ['Paid', 'Paid', 'Paid', 'Paid', 'Paid', 'Paid'],
            'Notes': ['Disc Harrow', '', '', 'Deep ploughing', '', 'Disc plough']
        })
        df_land_prep.to_excel(writer, sheet_name='PRE_PROD_Land_Preparation', index=False)
        
        # SHEET 6: PRE_PROD_Seed_Costs
        df_seed = pd.DataFrame({
            'Seed_Cost_ID': ['SC001', 'SC002', 'SC003'],
            'Crop_Season_ID': ['CS001', 'CS002', 'CS003'],
            'Date': ['2024-11-08', '2024-11-10', '2024-06-15'],
            'Variety': ['PBW 826', 'Desi Gram', 'Pusa Basmati'],
            'Qty_KG': [200, 100, 120],
            'Rate_Per_KG': [35, 80, 150],
            'Seed_Cost': [7000, 8000, 18000],
            'Treatment_Chemical': ['Vitavax', 'Thiram', 'Carbendazim'],
            'Treatment_Cost': [500, 400, 600],
            'Biofertilizer_Cost': [250, 200, 300],
            'Total_Seed_Cost': [7750, 8600, 18900],
            'Payment_Mode': ['Cash', 'Cash', 'UPI'],
            'Payment_Status': ['Paid', 'Paid', 'Paid']
        })
        df_seed.to_excel(writer, sheet_name='PRE_PROD_Seed_Costs', index=False)
        
        # SHEET 7: PRE_PROD_Organic_Manure
        df_manure = pd.DataFrame({
            'Manure_ID': ['OM001', 'OM002', 'OM003'],
            'Crop_Season_ID': ['CS001', 'CS002', 'CS003'],
            'Date': ['2024-10-25', '2024-10-28', '2024-06-05'],
            'Manure_Type': ['FYM', 'FYM', 'Compost'],
            'Qty_Tonnes': [40, 25, 35],
            'Rate_Per_Tonne': [800, 800, 1000],
            'Material_Cost': [32000, 20000, 35000],
            'Labor_Cost': [2000, 1500, 2500],
            'Transport_Cost': [3000, 2000, 3500],
            'Total_Manure_Cost': [37000, 23500, 41000],
            'Payment_Mode': ['Cash', 'Cash', 'Bank Transfer'],
            'Payment_Status': ['Paid', 'Paid', 'Paid']
        })
        df_manure.to_excel(writer, sheet_name='PRE_PROD_Organic_Manure', index=False)
        
        # SHEET 8: PROD_Fertilizer_Application
        df_fertilizer = pd.DataFrame({
            'Fertilizer_ID': ['FR001', 'FR002', 'FR003', 'FR004', 'FR005', 'FR006', 'FR007'],
            'Crop_Season_ID': ['CS001', 'CS001', 'CS001', 'CS002', 'CS002', 'CS003', 'CS003'],
            'Date': ['2024-11-10', '2024-12-20', '2025-01-25', '2024-11-15', '2024-12-25', '2024-06-20', '2024-07-25'],
            'Stage': ['Basal', '1st Split', '2nd Split', 'Basal', '1st Split', 'Basal', '1st Split'],
            'Fertilizer_Name': ['DAP', 'Urea', 'Urea', 'DAP', 'Urea', 'DAP', 'Urea'],
            'Qty_KG': [275, 225, 225, 120, 100, 200, 180],
            'Rate_Per_KG': [32, 8, 8, 32, 8, 32, 8],
            'Fertilizer_Cost': [8800, 1800, 1800, 3840, 800, 6400, 1440],
            'Labor_Cost': [500, 300, 300, 300, 200, 400, 300],
            'Total_Fertilizer_Cost': [9300, 2100, 2100, 4140, 1000, 6800, 1740],
            'Payment_Mode': ['Cash', 'Cash', 'Cash', 'Cash', 'Cash', 'UPI', 'UPI'],
            'Payment_Status': ['Paid', 'Paid', 'Pending', 'Paid', 'Paid', 'Paid', 'Paid']
        })
        df_fertilizer.to_excel(writer, sheet_name='PROD_Fertilizer_Application', index=False)
        
        # SHEET 9: PROD_Irrigation_Costs
        df_irrigation = pd.DataFrame({
            'Irrigation_ID': ['IR001', 'IR002', 'IR003', 'IR004', 'IR005', 'IR006'],
            'Crop_Season_ID': ['CS001', 'CS001', 'CS002', 'CS002', 'CS003', 'CS003'],
            'Date': ['2024-12-05', '2024-12-25', '2024-12-10', '2025-01-05', '2024-07-05', '2024-08-10'],
            'Irrigation_No': [1, 2, 1, 2, 1, 2],
            'Method': ['Flood', 'Flood', 'Sprinkler', 'Sprinkler', 'Flood', 'Flood'],
            'Water_Source': ['Tubewell', 'Tubewell', 'Tubewell', 'Tubewell', 'Canal', 'Canal'],
            'Hours_Run': [8, 8, 6, 6, 10, 10],
            'Electricity_Units': [120, 120, 90, 90, 150, 150],
            'Electricity_Cost': [960, 960, 720, 720, 1200, 1200],
            'Diesel_Cost': [0, 0, 0, 0, 500, 500],
            'Labor_Cost': [200, 200, 150, 150, 300, 300],
            'Total_Irrigation_Cost': [1160, 1160, 870, 870, 2000, 2000],
            'Payment_Status': ['Paid', 'Paid', 'Paid', 'Pending', 'Paid', 'Paid']
        })
        df_irrigation.to_excel(writer, sheet_name='PROD_Irrigation_Costs', index=False)
        
        # SHEET 10: POST_PROD_Yield_Record
        df_yield = pd.DataFrame({
            'Yield_ID': ['YD001', 'YD002', 'YD003'],
            'Crop_Season_ID': ['CS001', 'CS002', 'CS003'],
            'Harvest_Date': ['2025-04-15', '2025-03-30', '2024-10-15'],
            'Main_Product_Qtls': [120, 36, 96],
            'Yield_Per_Acre': [24, 12, 24],
            'By_Product_Qtls': [80, 20, 60],
            'Expected_Yield_Per_Acre': [23.2, 11.5, 22.0],
            'Variance_%': [3.45, 4.35, 9.09]
        })
        df_yield.to_excel(writer, sheet_name='POST_PROD_Yield_Record', index=False)
        
        # SHEET 11: REVENUE_Sales
        df_sales = pd.DataFrame({
            'Sale_ID': ['SL001', 'SL002', 'SL003', 'SL004', 'SL005', 'SL006'],
            'Crop_Season_ID': ['CS001', 'CS001', 'CS002', 'CS002', 'CS003', 'CS003'],
            'Sale_Date': ['2025-06-20', '2025-06-20', '2025-05-15', '2025-05-15', '2024-11-20', '2024-11-20'],
            'Product_Type': ['Main Product', 'Straw', 'Main Product', 'Straw', 'Main Product', 'Straw'],
            'Qty_Qtls': [120, 80, 36, 20, 96, 60],
            'Rate_Per_Qtl': [2275, 300, 5500, 200, 2100, 250],
            'Gross_Revenue': [273000, 24000, 198000, 4000, 201600, 15000],
            'Buyer_Name': ['Mandi', 'Local Buyer', 'Mandi', 'Local Buyer', 'Mandi', 'Local Buyer'],
            'Buyer_Type': ['Mandi', 'Direct', 'Mandi', 'Direct', 'Mandi', 'Direct'],
            'MSP_Rate': [2275, 'NA', 5500, 'NA', 2100, 'NA'],
            'Payment_Received': [273000, 24000, 198000, 4000, 201600, 15000],
            'Outstanding': [0, 0, 0, 0, 0, 0]
        })
        df_sales.to_excel(writer, sheet_name='REVENUE_Sales', index=False)
    
    output.seek(0)
    return output

# ====================
# FUNCTION: LOAD EXCEL DATA
# ====================
def load_excel_data(uploaded_file):
    """Load all sheets from the uploaded Excel file"""
    try:
        excel_data = pd.read_excel(uploaded_file, sheet_name=None)
        return excel_data
    except Exception as e:
        st.error(f"Error loading Excel file: {e}")
        return None

# ====================
# FUNCTION: CALCULATE SUMMARY METRICS
# ====================
def calculate_summary_metrics(excel_data):
    """Calculate overall financial metrics from all cost and revenue sheets"""
    metrics = {}
    
    try:
        # Calculate costs from different sheets
        land_prep_cost = excel_data.get('PRE_PROD_Land_Preparation', pd.DataFrame())['Total_Cost'].sum() if 'PRE_PROD_Land_Preparation' in excel_data else 0
        seed_cost = excel_data.get('PRE_PROD_Seed_Costs', pd.DataFrame())['Total_Seed_Cost'].sum() if 'PRE_PROD_Seed_Costs' in excel_data else 0
        manure_cost = excel_data.get('PRE_PROD_Organic_Manure', pd.DataFrame())['Total_Manure_Cost'].sum() if 'PRE_PROD_Organic_Manure' in excel_data else 0
        fertilizer_cost = excel_data.get('PROD_Fertilizer_Application', pd.DataFrame())['Total_Fertilizer_Cost'].sum() if 'PROD_Fertilizer_Application' in excel_data else 0
        irrigation_cost = excel_data.get('PROD_Irrigation_Costs', pd.DataFrame())['Total_Irrigation_Cost'].sum() if 'PROD_Irrigation_Costs' in excel_data else 0
        
        # Total costs
        total_cost = land_prep_cost + seed_cost + manure_cost + fertilizer_cost + irrigation_cost
        
        # Revenue
        total_revenue = excel_data.get('REVENUE_Sales', pd.DataFrame())['Gross_Revenue'].sum() if 'REVENUE_Sales' in excel_data else 0
        
        # Profit
        net_profit = total_revenue - total_cost
        roi = (net_profit / total_cost * 100) if total_cost > 0 else 0
        
        metrics = {
            'total_cost': total_cost,
            'total_revenue': total_revenue,
            'net_profit': net_profit,
            'roi': roi
        }
    except Exception as e:
        st.error(f"Error calculating metrics: {e}")
    
    return metrics

# ====================
# FUNCTION: DISPLAY DASHBOARD
# ====================
def display_dashboard(excel_data, metrics):
    """Display the main dashboard with key metrics and charts"""
    st.markdown('<p class="main-header">🌾 ROOTS - Farm Accounting Dashboard</p>', unsafe_allow_html=True)
    
    # Key Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Investment", f"₹{metrics['total_cost']:,.0f}")
    
    with col2:
        st.metric("Total Revenue", f"₹{metrics['total_revenue']:,.0f}")
    
    with col3:
        st.metric("Net Profit/Loss", f"₹{metrics['net_profit']:,.0f}")
    
    with col4:
        st.metric("ROI", f"{metrics['roi']:.2f}%")
    
    # Charts Section
    st.markdown('<p class="sub-header">Cost Distribution</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Cost breakdown pie chart
        cost_data = {
            'Category': ['Land Preparation', 'Seeds', 'Manure', 'Fertilizers', 'Irrigation'],
            'Amount': [
                excel_data.get('PRE_PROD_Land_Preparation', pd.DataFrame())['Total_Cost'].sum() if 'PRE_PROD_Land_Preparation' in excel_data else 0,
                excel_data.get('PRE_PROD_Seed_Costs', pd.DataFrame())['Total_Seed_Cost'].sum() if 'PRE_PROD_Seed_Costs' in excel_data else 0,
                excel_data.get('PRE_PROD_Organic_Manure', pd.DataFrame())['Total_Manure_Cost'].sum() if 'PRE_PROD_Organic_Manure' in excel_data else 0,
                excel_data.get('PROD_Fertilizer_Application', pd.DataFrame())['Total_Fertilizer_Cost'].sum() if 'PROD_Fertilizer_Application' in excel_data else 0,
                excel_data.get('PROD_Irrigation_Costs', pd.DataFrame())['Total_Irrigation_Cost'].sum() if 'PROD_Irrigation_Costs' in excel_data else 0
            ]
        }
        df_costs = pd.DataFrame(cost_data)
        df_costs = df_costs[df_costs['Amount'] > 0]
        
        if not df_costs.empty:
            fig_pie = px.pie(df_costs, values='Amount', names='Category', 
                           title='Cost Distribution by Category',
                           color_discrete_sequence=px.colors.sequential.Greens)
            st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # Revenue vs Cost bar chart
        comparison_data = {
            'Metric': ['Total Cost', 'Total Revenue'],
            'Amount': [metrics['total_cost'], metrics['total_revenue']]
        }
        df_comparison = pd.DataFrame(comparison_data)
        
        fig_bar = px.bar(df_comparison, x='Metric', y='Amount',
                        title='Revenue vs Cost Comparison',
                        color='Metric',
                        color_discrete_map={'Total Cost': '#ef5350', 'Total Revenue': '#66bb6a'})
        st.plotly_chart(fig_bar, use_container_width=True)

# ====================
# FUNCTION: DISPLAY DATA ENTRY FORMS
# ====================
def display_data_entry(excel_data):
    """Display forms for entering new farm data"""
    st.markdown('<p class="sub-header">📝 Data Entry</p>', unsafe_allow_html=True)
    
    entry_type = st.selectbox("Select Entry Type", [
        "Land Preparation",
        "Seed Costs",
        "Fertilizer Application",
        "Sales Record"
    ])
    
    if entry_type == "Land Preparation":
        with st.form("land_prep_form"):
            col1, col2 = st.columns(2)
            with col1:
                crop_season_id = st.text_input("Crop Season ID", "CS001")
                date = st.date_input("Date")
                operation_type = st.text_input("Operation Type")
                quantity = st.number_input("Quantity", min_value=0.0)
            
            with col2:
                unit = st.text_input("Unit")
                rate_per_unit = st.number_input("Rate per Unit", min_value=0.0)
                payment_mode = st.selectbox("Payment Mode", ["Cash", "UPI", "Bank Transfer"])
                payment_status = st.selectbox("Payment Status", ["Paid", "Pending", "Partial"])
            
            notes = st.text_area("Notes")
            
            if st.form_submit_button("Add Entry"):
                st.success("Entry added successfully!")
    
    elif entry_type == "Fertilizer Application":
        with st.form("fertilizer_form"):
            col1, col2 = st.columns(2)
            with col1:
                crop_season_id = st.text_input("Crop Season ID", "CS001")
                date = st.date_input("Date")
                stage = st.selectbox("Stage", ["Basal", "1st Split", "2nd Split", "3rd Split"])
                fertilizer_name = st.text_input("Fertilizer Name")
            
            with col2:
                qty_kg = st.number_input("Quantity (KG)", min_value=0.0)
                rate_per_kg = st.number_input("Rate per KG", min_value=0.0)
                labor_cost = st.number_input("Labor Cost", min_value=0.0)
                payment_status = st.selectbox("Payment Status", ["Paid", "Pending", "Partial"])
            
            if st.form_submit_button("Add Entry"):
                st.success("Fertilizer entry added successfully!")
    
    elif entry_type == "Sales Record":
        with st.form("sales_form"):
            col1, col2 = st.columns(2)
            with col1:
                crop_season_id = st.text_input("Crop Season ID", "CS001")
                sale_date = st.date_input("Sale Date")
                product_type = st.selectbox("Product Type", ["Main Product", "By-Product", "Straw"])
                qty_qtls = st.number_input("Quantity (Quintals)", min_value=0.0)
            
            with col2:
                rate_per_qtl = st.number_input("Rate per Quintal", min_value=0.0)
                buyer_name = st.text_input("Buyer Name")
                buyer_type = st.selectbox("Buyer Type", ["Mandi", "Direct", "Trader"])
                payment_received = st.number_input("Payment Received", min_value=0.0)
            
            if st.form_submit_button("Add Sale"):
                st.success("Sale record added successfully!")

# ====================
# FUNCTION: DISPLAY REPORTS
# ====================
def display_reports(excel_data):
    """Display various reports from the data"""
    st.markdown('<p class="sub-header">📊 Reports</p>', unsafe_allow_html=True)
    
    report_type = st.selectbox("Select Report", [
        "Cost Summary",
        "Revenue Summary",
        "Yield Analysis"
    ])
    
    if report_type == "Cost Summary":
        if 'PRE_PROD_Land_Preparation' in excel_data:
            st.write("**Land Preparation Costs**")
            st.dataframe(excel_data['PRE_PROD_Land_Preparation'], use_container_width=True)
        
        if 'PROD_Fertilizer_Application' in excel_data:
            st.write("**Fertilizer Application Costs**")
            st.dataframe(excel_data['PROD_Fertilizer_Application'], use_container_width=True)
    
    elif report_type == "Revenue Summary":
        if 'REVENUE_Sales' in excel_data:
            st.write("**Sales Records**")
            st.dataframe(excel_data['REVENUE_Sales'], use_container_width=True)
            
            total_revenue = excel_data['REVENUE_Sales']['Gross_Revenue'].sum()
            st.metric("Total Sales Revenue", f"₹{total_revenue:,.0f}")
    
    elif report_type == "Yield Analysis":
        if 'POST_PROD_Yield_Record' in excel_data:
            st.write("**Yield Performance**")
            st.dataframe(excel_data['POST_PROD_Yield_Record'], use_container_width=True)

# ====================
# FUNCTION: DISPLAY CROP COMPARISON
# ====================
def display_crop_comparison(excel_data):
    """Display detailed crop-by-crop comparison analysis"""
    st.markdown('<p class="sub-header">🌾 Crop Comparison Analysis</p>', unsafe_allow_html=True)
    
    if 'Crop_Season_Master' not in excel_data:
        st.warning("No crop season data available. Please upload data first.")
        return
    
    crop_seasons = excel_data['Crop_Season_Master']
    
    if crop_seasons.empty:
        st.warning("No crop seasons found.")
        return
    
    # Merge with crop master to get crop names
    if 'MASTER_Crops' in excel_data:
        crops_master = excel_data['MASTER_Crops']
        crop_seasons = crop_seasons.merge(
            crops_master[['Crop_ID', 'Crop_Name', 'Category']], 
            on='Crop_ID', 
            how='left'
        )
    
    # Calculate costs and revenue for each crop season
    comparison_data = []
    
    for _, season in crop_seasons.iterrows():
        cs_id = season['Crop_Season_ID']
        crop_name = season.get('Crop_Name', 'Unknown')
        area = season.get('Area_Acres', 0)
        
        # Calculate total costs
        total_cost = 0
        
        # Land preparation
        if 'PRE_PROD_Land_Preparation' in excel_data:
            land_cost = excel_data['PRE_PROD_Land_Preparation'][
                excel_data['PRE_PROD_Land_Preparation']['Crop_Season_ID'] == cs_id
            ]['Total_Cost'].sum()
            total_cost += land_cost
        
        # Seed costs
        if 'PRE_PROD_Seed_Costs' in excel_data:
            seed_cost = excel_data['PRE_PROD_Seed_Costs'][
                excel_data['PRE_PROD_Seed_Costs']['Crop_Season_ID'] == cs_id
            ]['Total_Seed_Cost'].sum()
            total_cost += seed_cost
        
        # Manure costs
        if 'PRE_PROD_Organic_Manure' in excel_data:
            manure_cost = excel_data['PRE_PROD_Organic_Manure'][
                excel_data['PRE_PROD_Organic_Manure']['Crop_Season_ID'] == cs_id
            ]['Total_Manure_Cost'].sum()
            total_cost += manure_cost
        
        # Fertilizer costs
        if 'PROD_Fertilizer_Application' in excel_data:
            fert_cost = excel_data['PROD_Fertilizer_Application'][
                excel_data['PROD_Fertilizer_Application']['Crop_Season_ID'] == cs_id
            ]['Total_Fertilizer_Cost'].sum()
            total_cost += fert_cost
        
        # Irrigation costs
        if 'PROD_Irrigation_Costs' in excel_data:
            irr_cost = excel_data['PROD_Irrigation_Costs'][
                excel_data['PROD_Irrigation_Costs']['Crop_Season_ID'] == cs_id
            ]['Total_Irrigation_Cost'].sum()
            total_cost += irr_cost
        
        # Revenue
        total_revenue = 0
        if 'REVENUE_Sales' in excel_data:
            total_revenue = excel_data['REVENUE_Sales'][
                excel_data['REVENUE_Sales']['Crop_Season_ID'] == cs_id
            ]['Gross_Revenue'].sum()
        
        # Yield
        yield_per_acre = 0
        if 'POST_PROD_Yield_Record' in excel_data:
            yield_data = excel_data['POST_PROD_Yield_Record'][
                excel_data['POST_PROD_Yield_Record']['Crop_Season_ID'] == cs_id
            ]
            if not yield_data.empty:
                yield_per_acre = yield_data['Yield_Per_Acre'].iloc[0]
        
        profit = total_revenue - total_cost
        roi = (profit / total_cost * 100) if total_cost > 0 else 0
        cost_per_acre = total_cost / area if area > 0 else 0
        revenue_per_acre = total_revenue / area if area > 0 else 0
        
        comparison_data.append({
            'Crop': crop_name,
            'Crop_Season_ID': cs_id,
            'Area (Acres)': area,
            'Total Cost': total_cost,
            'Total Revenue': total_revenue,
            'Profit/Loss': profit,
            'ROI (%)': roi,
            'Cost per Acre': cost_per_acre,
            'Revenue per Acre': revenue_per_acre,
            'Yield per Acre': yield_per_acre
        })
    
    df_comparison = pd.DataFrame(comparison_data)
    
    if df_comparison.empty:
        st.warning("No data available for comparison.")
        return
    
    # Display metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        most_profitable = df_comparison.loc[df_comparison['Profit/Loss'].idxmax()]
        st.metric("Most Profitable Crop", most_profitable['Crop'], 
                 f"₹{most_profitable['Profit/Loss']:,.0f}")
    
    with col2:
        highest_roi = df_comparison.loc[df_comparison['ROI (%)'].idxmax()]
        st.metric("Highest ROI", highest_roi['Crop'], 
                 f"{highest_roi['ROI (%)']:.1f}%")
    
    with col3:
        highest_yield = df_comparison.loc[df_comparison['Yield per Acre'].idxmax()]
        st.metric("Highest Yield/Acre", highest_yield['Crop'], 
                 f"{highest_yield['Yield per Acre']:.1f} Qtls")
    
    # Display comparison table
    st.markdown("### 📋 Detailed Comparison Table")
    st.dataframe(
        df_comparison.style.format({
            'Total Cost': '₹{:,.0f}',
            'Total Revenue': '₹{:,.0f}',
            'Profit/Loss': '₹{:,.0f}',
            'ROI (%)': '{:.2f}%',
            'Cost per Acre': '₹{:,.0f}',
            'Revenue per Acre': '₹{:,.0f}',
            'Yield per Acre': '{:.2f}',
            'Area (Acres)': '{:.1f}'
        }).background_gradient(subset=['Profit/Loss'], cmap='RdYlGn'),
        use_container_width=True
    )
    
    # Visualizations
    st.markdown("### 📊 Visual Comparisons")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_profit = px.bar(
            df_comparison, 
            x='Crop', 
            y='Profit/Loss',
            title='Profit/Loss by Crop',
            color='Profit/Loss',
            color_continuous_scale=['red', 'yellow', 'green'],
            text='Profit/Loss'
        )
        fig_profit.update_traces(texttemplate='₹%{text:,.0f}', textposition='outside')
        st.plotly_chart(fig_profit, use_container_width=True)
    
    with col2:
        fig_roi = px.bar(
            df_comparison,
            x='Crop',
            y='ROI (%)',
            title='Return on Investment (%) by Crop',
            color='ROI (%)',
            color_continuous_scale='Greens',
            text='ROI (%)'
        )
        fig_roi.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        st.plotly_chart(fig_roi, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_cost = px.bar(
            df_comparison,
            x='Crop',
            y=['Cost per Acre', 'Revenue per Acre'],
            title='Cost vs Revenue per Acre',
            barmode='group',
            color_discrete_map={'Cost per Acre': '#ef5350', 'Revenue per Acre': '#66bb6a'}
        )
        st.plotly_chart(fig_cost, use_container_width=True)
    
    with col2:
        fig_yield = px.bar(
            df_comparison,
            x='Crop',
            y='Yield per Acre',
            title='Yield per Acre (Quintals)',
            color='Yield per Acre',
            color_continuous_scale='Blues',
            text='Yield per Acre'
        )
        fig_yield.update_traces(texttemplate='%{text:.1f}', textposition='outside')
        st.plotly_chart(fig_yield, use_container_width=True)
    
    # Recommendations
    st.markdown("### 💡 Recommendations")
    
    best_profit_crop = df_comparison.loc[df_comparison['Profit/Loss'].idxmax()]
    worst_profit_crop = df_comparison.loc[df_comparison['Profit/Loss'].idxmin()]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.success(f"""
        **Best Performing Crop: {best_profit_crop['Crop']}**
        - Profit: ₹{best_profit_crop['Profit/Loss']:,.0f}
        - ROI: {best_profit_crop['ROI (%)']:.1f}%
        - Recommendation: Consider increasing acreage for this crop next season
        """)
    
    with col2:
        if worst_profit_crop['Profit/Loss'] < 0:
            st.error(f"""
            **Needs Attention: {worst_profit_crop['Crop']}**
            - Loss: ₹{abs(worst_profit_crop['Profit/Loss']):,.0f}
            - ROI: {worst_profit_crop['ROI (%)']:.1f}%
            - Recommendation: Review cultivation practices or consider alternative crops
            """)
        else:
            st.info(f"""
            **Lower Performing: {worst_profit_crop['Crop']}**
            - Profit: ₹{worst_profit_crop['Profit/Loss']:,.0f}
            - ROI: {worst_profit_crop['ROI (%)']:.1f}%
            - Recommendation: Optimize costs to improve returns
            """)

# ====================
# FUNCTION: DISPLAY SEASON ANALYSIS
# ====================
def display_season_analysis(excel_data):
    """Display comprehensive season-wise analysis"""
    st.markdown('<p class="sub-header">📅 Season-wise Analysis</p>', unsafe_allow_html=True)
    
    if 'Crop_Season_Master' not in excel_data or 'MASTER_Season' not in excel_data:
        st.warning("Season data not available. Please upload complete data.")
        return
    
    seasons_master = excel_data['MASTER_Season']
    crop_seasons = excel_data['Crop_Season_Master']
    
    # Merge to get season names
    crop_seasons = crop_seasons.merge(
        seasons_master[['Season_ID', 'Season_Name']], 
        on='Season_ID', 
        how='left'
    )
    
    # Merge with crop names
    if 'MASTER_Crops' in excel_data:
        crops_master = excel_data['MASTER_Crops']
        crop_seasons = crop_seasons.merge(
            crops_master[['Crop_ID', 'Crop_Name']], 
            on='Crop_ID', 
            how='left'
        )
    
    # Season selector
    available_seasons = crop_seasons['Season_Name'].dropna().unique().tolist()
    
    if not available_seasons:
        st.warning("No season data found.")
        return
    
    selected_season = st.selectbox("Select Season", available_seasons)
    
    # Filter data for selected season
    season_data = crop_seasons[crop_seasons['Season_Name'] == selected_season]
    
    if season_data.empty:
        st.warning(f"No data available for {selected_season} season.")
        return
    
    # Calculate season metrics
    season_metrics = []
    total_area = season_data['Area_Acres'].sum()
    total_cost = 0
    total_revenue = 0
    
    for _, crop_season in season_data.iterrows():
        cs_id = crop_season['Crop_Season_ID']
        crop_name = crop_season.get('Crop_Name', 'Unknown')
        area = crop_season.get('Area_Acres', 0)
        
        # Calculate costs
        crop_cost = 0
        
        if 'PRE_PROD_Land_Preparation' in excel_data:
            crop_cost += excel_data['PRE_PROD_Land_Preparation'][
                excel_data['PRE_PROD_Land_Preparation']['Crop_Season_ID'] == cs_id
            ]['Total_Cost'].sum()
        
        if 'PRE_PROD_Seed_Costs' in excel_data:
            crop_cost += excel_data['PRE_PROD_Seed_Costs'][
                excel_data['PRE_PROD_Seed_Costs']['Crop_Season_ID'] == cs_id
            ]['Total_Seed_Cost'].sum()
        
        if 'PRE_PROD_Organic_Manure' in excel_data:
            crop_cost += excel_data['PRE_PROD_Organic_Manure'][
                excel_data['PRE_PROD_Organic_Manure']['Crop_Season_ID'] == cs_id
            ]['Total_Manure_Cost'].sum()
        
        if 'PROD_Fertilizer_Application' in excel_data:
            crop_cost += excel_data['PROD_Fertilizer_Application'][
                excel_data['PROD_Fertilizer_Application']['Crop_Season_ID'] == cs_id
            ]['Total_Fertilizer_Cost'].sum()
        
        if 'PROD_Irrigation_Costs' in excel_data:
            crop_cost += excel_data['PROD_Irrigation_Costs'][
                excel_data['PROD_Irrigation_Costs']['Crop_Season_ID'] == cs_id
            ]['Total_Irrigation_Cost'].sum()
        
        # Calculate revenue
        crop_revenue = 0
        if 'REVENUE_Sales' in excel_data:
            crop_revenue = excel_data['REVENUE_Sales'][
                excel_data['REVENUE_Sales']['Crop_Season_ID'] == cs_id
            ]['Gross_Revenue'].sum()
        
        total_cost += crop_cost
        total_revenue += crop_revenue
        
        season_metrics.append({
            'Crop': crop_name,
            'Area (Acres)': area,
            'Cost': crop_cost,
            'Revenue': crop_revenue,
            'Profit': crop_revenue - crop_cost
        })
    
    df_season = pd.DataFrame(season_metrics)
    
    # Display season summary
    st.markdown(f"### 🌱 {selected_season} Season Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Area", f"{total_area:.1f} Acres")
    
    with col2:
        st.metric("Total Investment", f"₹{total_cost:,.0f}")
    
    with col3:
        st.metric("Total Revenue", f"₹{total_revenue:,.0f}")
    
    with col4:
        net_profit = total_revenue - total_cost
        st.metric("Net Profit", f"₹{net_profit:,.0f}")
    
    # Crops in this season
    st.markdown("### 🌾 Crops Cultivated")
    st.dataframe(
        df_season.style.format({
            'Area (Acres)': '{:.1f}',
            'Cost': '₹{:,.0f}',
            'Revenue': '₹{:,.0f}',
            'Profit': '₹{:,.0f}'
        }).background_gradient(subset=['Profit'], cmap='RdYlGn'),
        use_container_width=True
    )
    
    # Visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        fig_area = px.pie(
            df_season,
            values='Area (Acres)',
            names='Crop',
            title=f'Land Distribution - {selected_season} Season',
            color_discrete_sequence=px.colors.sequential.Greens
        )
        st.plotly_chart(fig_area, use_container_width=True)
    
    with col2:
        fig_profit = px.bar(
            df_season,
            x='Crop',
            y='Profit',
            title=f'Profit by Crop - {selected_season} Season',
            color='Profit',
            color_continuous_scale=['red', 'yellow', 'green']
        )
        st.plotly_chart(fig_profit, use_container_width=True)
    
    # Compare all seasons
    st.markdown("### 📊 Compare All Seasons")
    
    all_seasons_data = []
    
    for season in available_seasons:
        season_crops = crop_seasons[crop_seasons['Season_Name'] == season]
        
        season_cost = 0
        season_revenue = 0
        season_area = season_crops['Area_Acres'].sum()
        
        for _, crop_season in season_crops.iterrows():
            cs_id = crop_season['Crop_Season_ID']
            
            if 'PRE_PROD_Land_Preparation' in excel_data:
                season_cost += excel_data['PRE_PROD_Land_Preparation'][
                    excel_data['PRE_PROD_Land_Preparation']['Crop_Season_ID'] == cs_id
                ]['Total_Cost'].sum()
            
            if 'PRE_PROD_Seed_Costs' in excel_data:
                season_cost += excel_data['PRE_PROD_Seed_Costs'][
                    excel_data['PRE_PROD_Seed_Costs']['Crop_Season_ID'] == cs_id
                ]['Total_Seed_Cost'].sum()
            
            if 'PRE_PROD_Organic_Manure' in excel_data:
                season_cost += excel_data['PRE_PROD_Organic_Manure'][
                    excel_data['PRE_PROD_Organic_Manure']['Crop_Season_ID'] == cs_id
                ]['Total_Manure_Cost'].sum()
            
            if 'PROD_Fertilizer_Application' in excel_data:
                season_cost += excel_data['PROD_Fertilizer_Application'][
                    excel_data['PROD_Fertilizer_Application']['Crop_Season_ID'] == cs_id
                ]['Total_Fertilizer_Cost'].sum()
            
            if 'PROD_Irrigation_Costs' in excel_data:
                season_cost += excel_data['PROD_Irrigation_Costs'][
                    excel_data['PROD_Irrigation_Costs']['Crop_Season_ID'] == cs_id
                ]['Total_Irrigation_Cost'].sum()
            
            if 'REVENUE_Sales' in excel_data:
                season_revenue += excel_data['REVENUE_Sales'][
                    excel_data['REVENUE_Sales']['Crop_Season_ID'] == cs_id
                ]['Gross_Revenue'].sum()
        
        all_seasons_data.append({
            'Season': season,
            'Total Area': season_area,
            'Total Cost': season_cost,
            'Total Revenue': season_revenue,
            'Net Profit': season_revenue - season_cost,
            'ROI (%)': (season_revenue - season_cost) / season_cost * 100 if season_cost > 0 else 0
        })
    
    df_all_seasons = pd.DataFrame(all_seasons_data)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_seasons = px.bar(
            df_all_seasons,
            x='Season',
            y=['Total Cost', 'Total Revenue'],
            title='Cost vs Revenue by Season',
            barmode='group',
            color_discrete_map={'Total Cost': '#ef5350', 'Total Revenue': '#66bb6a'}
        )
        st.plotly_chart(fig_seasons, use_container_width=True)
    
    with col2:
        fig_roi = px.bar(
            df_all_seasons,
            x='Season',
            y='ROI (%)',
            title='Return on Investment by Season',
            color='ROI (%)',
            color_continuous_scale='Greens',
            text='ROI (%)'
        )
        fig_roi.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        st.plotly_chart(fig_roi, use_container_width=True)
    
    # Season comparison table
    st.markdown("### 📋 Season Comparison Table")
    st.dataframe(
        df_all_seasons.style.format({
            'Total Area': '{:.1f}',
            'Total Cost': '₹{:,.0f}',
            'Total Revenue': '₹{:,.0f}',
            'Net Profit': '₹{:,.0f}',
            'ROI (%)': '{:.2f}%'
        }).background_gradient(subset=['Net Profit'], cmap='RdYlGn'),
        use_container_width=True
    )
    
    # Best season recommendation
    best_season = df_all_seasons.loc[df_all_seasons['Net Profit'].idxmax()]
    
    st.success(f"""
    ### 🏆 Best Performing Season: {best_season['Season']}
    - Net Profit: ₹{best_season['Net Profit']:,.0f}
    - ROI: {best_season['ROI (%)']:.1f}%
    - Total Area: {best_season['Total Area']:.1f} acres
    
    **Recommendation:** Focus on optimizing practices for this season to maximize returns.
    """)

# ====================
# MAIN APPLICATION
# ====================
def main():
    """Main application function"""
    
    # Sidebar
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/628/628283.png", width=100)
        st.title("🌾 ROOTS")
        st.markdown("**Farm Accounting Software**")
        st.markdown("---")
        
        page = st.radio("Navigation", [
            "🏠 Dashboard",
            "📝 Data Entry",
            "📊 Reports",
            "🌾 Crop Comparison",
            "📅 Season Analysis",
            "⚙️ Settings"
        ])
        
        st.markdown("---")
        
        # File upload
        st.subheader("Upload Excel File")
        uploaded_file = st.file_uploader("Choose Excel file", type=['xlsx', 'xls'])
        
        # Download sample template
        st.markdown("---")
        st.subheader("Download Template")
        sample_file = create_sample_excel()
        st.download_button(
            label="📥 Download Sample Excel",
            data=sample_file,
            file_name="roots_farm_template.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    
    # Main content area
    if uploaded_file is not None:
        excel_data = load_excel_data(uploaded_file)
        
        if excel_data:
            metrics = calculate_summary_metrics(excel_data)
            
            if page == "🏠 Dashboard":
                display_dashboard(excel_data, metrics)
            elif page == "📝 Data Entry":
                display_data_entry(excel_data)
            elif page == "📊 Reports":
                display_reports(excel_data)
            elif page == "🌾 Crop Comparison":
                display_crop_comparison(excel_data)
            elif page == "📅 Season Analysis":
                display_season_analysis(excel_data)
            elif page == "⚙️ Settings":
                st.markdown('<p class="sub-header">⚙️ Settings</p>', unsafe_allow_html=True)
                st.info("Settings panel - Configure your farm profile and preferences")
    else:
        st.info("👆 Please upload an Excel file or download the sample template to get started")
        
        # Show welcome message
        st.markdown('<p class="main-header">Welcome to ROOTS 🌾</p>', unsafe_allow_html=True)
        st.markdown("""
        ### Your Complete Farm Accounting Solution
        
        **Features:**
        - 📊 Track all farming costs (Land prep, Seeds, Fertilizers, etc.)
        - 💰 Record revenue and sales
        - 📈 Automatic profit/loss calculations
        - 🌾 Compare crops side-by-side
        - 📅 Analyze seasonal performance
        - 📱 Mobile-friendly data entry
        - 📉 Visual analytics and reports
        
        **Getting Started:**
        1. Download the sample Excel template from the sidebar
        2. Fill in your farm data
        3. Upload the file to see your dashboard
        
        **Or** start entering data directly using the Data Entry page!
        """)

# ====================
# APPLICATION ENTRY POINT
# ====================
if __name__ == "__main__":
    main()

# ====================
# END OF CODE
# ====================