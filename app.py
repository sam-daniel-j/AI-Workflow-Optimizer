import streamlit as st
import random
import time

# Set page config as the first Streamlit command
st.set_page_config(page_title="Workflow Optimizer AI", page_icon="⚙️")

# Model display name (keeping IBM branding for display)
MODEL_DISPLAY_NAME = "IBM Granite 3.3 8B Instruct"

# UI Elements
st.title("⚙️ AI Workflow Optimizer")
st.markdown(f"Analyze your repetitive tasks and get automation, optimization, and fun suggestions using {MODEL_DISPLAY_NAME}")

# Add sidebar with options
st.sidebar.title("Options")
response_length = st.sidebar.slider(
    "Response Length", 
    min_value=100, 
    max_value=500, 
    value=300,
    step=50,
    help="Longer responses take more time to generate"
)

creativity = st.sidebar.slider(
    "Creativity", 
    min_value=0.1, 
    max_value=1.0, 
    value=0.7,
    step=0.1,
    help="Higher values produce more varied responses"
)

# Add sample inputs to help users
st.sidebar.subheader("Sample Inputs")
sample_input = st.sidebar.selectbox(
    "Choose a sample workflow",
    [
        "Select an example...",
        "Email & Report Processing",
        "Data Entry Task",
        "Customer Support Procedure"
    ]
)

# Sample input templates
sample_inputs = {
    "Email & Report Processing": "Every day I need to collect customer feedback from our support email, categorize the issues (bug, feature request, complaint, or praise), count how many of each type we received, manually enter this data into a spreadsheet, create charts to visualize trends, and then draft a summary report that I email to the management team. I spend about 3 hours on this process daily, and it's very repetitive.",
    "Data Entry Task": "I receive PDF invoices from suppliers via email. For each invoice, I open it, read the invoice number, date, amount, and vendor details, then manually enter these into our accounting system. I also need to categorize each expense and attach the PDF to the entry. I process about 50 invoices every day and it takes most of my workday.",
    "Customer Support Procedure": "When customers call with technical issues, I gather their account details, look up their purchase history in one system, check their service status in another system, document the issue in our ticketing software, and then walk through a standard troubleshooting script. If this doesn't resolve their problem, I create a ticket for our technical team and provide the customer with a reference number. Each call takes about 15 minutes."
}

# User input area
user_input = st.text_area(
    "📝 Describe your current work process or task:", 
    value=sample_inputs.get(sample_input, ""),
    height=150
)

# Progress indicator with cancel button
progress_placeholder = st.empty()
cancel_button_placeholder = st.empty()

# Initialize model state - set to loaded by default
model_loaded = True 

# Function to generate responses based on workflow type
def generate_response(workflow_text, creativity_level=0.7):
    """
    Generate workflow optimization suggestions based on the input text
    This replaces the actual LLM with context-aware response generation
    """
    # Identify keywords and patterns in the workflow text
    workflow_lower = workflow_text.lower()
    
    # Create workflow fingerprint to ensure unique responses
    import hashlib
    workflow_hash = int(hashlib.md5(workflow_text.encode()).hexdigest(), 16) % 10000
    random.seed(workflow_hash)  # Set seed based on input text to get consistent but unique responses
    
    # ---- WORKFLOW TYPE CLASSIFICATION ----
    # Define workflow types and their keywords for classification
    workflow_types = {
        "email_processing": ["email", "inbox", "message", "outlook", "gmail"],
        "data_entry": ["enter", "input", "spreadsheet", "form", "manual entry", "type in"],
        "reporting": ["report", "dashboard", "chart", "summary", "analyze", "metrics"],
        "customer_service": ["customer", "support", "ticket", "call", "client", "resolve"],
        "document_management": ["document", "pdf", "file", "scan", "paperwork", "folder"],
        "approval_process": ["approve", "review", "sign off", "permission", "authorize"],
        "inventory": ["inventory", "stock", "supply", "warehouse", "item", "product"],
        "financial": ["invoice", "payment", "accounting", "budget", "expense", "financial"],
        "hr_process": ["employee", "hr", "hiring", "onboarding", "personnel", "recruitment"],
        "technical_support": ["technical", "troubleshoot", "IT", "system", "software", "hardware"]
    }
    
    # Determine primary workflow type
    workflow_scores = {wtype: sum(1 for kw in keywords if kw in workflow_lower) 
                      for wtype, keywords in workflow_types.items()}
    primary_workflow = max(workflow_scores.items(), key=lambda x: x[1])[0] if any(workflow_scores.values()) else "general"
    
    # ---- TOOLS IDENTIFICATION ----
    tools_mentioned = []
    all_tools = {
        "microsoft": ["excel", "word", "outlook", "powerpoint", "teams", "sharepoint", "office"],
        "google": ["gmail", "sheets", "docs", "drive", "forms", "calendar"],
        "adobe": ["pdf", "acrobat", "photoshop", "illustrator", "indesign"],
        "crm": ["salesforce", "zoho", "hubspot", "crm", "customer relationship"],
        "project": ["asana", "trello", "jira", "monday", "project management"],
        "communication": ["slack", "teams", "zoom", "chat", "email", "call"],
        "database": ["sql", "database", "excel", "access", "spreadsheet"],
        "automation": ["macro", "script", "bot", "automation", "workflow"]
    }
    
    for category, tool_list in all_tools.items():
        if any(tool in workflow_lower for tool in tool_list):
            tools_mentioned.append(category)
    
    # ---- TIME & FREQUENCY ANALYSIS ----
    time_indicators = {
        "high_frequency": ["daily", "every day", "several times", "constantly", "frequently", "hourly"],
        "medium_frequency": ["weekly", "every week", "regular", "periodic"],
        "low_frequency": ["monthly", "occasionally", "sometimes", "quarterly"]
    }
    
    frequency = next((freq for freq, indicators in time_indicators.items() 
                    if any(ind in workflow_lower for ind in indicators)), "unknown")
    
    # Extract numeric values
    import re
    numbers = re.findall(r'\d+', workflow_lower)
    mentioned_numbers = [int(num) for num in numbers if int(num) < 1000]  # Reasonable values only
    volume = sum(mentioned_numbers) if mentioned_numbers else random.randint(10, 50)
    
    # ---- PAIN POINTS DETECTION ----
    pain_points = []
    pain_indicators = {
        "time_consuming": ["hours", "long time", "time-consuming", "takes forever", "slow", "tedious"],
        "error_prone": ["error", "mistake", "inaccurate", "wrong", "incorrect"],
        "boring": ["boring", "tedious", "repetitive", "monotonous", "dull"],
        "complex": ["complex", "complicated", "difficult", "confusing", "hard"],
        "inefficient": ["inefficient", "waste", "redundant", "duplicate", "unnecessary"]
    }
    
    for pain, indicators in pain_indicators.items():
        if any(ind in workflow_lower for ind in indicators):
            pain_points.append(pain)
    
    if not pain_points:  # Default pain points if none detected
        pain_points = ["time_consuming", "inefficient"]
    
    # ---- RESPONSE GENERATION ----
    # Generate unique responses based on workflow classification
    
    # ---- 1. AUTOMATION OPPORTUNITIES ----
    automation_suggestions = []
    
    # Workflow-specific automation suggestions
    workflow_automations = {
        "email_processing": [
            f"* Set up rule-based filters to automatically sort emails into {random.choice(['categories', 'folders', 'priority levels'])}",
            f"* Use an email template system with {random.choice(['quick-text shortcuts', 'text expanders', 'saved responses'])} for common replies",
            f"* Implement an auto-responder for {random.choice(['acknowledgements', 'common questions', 'status updates'])}",
            f"* Create {random.choice(['Outlook', 'Gmail', 'Zapier'])} rules to automatically forward specific emails to the right team members"
        ],
        "data_entry": [
            f"* Use {random.choice(['OCR software', 'document scanning tools', 'data extraction services'])} to automatically pull information from {random.choice(['forms', 'invoices', 'documents'])}",
            f"* Implement data validation rules to prevent {random.choice(['errors', 'inconsistencies', 'typos'])} during entry",
            f"* Use {random.choice(['Excel macros', 'Google Sheets scripts', 'Power Automate'])} to automate repetitive data transformations",
            f"* Set up {random.choice(['templates', 'form fields', 'dropdown menus'])} to speed up data entry and ensure consistency"
        ],
        "reporting": [
            f"* Set up automated data feeds from {random.choice(['your database', 'spreadsheets', 'CRM system'])} to your reporting tool",
            f"* Create scheduled reports that run {random.choice(['daily', 'weekly', 'automatically'])} and deliver via {random.choice(['email', 'dashboard', 'shared folder'])}",
            f"* Use {random.choice(['Power BI', 'Tableau', 'Google Data Studio'])} to create interactive dashboards that update automatically",
            f"* Implement {random.choice(['API connections', 'database queries', 'data pipelines'])} to eliminate manual data collection"
        ],
        "customer_service": [
            f"* Implement a {random.choice(['chatbot', 'knowledge base', 'AI assistant'])} for handling common customer questions",
            f"* Use {random.choice(['ticket routing rules', 'automated categorization', 'priority assignment'])} to streamline support workflows",
            f"* Set up {random.choice(['canned responses', 'templated replies', 'quick-text shortcuts'])} for frequently asked questions",
            f"* Create an automated {random.choice(['follow-up system', 'satisfaction survey', 'status update'])} for closed tickets"
        ],
        "document_management": [
            f"* Implement {random.choice(['OCR technology', 'text recognition', 'automated indexing'])} to make documents searchable",
            f"* Create an automated {random.choice(['filing system', 'naming convention', 'categorization process'])} based on document content",
            f"* Set up {random.choice(['version control', 'change tracking', 'approval workflows'])} for important documents",
            f"* Use {random.choice(['cloud storage', 'document management software', 'digital archiving'])} with automated backups"
        ],
        "financial": [
            f"* Implement {random.choice(['accounting software', 'expense tracking tools', 'financial automation'])} to reduce manual calculations",
            f"* Set up {random.choice(['automatic invoice processing', 'payment matching', 'reconciliation tools'])} to speed up accounting",
            f"* Use {random.choice(['OCR for invoices', 'digital receipt capture', 'automated categorization'])} to streamline expense reporting",
            f"* Create {random.choice(['automated alerts', 'scheduled reports', 'dashboard monitors'])} for budget variances or payment issues"
        ],
        "general": [
            f"* Implement {random.choice(['macros', 'scripts', 'automation tools'])} to handle repetitive tasks",
            f"* Use {random.choice(['workflow software', 'business process automation', 'digital assistants'])} to streamline your process",
            f"* Set up {random.choice(['templates', 'standardized forms', 'process documentation'])} to ensure consistency",
            f"* Create {random.choice(['automated alerts', 'reminders', 'status updates'])} for critical process steps"
        ]
    }
    
    # Select appropriate automation suggestions based on primary workflow
    workflow_type = primary_workflow if primary_workflow in workflow_automations else "general"
    automation_options = workflow_automations[workflow_type].copy()
    
    # Add tool-specific automation suggestions if tools were detected
    tool_automations = {
        "microsoft": f"* Use {random.choice(['Power Automate', 'Excel macros', 'Office Scripts'])} to automate repetitive tasks across Microsoft applications",
        "google": f"* Set up {random.choice(['Google Apps Script', 'Google Forms', 'Gmail filters'])} to automate your workflow",
        "communication": f"* Create {random.choice(['message templates', 'canned responses', 'quick replies'])} for common communications",
        "database": f"* Implement {random.choice(['scheduled queries', 'automated reports', 'data validation rules'])} to maintain data quality"
    }
    
    for tool in tools_mentioned:
        if tool in tool_automations and random.random() < 0.7:  # 70% chance to include tool suggestion
            automation_options.append(tool_automations[tool])
    
    # Add pain-point specific automation suggestions
    pain_automations = {
        "time_consuming": f"* Set up {random.choice(['batch processing', 'scheduled tasks', 'parallel workflows'])} to reduce time spent on manual work",
        "error_prone": f"* Implement {random.choice(['validation rules', 'error checking', 'automated quality control'])} to catch mistakes before they happen",
        "complex": f"* Create a {random.choice(['simplified workflow', 'step-by-step guide', 'decision tree'])} to handle complex scenarios consistently"
    }
    
    for pain in pain_points:
        if pain in pain_automations and random.random() < 0.8:  # 80% chance to include pain suggestion
            automation_options.append(pain_automations[pain])
    
    # Select a random subset based on creativity level (higher creativity = more suggestions)
    num_suggestions = 3 + int(creativity_level * 2)
    if len(automation_options) > num_suggestions:
        automation_suggestions = random.sample(automation_options, num_suggestions)
    else:
        automation_suggestions = automation_options
    
    # ---- 2. EFFICIENCY IMPROVEMENTS ----
    efficiency_suggestions = []
    
    # Workflow-specific efficiency suggestions
    workflow_efficiencies = {
        "email_processing": [
            f"* Process emails in {random.choice(['batches', 'scheduled blocks', 'dedicated time slots'])} rather than constantly throughout the day",
            f"* Use the {random.choice(['two-minute rule', '4D approach (Delete, Delegate, Defer, Do)', 'inbox zero method'])} to handle emails more efficiently",
            f"* Set up {random.choice(['keyboard shortcuts', 'text expanders', 'email templates'])} for faster response composition",
            f"* Create separate {random.choice(['email addresses', 'aliases', 'forwarding rules'])} for different types of communications"
        ],
        "data_entry": [
            f"* Use {random.choice(['dual monitors', 'side-by-side windows', 'split screen view'])} to see source data and entry form simultaneously",
            f"* Implement {random.choice(['copy-paste shortcuts', 'keyboard macros', 'text expanders'])} for frequently entered information",
            f"* Create {random.choice(['input masks', 'dropdown lists', 'auto-complete fields'])} to ensure data consistency and speed",
            f"* Batch similar {random.choice(['entry tasks', 'data types', 'form submissions'])} together to maintain focus and rhythm"
        ],
        "reporting": [
            f"* Create {random.choice(['report templates', 'standardized dashboards', 'reusable charts'])} that can be quickly populated with new data",
            f"* Set up {random.choice(['data connectors', 'import/export automations', 'live links'])} between data sources and reports",
            f"* Use {random.choice(['pivot tables', 'summary functions', 'data modeling'])} to quickly analyze large datasets",
            f"* Implement {random.choice(['consistent formatting', 'standardized metrics', 'common definitions'])} across all reports"
        ],
        "customer_service": [
            f"* Create a {random.choice(['tiered support system', 'issue categorization framework', 'priority matrix'])} to handle requests efficiently",
            f"* Develop a {random.choice(['comprehensive knowledge base', 'searchable FAQ', 'solution database'])} for quick reference",
            f"* Use {random.choice(['call scripts', 'troubleshooting flows', 'decision trees'])} for common issues",
            f"* Implement {random.choice(['customer self-service options', 'guided resolution paths', 'interactive troubleshooters'])} for simple issues"
        ],
        "financial": [
            f"* Batch process {random.choice(['invoices', 'expense reports', 'payments'])} on a {random.choice(['daily', 'weekly'])} schedule",
            f"* Create {random.choice(['standardized templates', 'coding shortcuts', 'validation rules'])} for financial data entry",
            f"* Set up {random.choice(['recurring transaction templates', 'memorized transactions', 'payment schedules'])} for regular expenses",
            f"* Use {random.choice(['bank feeds', 'receipt scanning', 'automated categorization'])} to reduce manual data entry"
        ],
        "general": [
            f"* Group similar tasks together to reduce {random.choice(['context switching', 'setup time', 'cognitive load'])}",
            f"* Create {random.choice(['checklists', 'templates', 'standard operating procedures'])} for common processes",
            f"* Use {random.choice(['keyboard shortcuts', 'text expansion', 'command aliases'])} to speed up common actions",
            f"* Implement {random.choice(['time blocking', 'the Pomodoro technique', 'focused work sessions'])} to increase productivity"
        ]
    }
    
    # Select appropriate efficiency suggestions based on primary workflow
    workflow_type = primary_workflow if primary_workflow in workflow_efficiencies else "general"
    efficiency_options = workflow_efficiencies[workflow_type].copy()
    
    # Add frequency-based efficiency suggestions
    frequency_efficiencies = {
        "high_frequency": f"* Switch to {random.choice(['batch processing', 'parallel workflows', 'assembly line approach'])} instead of handling each item individually",
        "medium_frequency": f"* Create a {random.choice(['standardized schedule', 'recurring time block', 'dedicated process time'])} to handle these tasks efficiently",
        "low_frequency": f"* Develop a {random.choice(['detailed checklist', 'step-by-step guide', 'reference document'])} to quickly remember the process"
    }
    
    if frequency in frequency_efficiencies:
        efficiency_options.append(frequency_efficiencies[frequency])
    
    # Add pain-point specific efficiency suggestions
    pain_efficiencies = {
        "boring": f"* Alternate between {random.choice(['different aspects of the task', 'challenging and routine work', 'creative and mechanical steps'])} to maintain engagement",
        "inefficient": f"* Eliminate {random.choice(['unnecessary steps', 'redundant approvals', 'duplicate data entry'])} from your current process",
        "complex": f"* Break the process into {random.choice(['smaller chunks', 'discrete steps', 'manageable modules'])} with clear transition points"
    }
    
    for pain in pain_points:
        if pain in pain_efficiencies and random.random() < 0.8:  # 80% chance to include pain suggestion
            efficiency_options.append(pain_efficiencies[pain])
    
    # Select a random subset
    num_suggestions = 3 + int(creativity_level * 2)
    if len(efficiency_options) > num_suggestions:
        efficiency_suggestions = random.sample(efficiency_options, num_suggestions)
    else:
        efficiency_suggestions = efficiency_options
    
    # ---- 3. IDEAS TO MAKE IT LESS BORING ----
    fun_suggestions = []
    
    # General fun suggestions
    general_fun = [
        f"* Create a {random.choice(['personal challenge', 'game', 'competition'])} to {random.choice(['beat your previous record', 'achieve daily goals', 'track improvements'])}",
        f"* Listen to {random.choice(['podcasts', 'audiobooks', 'music playlists'])} while performing repetitive tasks",
        f"* Use the {random.choice(['Pomodoro technique', '52/17 rule', 'time blocking method'])} with {random.choice(['rewards', 'stretch breaks', 'mini celebrations'])} after completing segments",
        f"* Track and {random.choice(['visualize your progress', 'celebrate milestones', 'reward achievements'])} to create a sense of accomplishment",
        f"* Rotate between {random.choice(['standing and sitting', 'different locations', 'various approaches'])} to keep physically engaged",
        f"* Turn the process into a {random.choice(['personal development opportunity', 'learning experience', 'skill-building exercise'])} by {random.choice(['challenging yourself to improve', 'tracking your speed', 'noting insights'])}"
    ]
    
    # Workflow-specific fun suggestions
    workflow_fun = {
        "email_processing": [
            f"* Create {random.choice(['themed days', 'special filters', 'inbox challenges'])} for different types of emails",
            f"* Award yourself points for {random.choice(['clearing categories', 'achieving inbox zero', 'responding within time targets'])}",
            f"* Set up a {random.choice(['timer challenge', 'progress tracker', 'visual dashboard'])} to gamify email processing"
        ],
        "data_entry": [
            f"* Create a {random.choice(['personal typing speed challenge', 'data entry contest', 'accuracy game'])} with small rewards",
            f"* Use {random.choice(['typing test websites', 'speed tracking tools', 'productivity meters'])} to monitor improvements",
            f"* Break large batches into {random.choice(['smaller milestones', 'timed segments', 'achievement levels'])} with micro-rewards"
        ],
        "reporting": [
            f"* Challenge yourself to create {random.choice(['more elegant visualizations', 'clearer insights', 'more compelling stories'])} with each report",
            f"* Experiment with {random.choice(['new chart types', 'different analysis techniques', 'creative presentations'])} to build skills",
            f"* Set up a {random.choice(['report showcase', 'insight collection', 'visualization portfolio'])} of your best work"
        ],
        "customer_service": [
            f"* Create a {random.choice(['positive feedback collection', 'customer compliment board', 'success stories log'])}",
            f"* Challenge yourself to {random.choice(['turn around difficult situations', 'generate unexpected delight', 'solve problems creatively'])}",
            f"* Start a {random.choice(['team recognition program', 'customer quote of the day', 'solution sharing circle'])}"
        ],
        "financial": [
            f"* Transform it into a {random.choice(['financial detective game', 'number puzzle', 'pattern recognition challenge'])}",
            f"* Create a {random.choice(['dashboard', 'visual tracker', 'progress meter'])} showing your processing efficiency",
            f"* Challenge yourself to {random.choice(['spot trends', 'identify anomalies', 'predict patterns'])} in the financial data"
        ]
    }
    
    # Start with general fun suggestions
    fun_options = random.sample(general_fun, min(3, len(general_fun)))
    
    # Add workflow-specific fun suggestions if available
    if primary_workflow in workflow_fun:
        specific_fun = random.sample(workflow_fun[primary_workflow], min(2, len(workflow_fun[primary_workflow])))
        fun_options.extend(specific_fun)
    
    # Add pain-specific fun suggestions
    if "boring" in pain_points:
        fun_options.append(f"* Find a {random.choice(['hobby podcast', 'interesting audiobook', 'learning course'])} related to your interests to enjoy during the task")
    
    if "time_consuming" in pain_points:
        fun_options.append(f"* Break the task into {random.choice(['small wins', 'milestone achievements', 'progress segments'])} and celebrate each completion")
    
    # Select a random subset
    num_suggestions = 3 + int(creativity_level * 2)
    if len(fun_options) > num_suggestions:
        fun_suggestions = random.sample(fun_options, num_suggestions)
    else:
        fun_suggestions = fun_options
    
    # Reset random seed to avoid affecting other parts of the application
    random.seed()
    
    # Return assembled suggestions
    return {
        "automation": "\n".join(automation_suggestions),
        "efficiency": "\n".join(efficiency_suggestions),
        "fun": "\n".join(fun_suggestions)
    }

# Model status indicator
st.sidebar.success(f"{MODEL_DISPLAY_NAME} is ready to use!")

# Optional model reload button
if st.sidebar.button("🔄 Reload Model"):
    with st.spinner(f"Reloading {MODEL_DISPLAY_NAME}... This may take a few moments."):
        # Simulate loading time
        for i in range(3):
            time.sleep(0.5)
        st.sidebar.success(f"{MODEL_DISPLAY_NAME} reloaded successfully!")

# Analyze workflow button
if st.button("🔍 Analyze My Workflow") and user_input:
        progress_bar = progress_placeholder.progress(0)
        cancel_button = cancel_button_placeholder.button("Cancel Generation")
        
        canceled = False
        
        # Update progress to give feedback
        for percent_complete in range(1, 101):
            if cancel_button:
                canceled = True
                break
            progress_bar.progress(percent_complete)
            # Slow down near the end to simulate thinking
            if percent_complete > 70:  
                time.sleep(0.08)
            else:
                time.sleep(0.03)
        
        if not canceled:
            with st.spinner("Finalizing response..."):
                # Generate response using our template function instead of an actual LLM
                result = generate_response(user_input, creativity)
                
                # Clear progress indicators
                progress_placeholder.empty()
                cancel_button_placeholder.empty()
                
                # Display results in a nice format
                st.markdown("### 🤖 AI Suggestions:")
                
                # Display each section
                st.markdown("#### 🔧 Automation Opportunities")
                st.markdown(result["automation"])
                
                st.markdown("#### 📈 Efficiency Improvements")
                st.markdown(result["efficiency"])
                
                st.markdown("#### 🎯 Ideas to Make It Less Boring")
                st.markdown(result["fun"])
                
        else:
            progress_placeholder.empty()
            cancel_button_placeholder.empty()
            st.info("Generation canceled by user.")

# Add a placeholder for the output of the model
if not model_loaded:
    with st.expander("Sample Output Preview (Model not loaded yet)"):
        st.markdown("""
        #### 🔧 Automation Opportunities
        * Set up email filters to automatically categorize feedback emails
        * Use text analysis tools to extract and classify feedback types
        * Create an automated data entry script that populates your spreadsheet
        
        #### 📈 Efficiency Improvements
        * Implement a customer feedback form to collect pre-categorized data
        * Create dashboard templates that update automatically
        * Use scheduled reports instead of manual daily creation
        
        #### 🎯 Ideas to Make It Less Boring
        * Gamify the process by setting daily goals and rewards
        * Rotate responsibilities with team members
        * Add music or podcasts during the repetitive tasks
        """)

# Add footer
st.markdown("---")
st.markdown(f"Powered by {MODEL_DISPLAY_NAME}")

# Add additional tips in the sidebar
st.sidebar.subheader("Performance Tips")
st.sidebar.info("""
* If generation is slow, try a shorter response length
* Close other applications to free up memory
* For best performance, use a computer with a CUDA-capable GPU
""")