import streamlit as st
import os
import sys
import shutil
import markdown
from pathlib import Path
from datetime import datetime

# Add the modules directory to the Python path
sys.path.append(str(Path(__file__).parent / "modules"))

# Import modules
modules = {}
try:
    from modules.module1 import module1
    modules['module1'] = module1
    from modules.module2 import module2
    modules['module2'] = module2
    from modules.module3 import module3
    modules['module3'] = module3
    from modules.module4 import module4
    modules['module4'] = module4
    from modules.module5 import module5
    modules['module5'] = module5
    from modules.module6 import module6
    modules['module6'] = module6
    
except ImportError as e:
    st.error(f"Error importing modules: {e}")
    st.info("Please ensure all module files are properly configured")

# Page configuration
st.set_page_config(
    page_title="Real Estate Operating System",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Enhanced CSS for a professional styling
st.markdown(
    """
<style>
    /* Reset and base styles */
    * { box-sizing: border-box; }
    
    /* Global background */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    }

    /* Main container */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1280px;
        background: transparent;
    }

    /* Sidebar */
    .css-1d391kg {
        background: #0f172a; /* slate-900 */
        border-right: 1px solid #1f2937; /* gray-800 */
    }

    .sidebar-header {
        background: #0b1220;
        padding: 1.25rem 1rem;
        border-radius: 10px;
        margin: 1rem;
        text-align: center;
        border: 1px solid #1f2937;
    }

    .sidebar-header h2 {
        color: #e5e7eb; /* gray-200 */
        margin: 0;
        font-size: 1.25rem;
        font-weight: 700;
        letter-spacing: .3px;
    }

    .sidebar-header .logo {
        background: #0f172a;
        width: 48px; height: 48px;
        border-radius: 10px;
        display: flex; align-items: center; justify-content: center;
        margin: 0 auto 0.75rem;
        border: 1px solid #1f2937;
        color: #38bdf8; /* sky-400 */
    }

    /* Section headers */
    .section-header {
        color: #94a3b8; /* slate-400 */
        font-size: 0.8rem; font-weight: 600;
        text-transform: uppercase; letter-spacing: 0.06em;
        margin: 1.25rem 1rem 0.75rem; padding: 0 0.5rem;
    }

    /* Buttons (Streamlit base buttons in sidebar) */
    .stButton > button {
        background: #111827; /* gray-900 */
        color: #e5e7eb;
        border: 1px solid #1f2937;
        border-radius: 10px;
        padding: 0.6rem 0.9rem;
        text-align: left;
        width: 100%;
        transition: background .15s ease, border-color .15s ease, transform .08s ease;
    }
    .stButton > button:hover {
        background: #0b1220;
        border-color: #334155; /* slate-700 */
    }
    .stButton > button:active { transform: translateY(0); }

    /* Main content area */
    .main-content {
        background: #1e293b; /* slate-800 */
        border-radius: 12px;
        padding: 2rem;
        border: 1px solid #334155; /* slate-700 */
    }

    /* Chat header */
    .chat-header {
        background: #0f172a; /* slate-900 */
        border-radius: 12px;
        padding: 1.25rem 1.5rem;
        margin-bottom: 1.5rem;
        border: 1px solid #334155; /* slate-700 */
    }
    .chat-header .module-tag {
        background: #0ea5e9; /* sky-500 */
        color: #ffffff;
        padding: 0.35rem 0.85rem;
        border-radius: 999px;
        font-size: 0.8rem; font-weight: 600;
        display: inline-block;
        margin-bottom: 0.75rem;
    }
    .chat-header h1 {
        color: #f1f5f9; /* slate-100 */
        margin: 0 0 0.4rem 0; font-size: 1.6rem; font-weight: 700;
    }
    .chat-header .description { color: #94a3b8; font-size: 1rem; margin: 0; }

    /* Chat container */
    .chat-container {
        background: #1e293b; /* slate-800 */
        border-radius: 12px;
        padding: 1.25rem;
        margin-bottom: 1.5rem;
        border: 1px solid #334155; /* slate-700 */ 
        min-height: 400px;
    }

    .chat-message { display: flex; align-items: flex-start; margin-bottom: 1.1rem; }
    .chat-message.user { flex-direction: row-reverse; }
    .chat-message .avatar {
        width: 40px; height: 40px; border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-weight: 700; font-size: 1rem; margin: 0 0.75rem; flex-shrink: 0;
    }
    .chat-message.user .avatar { background: #0ea5e9; color: #fff; }
    .chat-message.bot .avatar { background: #0369a1; color: #fff; }
    .chat-message .content {
        background: #334155; /* slate-700 */ 
        color: #f1f5f9; /* slate-100 */
        padding: 0.85rem 1.1rem; border-radius: 12px; max-width: 72%;
        border: 1px solid #475569; /* slate-600 */
    }
    .chat-message.user .content { background: #0ea5e9; color: #ffffff; border-color: #0ea5e9; }
    .chat-message .timestamp { font-size: 0.72rem; color: #94a3b8; margin-top: 0.35rem; text-align: right; }
    .chat-message.user .timestamp { color: rgba(255,255,255,.85); }

    /* Input area */
    .input-area { background: #1e293b; /* slate-800 */ border-radius: 12px; padding: 1.25rem; border: 1px solid #334155; /* slate-700 */ }
    .input-tools { display: flex; gap: 0.75rem; margin-bottom: 0.75rem; }
    .input-tools .tool-btn {
        background: #334155; /* slate-700 */ border: 1px solid #475569; /* slate-600 */ border-radius: 8px; padding: 0.45rem .85rem;
        color: #f1f5f9; /* slate-100 */ font-size: 0.85rem; cursor: pointer; transition: background .15s ease, border-color .15s ease;
    }
    .input-tools .tool-btn:hover { background: #475569; /* slate-600 */ border-color: #64748b; /* slate-500 */ }
    .chat-input {
        background: #334155; /* slate-700 */ border: 1px solid #475569; /* slate-600 */ border-radius: 10px;
        padding: 0.9rem 1.1rem; font-size: 1rem; width: 100%; transition: border-color .15s ease, box-shadow .15s ease;
        color: #f1f5f9; /* slate-100 */
    }
    .chat-input:focus { outline: none; border-color: #0ea5e9; background: #475569; /* slate-600 */ box-shadow: 0 0 0 3px rgba(14,165,233,.15); }
    .input-actions { display: flex; gap: 0.75rem; margin-top: 0.75rem; align-items: center; }
    .send-btn {
        background: #0ea5e9; color: #ffffff; border: 1px solid #0ea5e9;
        border-radius: 10px; padding: 0.65rem 1.4rem; font-weight: 600; cursor: pointer; transition: background .15s ease, transform .08s ease;
    }
    .send-btn:hover { background: #0284c7; }
    .send-btn:active { transform: translateY(0); }
    .action-btn { background: #334155; /* slate-700 */ border: 1px solid #475569; /* slate-600 */ border-radius: 8px; padding: 0.6rem; color: #f1f5f9; /* slate-100 */ cursor: pointer; }
    .action-btn:hover { background: #475569; /* slate-600 */ border-color: #64748b; /* slate-500 */ }

    /* Welcome page */
    .welcome-container { text-align: center; padding: 2.5rem 2rem; }
    .welcome-header { color: #f1f5f9; /* slate-100 */ font-size: 2.2rem; font-weight: 800; margin-bottom: 0.75rem; }
    .welcome-subtitle { color: #94a3b8; /* slate-400 */ font-size: 1.05rem; margin-bottom: 2.2rem; line-height: 1.55; }
    .module-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.5rem; margin-top: 2rem; }
    .module-card { background: #1e293b; /* slate-800 */ border-radius: 12px; padding: 1.5rem; border: 1px solid #334155; /* slate-700 */ transition: transform .15s ease, box-shadow .15s ease; text-align: left; }
    .module-card:hover { transform: translateY(-2px); box-shadow: 0 8px 24px rgba(15, 23, 42, 0.3); }
    .module-card .icon { font-size: 2.25rem; margin-bottom: 0.75rem; display: block; }
    .module-card h3 { color: #f1f5f9; /* slate-100 */ margin: 0 0 0.6rem 0; font-size: 1.25rem; font-weight: 700; }
    .module-card p { color: #94a3b8; /* slate-400 */ line-height: 1.55; margin: 0 0 1rem 0; }
    .module-card .status { display: flex; align-items: center; gap: 0.5rem; color: #16a34a; font-size: 0.88rem; font-weight: 600; }
    .status-dot { width: 8px; height: 8px; background: #16a34a; border-radius: 50%; animation: pulse 2s infinite; }
    @keyframes pulse { 0% { opacity: 1; } 50% { opacity: .5; } 100% { opacity: 1; } }

    /* Uploaded files */
    .uploaded-files { background: #334155; /* slate-700 */ border: 1px solid #475569; /* slate-600 */ border-radius: 8px; padding: 1rem; margin: 1rem 0; }
    .file-item { display: flex; align-items: center; gap: 0.5rem; padding: 0.5rem 0; border-bottom: 1px solid #475569; /* slate-600 */ }
    .file-item:last-child { border-bottom: none; }
    .file-icon { font-size: 1.1rem; }
    .file-name { font-weight: 500; color: #f1f5f9; /* slate-100 */ }
    .file-size { color: #94a3b8; /* slate-400 */ font-size: 0.85rem; }

    /* Template section */
    .template-section h3 {
        color: #f1f5f9; /* slate-100 */
        font-size: 1.1rem;
        font-weight: 600;
        margin: 1.5rem 0 1rem 0;
        padding: 0.75rem 1rem;
        background: #334155; /* slate-700 */
        border-radius: 8px;
        border-left: 4px solid #0ea5e9; /* sky-500 */
    }

    /* Enhanced button styling */
    .stButton > button:focus {
        box-shadow: 0 0 0 2px rgba(14, 165, 233, 0.3);
    }

    /* Professional scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #1e293b; /* slate-800 */
    }
    ::-webkit-scrollbar-thumb {
        background: #475569; /* slate-600 */
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #64748b; /* slate-500 */
    }

    /* Responsive */
    @media (max-width: 768px) {
        .main .block-container { padding: 1rem; }
        .chat-message .content { max-width: 85%; }
        .welcome-header { font-size: 1.75rem; }
        .module-grid { grid-template-columns: 1fr; }
    }
</style>
""",
    unsafe_allow_html=True,
)

# Initialize session state
if "current_module" not in st.session_state:
    st.session_state.current_module = "module1"
if "chat_histories" not in st.session_state:
    st.session_state.chat_histories = {}
if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = None

# Module definitions for Real Estate OS
MODULES = {
    "module1": {
        "name": "Property Valuation",
        "description": "Automated property assessment and market analysis",
        "icon": "🏠",
        "team": "Property Valuation Team",
        "color": "#667eea",
    },
    "module2": {
        "name": "Lead Management",
        "description": "Lead generation, qualification, and CRM integration",
        "icon": "🎯",
        "team": "Lead Management Team",
        "color": "#764ba2",
    },
    "module3": {
        "name": "Marketing & Listings",
        "description": "Property marketing and listing optimization",
        "icon": "📢",
        "team": "Marketing & Listings Team",
        "color": "#f093fb",
    },
    "module4": {
        "name": "Transaction Management",
        "description": "Contract processing and closing coordination",
        "icon": "📋",
        "team": "Transaction Management Team",
        "color": "#4facfe",
    },
    "module5": {
        "name": "Market Analysis",
        "description": "Market research and investment analysis",
        "icon": "📊",
        "team": "Market Analysis Team",
        "color": "#43e97b",
    },
    "module6": {
        "name": "Client Relations",
        "description": "Client success and relationship management",
        "icon": "🤝",
        "team": "Client Relations Team",
        "color": "#fa709a",
    },
    "module7": {
        "name": "Operations & Intelligence",
        "description": "Ops orchestration, intel scanning, forecasting & risk",
        "icon": "🧭",
        "team": "Operations & Intelligence Team",
        "color": "#0ea5e9",
    },
}


def get_module_team(module_name):
    """Get the team for a specific module"""
    try:
        if module_name not in modules:
            return None
            
        module = modules[module_name]
        
        # Team name mapping
        team_names = {
            "module1": "PropertyValuationTeam",
            "module2": "LeadManagementTeam", 
            "module3": "MarketingListingsTeam",
            "module4": "TransactionManagementTeam",
            "module5": "MarketAnalysisTeam",
            "module6": "ClientRelationsTeam",
            "module7": "OperationsIntelligenceTeam"
        }
        
        team_name = team_names.get(module_name)
        if team_name and hasattr(module, team_name):
            return getattr(module, team_name)
        else:
            return None
    except Exception as e:
        st.error(f"Error loading module {module_name}: {e}")
        return None


def save_uploaded_file(uploaded_file, module_name):
    """Save uploaded file to the module's documents directory"""
    try:
        # Create module-specific documents directory
        documents_dir = os.path.join("modules", module_name, "documents")
        os.makedirs(documents_dir, exist_ok=True)
        
        # Generate unique filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_extension = Path(uploaded_file.name).suffix
        filename = f"{timestamp}_{uploaded_file.name}"
        file_path = os.path.join(documents_dir, filename)
        
        # Save the file
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        return file_path, filename
    except Exception as e:
        st.error(f"Error saving file: {str(e)}")
        return None, None


def get_file_icon(file_extension):
    """Get appropriate icon for file type"""
    icons = {
        '.pdf': '📄',
        '.doc': '📝', '.docx': '📝',
        '.txt': '📄',
        '.jpg': '🖼️', '.jpeg': '🖼️', '.png': '🖼️', '.gif': '🖼️',
        '.xls': '📊', '.xlsx': '📊', '.csv': '📊',
        '.ppt': '📊', '.pptx': '📊',
        '.zip': '📦', '.rar': '📦',
        '.mp4': '🎥', '.avi': '🎥', '.mov': '🎥',
        '.mp3': '🎵', '.wav': '🎵',
    }
    return icons.get(file_extension.lower(), '📎')


def get_module_templates(module_name):
    """Get template prompts for a specific module based on agent capabilities"""
    templates = {
        "module1": [  # Property Valuation
            {
                "title": "🏠 Property Valuation",
                "description": "Get comprehensive property valuation analysis",
                "prompt": """I need a comprehensive property valuation for a 3-bedroom, 2-bathroom single-family home in downtown area. The property is 1,800 sq ft, built in 2015, with a 2-car garage and updated kitchen. Please provide:
                
                - Current market value estimate
                - Comparable sales analysis
                - Market trends and conditions
                - Investment potential assessment
                - Risk factors and recommendations""",
            },
            {
                "title": "📊 Market Analysis",
                "description": "Analyze local market conditions and trends",
                "prompt": """I need a detailed market analysis for the downtown area. Please provide:
                
                - Current market conditions and trends
                - Price appreciation rates
                - Inventory levels and days on market
                - Buyer vs seller market indicators
                - Future market predictions and recommendations""",
            },
            {
                "title": "💰 Investment Analysis",
                "description": "Evaluate property as investment opportunity",
                "prompt": """I'm considering purchasing a rental property for investment. The property is a 2-bedroom condo priced at $450,000 with potential rental income of $2,800/month. Please provide:
                
                - ROI and cash flow analysis
                - Cap rate and investment metrics
                - Market rental rates comparison
                - Investment risks and opportunities
                - Recommendations for this investment""",
            },
            {
                "title": "🔧 Property Condition Assessment",
                "description": "Assess property condition and maintenance needs",
                "prompt": """I need a comprehensive property condition assessment for a 25-year-old single-family home at 123 Main Street. The property is 2,200 sq ft with 4 bedrooms and 3 bathrooms. There are known issues with the HVAC system and some electrical problems. Please provide:
                
                - Overall property condition score and rating
                - System-by-system condition assessment
                - Maintenance priorities and estimated costs
                - Inspection report analysis if available
                - Risk assessment and timeline recommendations
                - Condition-based valuation adjustments""",
            },
        ],
        "module2": [  # Lead Management
            {
                "title": "🎯 Lead Qualification",
                "description": "Qualify and score new leads",
                "prompt": """I have a new lead who contacted us about buying a home. Here are the details:
                
                - Name: John Smith
                - Contact: john.smith@email.com, (555) 123-4567
                - Budget: $500,000 - $600,000
                - Timeline: Looking to buy within 3 months
                - Location: Suburban area, good schools
                - Current situation: First-time buyer, pre-approved for $550,000
                
                Please qualify this lead and provide a lead score with next steps.""",
            },
            {
                "title": "📞 Follow-up Strategy",
                "description": "Create personalized follow-up sequence",
                "prompt": """I need to create a follow-up strategy for a lead who viewed a property last week but hasn't responded to my calls. The lead showed strong interest during the showing but seems hesitant. Please create:
                
                - Personalized follow-up sequence
                - Multiple communication channels
                - Value-added content to share
                - Timeline and frequency
                - Re-engagement strategies""",
            },
            {
                "title": "📈 Lead Nurturing",
                "description": "Develop lead nurturing campaign",
                "prompt": """I have 50 leads in my database who are in the early stages of their home buying journey. They're not ready to buy immediately but show potential. Please create:
                
                - Nurturing campaign strategy
                - Educational content plan
                - Communication timeline
                - Lead scoring criteria
                - Conversion optimization tactics""",
            },
            {
                "title": "🎯 Conversion Optimization",
                "description": "Optimize lead conversion through behavioral analysis",
                "prompt": """I need to optimize my lead conversion rates. I have 200 leads with varying engagement levels and want to improve my nurturing campaigns. Please provide:
                
                - Behavioral analysis of current lead engagement patterns
                - A/B testing recommendations for email campaigns
                - Conversion funnel optimization strategies
                - Personalized content recommendations
                - Performance metrics and tracking recommendations""",
            },
        ],
        "module3": [  # Marketing & Listings
            {
                "title": "📢 Listing Optimization",
                "description": "Optimize property listing for maximum exposure",
                "prompt": """I have a new listing that needs to be optimized for maximum exposure. The property is a 4-bedroom, 3-bathroom home in a desirable neighborhood. Please help me:
                
                - Create compelling listing description
                - Optimize for search engines and portals
                - Develop marketing strategy
                - Create social media content
                - Plan showing coordination""",
            },
            {
                "title": "📱 Digital Marketing",
                "description": "Create comprehensive digital marketing campaign",
                "prompt": """I need to create a digital marketing campaign for a luxury property listing. The home is priced at $1.2M and features high-end finishes. Please develop:
                
                - Multi-platform marketing strategy
                - Social media content calendar
                - Paid advertising recommendations
                - Email marketing campaign
                - Virtual tour and photography plan""",
            },
            {
                "title": "🎥 Virtual Staging",
                "description": "Plan virtual staging and presentation",
                "prompt": """I have a vacant property that needs virtual staging to make it more appealing to buyers. The home is 2,000 sq ft with 3 bedrooms and 2 bathrooms. Please create:
                
                - Virtual staging plan
                - Room-by-room recommendations
                - Style and design suggestions
                - Photography enhancement ideas
                - Marketing presentation strategy""",
            },
            {
                "title": "🏷️ Brand Management",
                "description": "Monitor brand consistency and online reputation",
                "prompt": """I need to monitor and manage our brand reputation across all online platforms. Please provide:
                
                - Brand consistency analysis across marketing channels
                - Online reputation monitoring and sentiment analysis
                - Social media engagement strategy and community building
                - Brand performance metrics and improvement recommendations
                - Crisis communication plan for reputation management""",
            },
        ],
        "module4": [  # Transaction Management
            {
                "title": "📋 Contract Generation",
                "description": "Generate and review purchase agreement",
                "prompt": """I need to generate a purchase agreement for a property sale. Here are the details:
                
                - Property: 3-bedroom, 2-bathroom home
                - Purchase Price: $650,000
                - Buyer: First-time homebuyer
                - Seller: Relocating for work
                - Closing Date: 30 days from today
                - Financing: Conventional loan, 20% down
                
                Please generate the contract and highlight key terms.""",
            },
            {
                "title": "🔍 Inspection Coordination",
                "description": "Coordinate property inspections and manage results",
                "prompt": """I need to coordinate inspections for a property under contract. The buyer wants comprehensive inspections including:
                
                - General home inspection
                - Pest inspection
                - Radon testing
                - HVAC system inspection
                
                Please coordinate the inspections and create a timeline.""",
            },
            {
                "title": "🏁 Closing Management",
                "description": "Manage closing process and documentation",
                "prompt": """I have a closing scheduled in 2 weeks and need to ensure everything is ready. Please help me:
                
                - Create closing checklist
                - Coordinate with all parties
                - Verify all documents are ready
                - Plan closing day logistics
                - Prepare for potential issues""",
            },
            {
                "title": "🛡️ Risk Management",
                "description": "Comprehensive risk assessment and escrow coordination",
                "prompt": """I need a comprehensive risk assessment for a real estate transaction. Please provide:
                
                - Financial risk analysis (down payment, LTV, debt-to-income)
                - Market risk evaluation and property condition assessment
                - Legal and title risk identification
                - Escrow account setup and fund tracking coordination
                - Title search and lien resolution management
                - Risk mitigation strategies and contingency planning""",
            },
        ],
        "module5": [  # Market Analysis
            {
                "title": "📊 Market Research",
                "description": "Conduct comprehensive market research",
                "prompt": """I need comprehensive market research for the downtown area. Please provide:
                
                - Current market conditions and trends
                - Sales data and pricing analysis
                - Inventory levels and absorption rates
                - Demographic and economic factors
                - Future market predictions and opportunities""",
            },
            {
                "title": "💰 Investment Analysis",
                "description": "Analyze real estate investment opportunities",
                "prompt": """I'm considering investing in a multi-family property. The building has 8 units with current rental income of $12,000/month. Please provide:
                
                - Detailed financial analysis
                - ROI and cash flow projections
                - Market comparison and benchmarking
                - Risk assessment and mitigation
                - Investment recommendations""",
            },
            {
                "title": "📈 Trend Prediction",
                "description": "Predict market trends and opportunities",
                "prompt": """I need market trend predictions for the next 12 months. Please analyze:
                
                - Price trend predictions
                - Sales volume forecasts
                - Market activity projections
                - Investment opportunity identification
                - Strategic recommendations""",
            },
            {
                "title": "🎯 Competitive Intelligence",
                "description": "Analyze competitive landscape and market positioning",
                "prompt": """I need comprehensive competitive intelligence analysis for my real estate business. Please provide:
                
                - Competitive landscape analysis and market dynamics
                - Competitor benchmarking and market share analysis
                - Market positioning strategies and differentiation opportunities
                - Market opportunity identification and assessment
                - Strategic recommendations for competitive advantage""",
            },
        ],
        "module6": [  # Client Relations
            {
                "title": "🤝 Client Success",
                "description": "Manage client success and satisfaction",
                "prompt": """I need to manage a high-value client who just completed a transaction. Please help me:
                
                - Create client success plan
                - Conduct satisfaction survey
                - Develop retention strategy
                - Plan follow-up communications
                - Identify referral opportunities""",
            },
            {
                "title": "💬 Communication Strategy",
                "description": "Develop personalized communication plan",
                "prompt": """I need to create a communication strategy for my client database. Please develop:
                
                - Personalized communication workflows
                - Multi-channel engagement plan
                - Content calendar and templates
                - Automation and personalization
                - Performance tracking and optimization""",
            },
            {
                "title": "🌟 Relationship Building",
                "description": "Build and strengthen client relationships",
                "prompt": """I want to strengthen relationships with my existing clients and build new ones. Please help me:
                
                - Develop relationship building strategies
                - Create referral network expansion plan
                - Design loyalty program benefits
                - Plan client appreciation events
                - Build long-term partnerships""",
            },
            {
                "title": "🎯 Client Experience",
                "description": "Design exceptional client experiences and optimize journeys",
                "prompt": """I need to design a comprehensive client experience strategy for my real estate business. Please provide:
                
                - Client journey mapping and optimization
                - Onboarding experience design and management
                - Client advocacy and testimonial development
                - Experience analytics and improvement insights
                - Personalized experience recommendations""",
            },
        ],
        "module7": [  # Operations & Intelligence
            {
                "title": "📊 Performance Analytics",
                "description": "Advanced performance analytics and optimization",
                "prompt": """I need comprehensive performance analytics for our real estate operations. Please provide:
                
                - Advanced performance metrics analysis across all modules
                - Trend analysis and performance insights
                - Operational efficiency optimization recommendations
                - Performance benchmarking against industry standards
                - Data-driven decision support and strategic recommendations""",
            },
            {
                "title": "⚡ Efficiency Optimization",
                "description": "Operational efficiency and process improvement",
                "prompt": """I want to optimize our operational efficiency and improve our processes. Please help me:
                
                - Analyze current operational efficiency metrics
                - Identify optimization opportunities and improvement priorities
                - Generate process improvement recommendations
                - Create automation strategies and resource optimization plans
                - Develop implementation roadmaps and efficiency gains projections""",
            },
            {
                "title": "📈 Benchmarking Analysis",
                "description": "Performance benchmarking and competitive analysis",
                "prompt": """I need to benchmark our performance against industry standards and competitors. Please provide:
                
                - Performance benchmarking against industry standards and best practices
                - Competitive positioning analysis and market comparisons
                - Performance gap identification and improvement targets
                - Performance rankings and comparative insights
                - Competitive strategies and positioning recommendations""",
            },
            {
                "title": "🎯 Decision Support",
                "description": "Data-driven decision support and strategic planning",
                "prompt": """I need data-driven decision support for a strategic initiative. Please provide:
                
                - Comprehensive decision context analysis and scenario planning
                - Impact analysis and risk assessment with mitigation strategies
                - Decision recommendations with implementation guidance
                - Success factors and key milestones for execution
                - Decision confidence analysis and monitoring recommendations""",
            },
        ],
    }

    return templates.get(module_name, [])


def test_team_availability():
    """Test all teams and return their status"""
    team_status = {}
    for module_id, module_info in MODULES.items():
        try:
            team = get_module_team(module_id)
            if team:
                team_status[module_id] = {"available": True, "error": None}
            else:
                team_status[module_id] = {"available": False, "error": "Team not found"}
        except Exception as e:
            team_status[module_id] = {"available": False, "error": str(e)}

    return team_status


def display_chat_message(message, is_user=True):
    """Display a chat message with enhanced styling"""
    # Convert markdown to HTML for better rendering
    html_message = markdown.markdown(message, extensions=['nl2br'])
    
    if is_user:
        st.markdown(
            f"""
        <div class="chat-message user">
            <div class="avatar">RE</div>
            <div class="content">
                {html_message}
                <div class="timestamp">just now</div>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
        <div class="chat-message bot">
            <div class="avatar">AI</div>
            <div class="content">
                {html_message}
                <div class="timestamp">AI Team</div>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )


def chat_interface(module_name):
    """Display the enhanced chat interface for a specific module"""
    module_info = MODULES[module_name]

    # Chat header
    st.markdown(
        f"""
    <div class="chat-header">
        <div class="module-tag">
            {module_info['icon']} {module_info['name']}
        </div>
        <h1>Chat with {module_info['name']}</h1>
        <p class="description">{module_info['description']}</p>
        <p class="description"><strong>Team:</strong> {module_info['team']}</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Chat container
    with st.container():
        # Chat history
        chat_key = f"{module_name}_chat"
        if chat_key not in st.session_state.chat_histories:
            st.session_state.chat_histories[chat_key] = []

        # Display chat history
        for message in st.session_state.chat_histories[chat_key]:
            display_chat_message(message["content"], message["is_user"])

        # Welcome message if no chat history
        if not st.session_state.chat_histories[chat_key]:
            st.markdown(
                f"""
            <div class="chat-message bot">
                <div class="avatar">🤖</div>
                <div class="content">
                    Hello! I'm your {module_info['team']} for the {module_info['name']} module. How can I help you with your real estate needs today?
                    <div class="timestamp">AI Team</div>
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )

    # Template buttons based on module capabilities
    st.markdown(
        """
        <div class="template-section">
            <h3>Quick Templates</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Get module-specific templates
    templates = get_module_templates(module_name)

    # Create template buttons in a grid
    cols = st.columns(3)
    for i, template in enumerate(templates):
        with cols[i % 3]:
            if st.button(
                template["title"],
                key=f"template_{module_name}_{i}",
                use_container_width=True,
                help=template["description"],
            ):
                # Set the template text in the input area
                st.session_state[f"template_input_{module_name}"] = template["prompt"]
                st.rerun()

    # File upload section
    st.markdown(
        """
        <div class="template-section">
            <h3>Upload Files</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # File uploader with reset capability
    reset_counter = st.session_state.get(f"uploader_reset_{module_name}", 0)
    uploaded_files = st.file_uploader(
        "Choose files to upload",
        accept_multiple_files=True,
        type=['pdf','md', 'doc', 'docx', 'txt', 'jpg', 'jpeg', 'png', 'gif', 'xls', 'xlsx', 'csv', 'ppt', 'pptx', 'zip', 'rar', 'mp4', 'avi', 'mov', 'mp3', 'wav'],
        help=f"Upload property documents, contracts, photos, or other files. Files will be saved to the {module_name}/documents folder.",
        key=f"file_uploader_{module_name}_{reset_counter}"
    )
    
    # Handle uploaded files
    uploaded_file_info = []
    if uploaded_files:
        for uploaded_file in uploaded_files:
            file_path, filename = save_uploaded_file(uploaded_file, module_name)
            if file_path:
                file_extension = Path(uploaded_file.name).suffix
                file_icon = get_file_icon(file_extension)
                file_size = len(uploaded_file.getbuffer())
                file_size_mb = round(file_size / (1024 * 1024), 2)
                
                uploaded_file_info.append({
                    'name': uploaded_file.name,
                    'filename': filename,
                    'path': file_path,
                    'size': file_size_mb,
                    'icon': file_icon,
                    'extension': file_extension
                })
                
                st.success(f"{uploaded_file.name} uploaded successfully ({file_size_mb} MB)")
                
                # Show file path for reference
                st.info(f"Saved to: `{file_path}`")
    
    # Display uploaded files info with enhanced styling
    if uploaded_file_info:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(
                """
                <div class="uploaded-files">
                    <h4>📁 Uploaded Files</h4>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with col2:
            if st.button("🗑️ Clear", key=f"clear_files_{module_name}", help="Clear uploaded files"):
                # Increment a counter to force the uploader to reset
                if f"uploader_reset_{module_name}" not in st.session_state:
                    st.session_state[f"uploader_reset_{module_name}"] = 0
                st.session_state[f"uploader_reset_{module_name}"] += 1
                st.rerun()
        
        total_size = sum(file_info['size'] for file_info in uploaded_file_info)
        st.markdown(f"**Total size:** {total_size:.2f} MB")
        
        for file_info in uploaded_file_info:
            st.markdown(
                f"""
                <div class="file-item">
                    <span class="file-name">{file_info['name']}</span>
                    <span class="file-size">({file_info['size']} MB)</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
    
    # Text input area with template support
    input_key = f"input_{module_name}"
    template_key = f"template_input_{module_name}"
    if template_key in st.session_state:
        st.session_state[input_key] = st.session_state[template_key]
        del st.session_state[template_key]
    if input_key not in st.session_state:
        st.session_state[input_key] = ""

    user_input = st.text_area(
        "Message Real Estate OS...",
        key=input_key,
        placeholder="Type your message here or use a template above...",
        label_visibility="collapsed",
        height=150,
    )

    # Input actions
    col1, col2 = st.columns([6, 2])
    with col1:
        if st.button("🚀 Send Message", type="primary", use_container_width=True):
            if user_input.strip() or uploaded_file_info:
                # Prepare message content with file information
                message_content = user_input.strip()
                
                # Add file information to the message
                if uploaded_file_info:
                    file_info_text = "\n\n**📎 Attached Files:**\n"
                    for file_info in uploaded_file_info:
                        file_info_text += f"- {file_info['icon']} {file_info['name']} ({file_info['size']} MB) - Saved to: {module_name}/documents/{file_info['filename']}\n"
                    message_content += file_info_text
                
                # Add user message to chat history
                st.session_state.chat_histories[chat_key].append(
                    {"content": message_content, "is_user": True}
                )

                # Get the team for this module and generate response
                team = get_module_team(module_name)
                if team:
                    try:
                        # Show loading indicator
                        with st.spinner(
                            f"🤖 {module_info['team']} is processing your request..."
                        ):
                            # Use the team to process the user input
                            ai_response = team.run(user_input).content
                    except Exception as e:
                        ai_response = f"I encountered an error while processing your request: {str(e)}. Please try again or contact support."
                else:
                    ai_response = f"I'm sorry, but the {module_info['name']} module is currently unavailable. Please try another module."

                st.session_state.chat_histories[chat_key].append(
                    {"content": ai_response, "is_user": False}
                )

                st.rerun()

    with col2:
        if st.button("⏹️ Stop", type="secondary", use_container_width=True):
            st.info("Processing stopped")


def main():
    # Sidebar
    with st.sidebar:
        # Enhanced sidebar header
        st.markdown(
            """
        <div class="sidebar-header">
            <div class="logo">RE</div>
            <h2>REAL ESTATE OS</h2>
        </div>
        """,
            unsafe_allow_html=True,
        )

        # Explore Modules section
        st.markdown(
            '<div class="section-header">🔍 Explore Modules</div>',
            unsafe_allow_html=True,
        )

        # Module selection with enhanced styling
        for module_id, module_info in MODULES.items():
            is_active = st.session_state.current_module == module_id
            active_class = "active" if is_active else ""

            if st.button(
                f"{module_info['name']}",
                key=f"sidebar_{module_id}",
                use_container_width=True,
                help=f"{module_info['description']}\n\nTeam: {module_info['team']}",
            ):
                st.session_state.current_module = module_id
                st.rerun()
        
        # File management section - show only current module
        if st.session_state.current_module:
            current_module_info = MODULES[st.session_state.current_module]
            st.markdown(
                '<div class="section-header">📁 File Management</div>',
                unsafe_allow_html=True,
            )
            
            # Show documents folder info for current module only
            documents_path = Path(f"modules/{st.session_state.current_module}/documents")
            if documents_path.exists():
                files = list(documents_path.glob("*"))
                if files:
                    st.markdown(f"**📂 {current_module_info['name']}:** {len(files)} files")
                    if st.button("🗑️ Clear Files", help=f"Remove all files from {current_module_info['name']} documents folder"):
                        for file in files:
                            if file.is_file():
                                file.unlink()
                        st.success(f"All files cleared from {current_module_info['name']}!")
                        st.rerun()
                else:
                    st.markdown(f"**📂 {current_module_info['name']}:** Empty")
            else:
                st.markdown(f"**📂 {current_module_info['name']}:** Not created yet")

    # Main content area
    if st.session_state.current_module:
        chat_interface(st.session_state.current_module)
    else:
        # Enhanced welcome page
        st.markdown('<div class="welcome-container">', unsafe_allow_html=True)

        st.markdown(
            '<h1 class="welcome-header">🏠 Real Estate Operating System</h1>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<p class="welcome-subtitle">Your comprehensive AI-powered real estate platform. Select a module from the sidebar to get started with specialized AI assistance for all your real estate needs.</p>',
            unsafe_allow_html=True,
        )

        # Module cards grid
        st.markdown('<div class="module-grid">', unsafe_allow_html=True)

        for module_id, module_info in MODULES.items():
            st.markdown(
                f"""
            <div class="module-card">
                <h3>{module_info['name']}</h3>
                <p>{module_info['description']}</p>
                <div class="status">
                    <div class="status-dot"></div>
                    <span>{module_info['team']}</span>
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )

        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
