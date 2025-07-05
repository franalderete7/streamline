def get_css_styles():
    """
    Returns the CSS styles for the Streamlit application with dark theme
    """
    return """
        /* Main page styling */
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        
        /* Sidebar styling */
        .css-1d391kg {
            background-color: #1e1e1e;
        }
        
        .stSidebar {
            background-color: #1e1e1e;
            color: white;
        }
        
        .stSidebar .sidebar-content {
            background-color: #1e1e1e;
        }
        
        .stSidebar .element-container {
            margin-bottom: 15px;
            padding: 10px;
            border-radius: 8px;
            background-color: #2d2d2d;
            border: 1px solid #404040;
        }
        
        .stSidebar label {
            font-weight: 600;
            color: white !important;
            font-size: 14px;
            margin-bottom: 5px;
            display: block;
        }
        
        .stSidebar .stNumberInput input {
            background-color: #404040;
            border: 1px solid #555;
            border-radius: 6px;
            padding: 8px 12px;
            color: white;
            font-size: 14px;
        }
        
        .stSidebar .stNumberInput input:focus {
            border-color: #2196F3;
            box-shadow: 0 0 0 2px rgba(33, 150, 243, 0.2);
        }
        
        /* Button styling - Blue theme */
        .stButton > button {
            background: linear-gradient(135deg, #2196F3, #1976D2);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 12px 24px;
            font-weight: 600;
            font-size: 14px;
            transition: all 0.3s ease;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }
        
        .stButton > button:hover {
            background: linear-gradient(135deg, #1976D2, #2196F3);
            transform: translateY(-1px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.3);
        }
        
        /* Dataframe styling - Dark theme */
        .stDataFrame {
            font-size: 14px;
            border: 2px solid #333;
            border-radius: 8px;
            padding: 15px;
            background: linear-gradient(135deg, #2d2d2d, #1a1a1a);
            box-shadow: 0 2px 8px rgba(0,0,0,0.3);
            width: 100% !important;
            max-width: 100% !important;
        }
        
        .stDataFrame > div {
            width: 100% !important;
            max-width: 100% !important;
        }
        
        .stDataFrame table {
            width: 100% !important;
            max-width: 100% !important;
        }
        
        /* Force table to take full width */
        .dataframe {
            width: 100% !important;
            max-width: 100% !important;
            background: linear-gradient(135deg, #2d2d2d, #1a1a1a) !important;
            border: 2px solid #333 !important;
            border-radius: 8px !important;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        .dataframe th {
            background-color: #333 !important;
            font-weight: 600;
            color: white !important;
            border-bottom: 2px solid #555 !important;
            padding: 12px 8px !important;
        }
        
        .dataframe td {
            background-color: rgba(255, 255, 255, 0.05) !important;
            border-bottom: 1px solid #444 !important;
            padding: 10px 8px !important;
            color: #e0e0e0 !important;
        }
        
        .dataframe tr:nth-child(even) td {
            background-color: rgba(255, 255, 255, 0.08) !important;
        }
        
        /* Subheader styling */
        .stSubheader {
            color: #e0e0e0;
            font-weight: 600;
            font-size: 1.5rem;
            margin-bottom: 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid #2196F3;
        }
        
        /* Financial summary box - Dark theme */
        .summary-box {
            background: linear-gradient(135deg, #2c3e50, #34495e);
            border: 2px solid #3498db;
            border-radius: 12px;
            padding: 25px;
            margin: 20px 0;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            color: white;
        }
        
        .summary-box p {
            color: white;
            font-size: 16px;
            margin: 12px 0;
            padding: 8px 0;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }
        
        .summary-box p:last-child {
            border-bottom: none;
        }
        
        .summary-box b {
            color: #3498db;
            font-weight: 600;
        }
        
        /* Download buttons - Blue theme */
        .stDownloadButton > button {
            background: linear-gradient(135deg, #2196F3, #1976D2);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 10px 20px;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }
        
        .stDownloadButton > button:hover {
            background: linear-gradient(135deg, #1976D2, #2196F3);
            transform: translateY(-1px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.3);
        }
        
        /* Chart container */
        .stPlotlyChart {
            border-radius: 8px;
            padding: 15px;
            background-color: #2d2d2d;
            box-shadow: 0 2px 8px rgba(0,0,0,0.3);
        }
        
        /* Header styling - Dark theme */
        h1 {
            color: white;
            font-weight: 700;
            text-align: center;
            margin-bottom: 2rem;
            padding: 1rem;
            background: linear-gradient(135deg, #2c3e50, #34495e);
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        }
        
        /* Responsive design */
        @media (max-width: 768px) {
            .stSidebar .element-container {
                margin-bottom: 10px;
                padding: 8px;
            }
            
            .summary-box {
                padding: 20px;
            }
            
            .summary-box p {
                font-size: 14px;
            }
        }
        
        /* Additional improvements */
        .stMarkdown {
            line-height: 1.6;
        }
        
        .stMarkdown p {
            margin-bottom: 1rem;
            color: #e0e0e0;
        }
        
        /* Remove any white backgrounds */
        .stDataFrame, .dataframe, .stDataFrame > div, .stDataFrame table {
            background: linear-gradient(135deg, #2d2d2d, #1a1a1a) !important;
        }
        
        /* Ensure dark theme throughout */
        .main .block-container {
            background: linear-gradient(135deg, #1a1a1a, #2d2d2d);
        }
        
        .stApp {
            background: linear-gradient(135deg, #1a1a1a, #2d2d2d);
        }
        
        /* Text colors for dark theme */
        .stMarkdown, .stText {
            color: #e0e0e0;
        }
    """ 