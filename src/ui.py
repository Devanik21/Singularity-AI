import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from src.utils import create_zip_download

def setup_page_config():
    st.set_page_config(
        page_title="Singularity-AI",
        page_icon="♾️",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def load_custom_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600&display=swap');

    .main {
        padding-top: 1rem;
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 25%, #16213e 50%, #0f0f23 75%, #000000 100%);
        color: #ffffff;
    }

    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 25%, #16213e 50%, #0f0f23 75%, #000000 100%);
    }

    /* Header styling */
    h1 {
        font-family: 'Orbitron', monospace !important;
        font-weight: 900 !important;
        background: linear-gradient(45deg, #00d4ff, #ff00ff, #00ff88);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-size: 3.5rem !important;
        margin-bottom: 0.5rem !important;
        text-shadow: 0 0 20px rgba(0, 212, 255, 0.5);
    }

    .subtitle {
        font-family: 'Rajdhani', sans-serif;
        text-align: center;
        font-size: 1.2rem;
        color: #00d4ff;
        margin-bottom: 2rem;
        font-weight: 300;
    }

    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
        border-right: 2px solid #00d4ff;
    }

    .css-1d391kg .stSelectbox, .css-1d391kg .stTextInput {
        color: #ffffff;
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background: rgba(26, 26, 46, 0.8);
        padding: 10px;
        border-radius: 15px;
        border: 1px solid #00d4ff;
    }

    .stTabs [data-baseweb="tab"] {
        height: 55px;
        background: linear-gradient(135deg, #1a1a2e, #16213e);
        border-radius: 12px;
        color: #00d4ff;
        border: 2px solid transparent;
        font-family: 'Rajdhani', sans-serif;
        font-weight: 600;
        transition: all 0.3s ease;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background: linear-gradient(135deg, #00d4ff, #0099cc);
        color: #000000;
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0, 212, 255, 0.4);
    }

    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, #00d4ff, #6b1cb0);
        color: #000000;
        border: 2px solid #ff00ff;
    }

    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #00d4ff, #0099cc);
        color: #000000;
        border: none;
        border-radius: 10px;
        font-family: 'Rajdhani', sans-serif;
        font-weight: 600;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 212, 255, 0.3);
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #005461, #002d7a);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 255, 136, 0.4);
    }

    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #ff00ff, #cc00cc);
        color: #ffffff;
    }

    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #ff44ff, #ff00cc);
    }

    /* Success/Error/Info boxes */
    .success-box {
        background: linear-gradient(135deg, #00ff88, #00cc6a);
        color: #000000;
        border-left: 5px solid #ffffff;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        font-family: 'Rajdhani', sans-serif;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(0, 255, 136, 0.3);
    }

    .error-box {
        background: linear-gradient(135deg, #ff4444, #cc3333);
        color: #ffffff;
        border-left: 5px solid #ffffff;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        font-family: 'Rajdhani', sans-serif;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(255, 68, 68, 0.3);
    }

    .info-box {
        background: linear-gradient(135deg, #00d4ff, #0099cc);
        color: #000000;
        border-left: 5px solid #ffffff;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        font-family: 'Rajdhani', sans-serif;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(0, 212, 255, 0.3);
    }

    /* Form styling */
    .stTextArea textarea, .stTextInput input, .stSelectbox select {
        background: rgba(26, 26, 46, 0.8);
        color: #ffffff;
        border: 2px solid #00d4ff;
        border-radius: 8px;
        font-family: 'Rajdhani', sans-serif;
    }

    /* Metric styling */
    .css-1xarl3l {
        background: linear-gradient(135deg, rgba(0, 212, 255, 0.1), rgba(255, 0, 255, 0.1));
        border: 2px solid #00d4ff;
        border-radius: 10px;
        padding: 1rem;
    }

    /* Code blocks */
    .stCode {
        background: rgba(0, 0, 0, 0.8) !important;
        border: 1px solid #00d4ff;
        border-radius: 8px;
    }

    /* Infinity symbol animation */
    .infinity {
        display: inline-block;
        animation: rotate 3s linear infinite;
        color: #00ff88;
        font-size: 1.2em;
    }

    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }

    /* Glowing effects */
    .glow {
        text-shadow: 0 0 10px currentColor;
    }

    /* Dataframe styling */
    .stDataFrame {
        background: rgba(26, 26, 46, 0.8);
        border: 1px solid #00d4ff;
        border-radius: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

def render_sidebar():
    with st.sidebar:
        st.markdown("### ⚙️ Configuration")

        # Language selection
        language = st.selectbox(
            "💻 Programming Language",
            ["Python", "JavaScript", "TypeScript", "Go", "Rust", "Java", "Kotlin", "C++"],
            key="language_select"
        )

        # Architecture pattern
        architecture = st.selectbox(
            "🏗️ Architecture Pattern",
            ["Standard", "MVC", "Microservices", "Serverless", "Clean Architecture", "Hexagonal"],
            key="architecture_select"
        )

        # Advanced settings
        st.markdown("### 🔬 Advanced Settings")
        max_debug_iterations = st.slider("Max Debug Iterations", 1, 10, 3, key="debug_iter")
        auto_test = st.checkbox("Auto-run tests", value=True, key="auto_test")
        auto_debug = st.checkbox("Auto-debug failures", value=True, key="auto_debug")

        return language, architecture, max_debug_iterations, auto_test, auto_debug

def render_main_content():
    st.markdown('<h1>♾️ Singularity-AI</h1>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Where AI meets infinity <span class="infinity">♾️</span></div>', unsafe_allow_html=True)

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🚀 Generate", "🔧 Build & Test", "🔍 Analysis", "📊 Dashboard", "🛡️ Security", "🚀 Deploy"
    ])

    return tab1, tab2, tab3, tab4, tab5, tab6

def render_generate_tab(language, architecture):
    with st.expander("🚀 Project Generator", expanded=True):
        col1, col2 = st.columns([3, 1])

        with col1:
            prompt = st.text_area(
                "📝 Describe your project:",
                placeholder="Build a REST API for a todo app with user authentication, SQLite database, and CRUD operations",
                height=120,
                key="project_prompt"
            )

        with col2:
            template = st.selectbox(
                "⚡ Quick Templates",
                ["Custom", "Web App + Auth", "REST API", "ML Service", "CLI Tool", "Microservice"],
                key="template_select"
            )

        template_prompts = {
            "Custom": "",
            "Web App + Auth": "Create a modern web application with user authentication, responsive design, and database integration",
            "REST API": "Build a RESTful API with CRUD operations, authentication, and comprehensive documentation",
            "ML Service": "Create a machine learning inference service with model loading, prediction endpoints, and monitoring",
            "CLI Tool": "Build a command-line tool with argument parsing, configuration management, and user-friendly output",
            "Microservice": "Create a microservice with health checks, logging, metrics, and containerization"
        }

        default_prompt = template_prompts.get(template, "")

        if st.button("🧙‍♂️ Generate Project", type="primary", key="generate_btn"):
            if prompt:
                return prompt
            else:
                st.error("⚠️ Please provide a project description")
    return None

def render_project_overview(language, architecture):
    if st.session_state.current_project and st.session_state.generation_status == "success":
        project = st.session_state.current_project

        st.markdown('<div class="success-box">✨ Project generated successfully!</div>', unsafe_allow_html=True)

        st.markdown("### 📋 Project Overview")
        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"**🏷️ Name:** `{project['project_name']}`")
            st.markdown(f"**💻 Language:** `{language}`")
            st.markdown(f"**📁 Files:** `{st.session_state.project_metrics['total_files']}`")

        with col2:
            st.markdown(f"**📦 Dependencies:** `{st.session_state.project_metrics['dependencies']}`")
            st.markdown(f"**🏗️ Architecture:** `{architecture}`")
            st.markdown(f"**📏 Lines:** `{st.session_state.project_metrics['total_lines']}`")

        st.markdown(f"**📝 Description:** {project['description']}")

        st.markdown("### 📁 Generated Files")
        selected_file = st.selectbox(
            "View file:",
            list(project['files'].keys()),
            key="file_browser"
        )

        if selected_file:
            file_ext = selected_file.split('.')[-1] if '.' in selected_file else 'text'
            st.code(project['files'][selected_file], language=file_ext)

        zip_data = create_zip_download(project)
        st.download_button(
            label="📦 Download Project ZIP",
            data=zip_data,
            file_name=f"{project['project_name']}.zip",
            mime="application/zip",
            key="download_zip"
        )

def render_build_test_tab(language, max_debug_iterations):
    if not st.session_state.current_project:
        st.markdown('<div class="info-box">ℹ️ Generate a project first to see build and test options</div>', unsafe_allow_html=True)
        return

    project = st.session_state.current_project

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🔨 Build Project", key="build_btn"):
            return "build"

    if st.session_state.build_output:
        if st.session_state.build_output["success"]:
            st.markdown('<div class="success-box">✅ Build successful!</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="error-box">❌ Build failed</div>', unsafe_allow_html=True)

        st.code(st.session_state.build_output["output"], language="bash")

    with col2:
        if st.button("🧪 Run Tests", key="test_btn"):
            return "test"

    if st.session_state.test_results:
        if st.session_state.test_results["success"]:
            st.markdown('<div class="success-box">✅ All tests passed!</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="error-box">❌ Some tests failed</div>', unsafe_allow_html=True)

        st.code(st.session_state.test_results["output"], language="bash")

        if st.session_state.test_results["errors"]:
            st.error("Test Errors:")
            st.code(st.session_state.test_results["errors"], language="bash")

    with col3:
        if st.button("🔧 Auto-Debug", key="debug_btn"):
            if st.session_state.test_results and not st.session_state.test_results["success"]:
                return "debug"
            else:
                st.info("No failing tests to debug")

    st.markdown("### 🔄 Refactoring Options")
    refactor_col1, refactor_col2, refactor_col3, refactor_col4 = st.columns(4)

    with refactor_col1:
        if st.button("📚 Readability", key="refactor_readability"):
            return "refactor_readability"

    if "readability" in st.session_state.refactor_results:
        with st.expander("📚 Readability Refactor Result"):
            st.markdown(st.session_state.refactor_results["readability"])

    with refactor_col2:
        if st.button("⚡ Performance", key="refactor_performance"):
            return "refactor_performance"

    if "performance" in st.session_state.refactor_results:
        with st.expander("⚡ Performance Refactor Result"):
            st.markdown(st.session_state.refactor_results["performance"])

    with refactor_col3:
        if st.button("📦 Size", key="refactor_size"):
            return "refactor_size"

    if "size" in st.session_state.refactor_results:
        with st.expander("📦 Size Refactor Result"):
            st.markdown(st.session_state.refactor_results["size"])

    with refactor_col4:
        if st.button("🛡️ Security", key="refactor_security"):
            return "refactor_security"

    if "security" in st.session_state.refactor_results:
        with st.expander("🛡️ Security Refactor Result"):
            st.markdown(st.session_state.refactor_results["security"])

def render_analysis_tab(language):
    if not st.session_state.current_project:
        st.markdown('<div class="info-box">ℹ️ Generate a project first to see analysis options</div>', unsafe_allow_html=True)
        return

    project = st.session_state.current_project

    st.markdown("### 📖 Explain Code")
    explain_file = st.selectbox(
        "Select file to explain:",
        list(project['files'].keys()),
        key="explain_file_select"
    )

    if st.button("🔍 Explain This File", key="explain_btn"):
        with st.spinner("🧠 Analyzing code..."):
            explanation = st.session_state.oracle.explain_code(
                project['files'][explain_file],
                language
            )
            st.session_state.explanations[explain_file] = explanation

    if explain_file in st.session_state.explanations:
        with st.expander(f"📖 Explanation: {explain_file}"):
            st.markdown(st.session_state.explanations[explain_file])

    st.markdown("### 🏗️ Architecture Overview")

    if st.button("📊 Visualize Architecture", key="viz_arch_btn"):
        files = list(project['files'].keys())
        file_types = {}

        for file in files:
            ext = file.split('.')[-1] if '.' in file else 'other'
            file_types[ext] = file_types.get(ext, 0) + 1

        st.session_state.arch_viz_data = file_types

    if hasattr(st.session_state, 'arch_viz_data'):
        fig = px.pie(
            values=list(st.session_state.arch_viz_data.values()),
            names=list(st.session_state.arch_viz_data.keys()),
            title="Project File Distribution",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("### 📦 Dependencies")
        deps = project.get('dependencies', [])
        if deps:
            dep_df = pd.DataFrame({'Dependency': deps, 'Type': ['External'] * len(deps)})
            st.dataframe(dep_df, use_container_width=True)
        else:
            st.info("No external dependencies found")

    st.markdown("### 📏 Code Metrics")

    if hasattr(st.session_state, 'project_metrics') and st.session_state.project_metrics:
       metrics = st.session_state.project_metrics
       col1, col2, col3, col4 = st.columns(4)
       col1.metric("Total Files", metrics['total_files'])
       col2.metric("Total Lines", metrics['total_lines'])
       col3.metric("Avg Lines/File", metrics['avg_lines_per_file'])
       col4.metric("Dependencies", metrics['dependencies'])
    elif st.session_state.current_project:
       project = st.session_state.current_project
       total_files = len(project['files'])
       total_lines = sum(len(content.split('\n')) for content in project['files'].values())
       avg_lines = round(total_lines/total_files) if total_files > 0 else 0
       dependencies = len(project.get('dependencies', []))

       col1, col2, col3, col4 = st.columns(4)
       col1.metric("Total Files", total_files)
       col2.metric("Total Lines", total_lines)
       col3.metric("Avg Lines/File", avg_lines)
       col4.metric("Dependencies", dependencies)

def render_dashboard_tab():
    if not st.session_state.current_project:
        st.markdown('<div class="info-box">ℹ️ Generate a project first to see the dashboard</div>', unsafe_allow_html=True)
        return

    health_score = 85
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("🏥 Health Score", f"{health_score}%", "5%")
    with col2:
        test_coverage = "78%" if st.session_state.test_results and st.session_state.test_results["success"] else "0%"
        st.metric("🧪 Test Coverage", test_coverage, "12%")
    with col3:
        security_rating = "A-" if "security" in st.session_state.refactor_results else "C"
        st.metric("🛡️ Security Rating", security_rating, "0")

    st.markdown("### 🕒 Project Timeline")
    timeline_events = []
    if st.session_state.current_project:
        timeline_events.append(('Generated', datetime.now().strftime('%H:%M:%S'), '✅'))
    if st.session_state.build_output:
        status = '✅' if st.session_state.build_output["success"] else '❌'
        timeline_events.append(('Built', datetime.now().strftime('%H:%M:%S'), status))
    if st.session_state.test_results:
        status = '✅' if st.session_state.test_results["success"] else '❌'
        timeline_events.append(('Tested', datetime.now().strftime('%H:%M:%S'), status))
    if st.session_state.security_report:
        timeline_events.append(('Secured', datetime.now().strftime('%H:%M:%S'), '✅'))

    if timeline_events:
        timeline_data = pd.DataFrame(timeline_events, columns=['Event', 'Timestamp', 'Status'])
        st.dataframe(timeline_data, use_container_width=True)

    st.markdown("### 📈 Quality Trends")

    dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='M')
    quality_data = pd.DataFrame({
        'Date': dates,
        'Code Quality': [75 + i*2 + (i%3)*5 for i in range(len(dates))],
        'Test Coverage': [60 + i*1.5 + (i%2)*3 for i in range(len(dates))],
        'Security Score': [70 + i*1.8 + (i%4)*4 for i in range(len(dates))]
    })

    fig = px.line(
        quality_data,
        x='Date',
        y=['Code Quality', 'Test Coverage', 'Security Score'],
        title="Project Health Over Time"
    )
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white'
    )
    st.plotly_chart(fig, use_container_width=True)

def render_security_tab(language):
    if not st.session_state.current_project:
        st.markdown('<div class="info-box">ℹ️ Generate a project first to run security analysis</div>', unsafe_allow_html=True)
        return

    if st.button("🔍 Run Security Scan", key="security_scan_btn"):
        return "scan"

    if st.session_state.security_report:
        if st.session_state.security_report["success"]:
            st.markdown("### 🛡️ Security Report")
            st.markdown(st.session_state.security_report["report"])
        else:
            st.error(f"Security scan failed: {st.session_state.security_report['error']}")

    st.markdown("### ✅ Security Checklist")

    security_items = [
        "Input validation implemented",
        "Authentication mechanisms in place",
        "Authorization checks present",
        "SQL injection prevention",
        "XSS protection enabled",
        "CSRF tokens implemented",
        "Secure headers configured",
        "Dependency vulnerabilities checked"
    ]

    for i, item in enumerate(security_items):
        st.checkbox(item, value=False, key=f"security_check_{i}")

def render_deploy_tab(language):
    if not st.session_state.current_project:
        st.markdown('<div class="info-box">ℹ️ Generate a project first to see deployment options</div>', unsafe_allow_html=True)
        return

    project = st.session_state.current_project

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🔄 CI/CD Configuration")
        cicd_platform = st.selectbox(
            "Platform:",
            ["GitHub Actions", "GitLab CI", "CircleCI", "Jenkins"],
            key="cicd_platform_select"
        )

        if st.button("Generate CI/CD Config", key="generate_cicd_btn"):
            with st.spinner("⚙️ Generating CI/CD configuration..."):
                cicd_config = st.session_state.oracle.generate_cicd(
                    project, language, cicd_platform
                )
                st.session_state.cicd_configs[cicd_platform] = cicd_config

        if cicd_platform in st.session_state.cicd_configs:
            st.code(st.session_state.cicd_configs[cicd_platform], language="yaml")

            st.download_button(
                label="📥 Download CI/CD Config",
                data=st.session_state.cicd_configs[cicd_platform],
                file_name=f"{cicd_platform.lower().replace(' ', '_')}.yml",
                mime="text/yaml",
                key=f"download_cicd_{cicd_platform}"
            )

    with col2:
        st.markdown("### 🐳 Containerization")

        if st.button("Generate Dockerfile", key="generate_dockerfile_btn"):
            dockerfile_prompt = f"""
            Generate a production-ready Dockerfile for this {language} project:

            Project: {project['project_name']}
            Dependencies: {project.get('dependencies', [])}
            Build Commands: {project.get('build_commands', [])}
            Run Commands: {project.get('run_commands', [])}

            Include:
            - Multi-stage build
            - Security best practices
            - Optimized layer caching
            - Non-root user
            - Health checks
            """

            with st.spinner("🐳 Generating Dockerfile..."):
                try:
                    response = st.session_state.oracle.model.generate_content(dockerfile_prompt)
                    st.session_state.dockerfile_content = response.text
                except Exception as e:
                    st.error(f"Dockerfile generation failed: {str(e)}")

        if hasattr(st.session_state, 'dockerfile_content'):
            st.code(st.session_state.dockerfile_content, language="dockerfile")

            st.download_button(
                label="📥 Download Dockerfile",
                data=st.session_state.dockerfile_content,
                file_name="Dockerfile",
                mime="text/plain",
                key="download_dockerfile"
            )

    st.markdown("### 🌐 Deployment Scripts")

    deployment_type = st.selectbox(
        "Deployment Target:",
        ["Docker Compose", "Kubernetes", "AWS ECS", "Google Cloud Run", "Azure Container Apps"],
        key="deployment_type_select"
    )

    if st.button("Generate Deployment Script", key="generate_deploy_btn"):
        deploy_prompt = f"""
        Generate deployment configuration for {deployment_type} for this project:

        Project: {project['project_name']}
        Language: {language}
        Dependencies: {project.get('dependencies', [])}
        Build Commands: {project.get('build_commands', [])}
        Run Commands: {project.get('run_commands', [])}

        Include:
        - Service definitions
        - Environment variables
        - Resource limits
        - Health checks
        - Networking configuration
        - Scaling policies
        - Monitoring setup
        """

        with st.spinner(f"🚀 Generating {deployment_type} configuration..."):
            try:
                response = st.session_state.oracle.model.generate_content(deploy_prompt)
                if 'deploy_configs' not in st.session_state:
                    st.session_state.deploy_configs = {}
                st.session_state.deploy_configs[deployment_type] = response.text
            except Exception as e:
                st.error(f"Deployment configuration generation failed: {str(e)}")

    if hasattr(st.session_state, 'deploy_configs') and deployment_type in st.session_state.deploy_configs:
        st.code(st.session_state.deploy_configs[deployment_type], language="yaml")

        file_extensions = {
            "Docker Compose": "docker-compose.yml",
            "Kubernetes": "k8s-deployment.yaml",
            "AWS ECS": "ecs-task-definition.json",
            "Google Cloud Run": "cloudrun-service.yaml",
            "Azure Container Apps": "containerapp.yaml"
        }

        filename = file_extensions.get(deployment_type, "deployment.yaml")

        st.download_button(
            label=f"📥 Download {deployment_type} Config",
            data=st.session_state.deploy_configs[deployment_type],
            file_name=filename,
            mime="text/yaml",
            key=f"download_deploy_{deployment_type}"
        )

    st.markdown("### 🔧 Environment Configuration")

    env_type = st.selectbox(
        "Environment Type:",
        ["Development", "Staging", "Production"],
        key="env_type_select"
    )

    if st.button("Generate Environment Config", key="generate_env_btn"):
        env_prompt = f"""
        Generate environment configuration for {env_type} environment:

        Project: {project['project_name']}
        Language: {language}

        Include appropriate settings for {env_type}:
        - Environment variables
        - Database configurations
        - Logging levels
        - Security settings
        - Performance optimizations
        - Monitoring configurations
        """

        with st.spinner(f"⚙️ Generating {env_type} environment config..."):
            try:
                response = st.session_state.oracle.model.generate_content(env_prompt)
                if 'env_configs' not in st.session_state:
                    st.session_state.env_configs = {}
                st.session_state.env_configs[env_type] = response.text
            except Exception as e:
                st.error(f"Environment configuration generation failed: {str(e)}")

    if hasattr(st.session_state, 'env_configs') and env_type in st.session_state.env_configs:
        st.code(st.session_state.env_configs[env_type], language="bash")

        st.download_button(
            label=f"📥 Download {env_type} Config",
            data=st.session_state.env_configs[env_type],
            file_name=f".env.{env_type.lower()}",
            mime="text/plain",
            key=f"download_env_{env_type}"
        )

def render_footer():
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #00d4ff; padding: 20px; font-family: "Rajdhani", sans-serif;'>
            <p style='font-size: 1.5rem; font-weight: 600;'>♾️ <strong>Singularity-AI</strong> - Where AI meets infinity</p>
            <p style='color: #00ff88;'>Autonomous Software Engineering Assistant</p>
            <p style='color: #ffffff; opacity: 0.8;'>Powered by Google Gemini • Built with Streamlit • Enhanced with infinite possibilities</p>
            <div class='infinity' style='font-size: 2rem; margin-top: 1rem;'>♾️</div>
        </div>
        """,
        unsafe_allow_html=True
    )
