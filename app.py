import streamlit as st
import google.generativeai as genai
import os
import tempfile
import zipfile
import subprocess
import json
import time
import ast
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import shutil

# Page config
st.set_page_config(
    page_title="CodeOracle AI",
    page_icon="🧙‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
.main {
    padding-top: 2rem;
}
.stTabs [data-baseweb="tab-list"] {
    gap: 24px;
}
.stTabs [data-baseweb="tab"] {
    height: 50px;
    background-color: #262730;
    border-radius: 4px;
    color: white;
    padding: 0 20px;
}
.success-box {
    background-color: #1f4e79;
    border-left: 5px solid #00ff88;
    padding: 15px;
    border-radius: 5px;
    margin: 10px 0;
}
.error-box {
    background-color: #4a1e1e;
    border-left: 5px solid #ff4444;
    padding: 15px;
    border-radius: 5px;
    margin: 10px 0;
}
.info-box {
    background-color: #1e3a4a;
    border-left: 5px solid #44aaff;
    padding: 15px;
    border-radius: 5px;
    margin: 10px 0;
}
</style>
""", unsafe_allow_html=True)

class CodeOracle:
    def __init__(self, api_key: str):
        self.api_key = api_key
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemma-3n-e4b-it')
        self.projects = {}
        
    def generate_project(self, prompt: str, language: str, architecture: str = "standard") -> Dict:
        """Generate a complete project from natural language prompt"""
        
        system_prompt = f"""
        You are CodeOracle, an expert software engineer. Generate a complete, production-ready {language} project based on the user's requirements.
        
        CRITICAL REQUIREMENTS:
        1. Create a multi-file project structure with proper organization
        2. Include all necessary files: source code, tests, README.md, requirements/package files, .gitignore
        3. Write actual working code, not pseudocode or placeholders
        4. Include comprehensive error handling and logging
        5. Follow {language} best practices and conventions
        6. Make the code modular and well-documented
        7. Include unit tests and integration tests
        8. Add security considerations where applicable
        
        Project Requirements: {prompt}
        Target Language: {language}
        Architecture Pattern: {architecture}
        
        Return the response as a JSON object with this exact structure:
        {{
            "project_name": "project-name",
            "description": "Brief project description",
            "files": {{
                "filename1.ext": "file content here",
                "filename2.ext": "file content here",
                "tests/test_file.ext": "test content here",
                "README.md": "comprehensive readme",
                ".gitignore": "appropriate gitignore for {language}"
            }},
            "dependencies": ["list", "of", "dependencies"],
            "build_commands": ["command1", "command2"],
            "run_commands": ["command1", "command2"],
            "test_commands": ["test command"],
            "architecture_notes": "explanation of the chosen architecture"
        }}
        """
        
        try:
            response = self.model.generate_content(system_prompt)
            
            # Parse JSON response
            json_start = response.text.find('{')
            json_end = response.text.rfind('}') + 1
            json_str = response.text[json_start:json_end]
            
            project_data = json.loads(json_str)
            return project_data
            
        except Exception as e:
            st.error(f"Generation failed: {str(e)}")
            return None
    
    def run_tests(self, project_path: str, language: str, test_commands: List[str]) -> Dict:
        """Run automated tests and return results"""
        results = {
            "success": False,
            "output": "",
            "errors": "",
            "coverage": 0,
            "failed_tests": []
        }
        
        try:
            os.chdir(project_path)
            
            for cmd in test_commands:
                process = subprocess.run(
                    cmd.split(), 
                    capture_output=True, 
                    text=True, 
                    timeout=30
                )
                
                results["output"] += f"Command: {cmd}\n"
                results["output"] += process.stdout
                
                if process.returncode != 0:
                    results["errors"] += process.stderr
                    results["failed_tests"].append(cmd)
                else:
                    results["success"] = True
                    
        except subprocess.TimeoutExpired:
            results["errors"] = "Test execution timed out"
        except Exception as e:
            results["errors"] = str(e)
            
        return results
    
    def debug_and_fix(self, project_data: Dict, test_results: Dict, max_iterations: int = 3) -> Dict:
        """Autonomous debugging loop"""
        
        debug_prompt = f"""
        The following project has failing tests. Analyze the errors and fix the code:
        
        Project Structure: {list(project_data['files'].keys())}
        Test Errors: {test_results['errors']}
        Failed Commands: {test_results['failed_tests']}
        
        Current Code Files:
        {json.dumps(project_data['files'], indent=2)}
        
        Fix the issues and return the corrected files in the same JSON structure.
        Focus on:
        1. Syntax errors
        2. Import/dependency issues  
        3. Logic errors causing test failures
        4. Missing error handling
        
        Return only the corrected files that need changes in this format:
        {{
            "fixed_files": {{
                "filename": "corrected content"
            }},
            "fix_explanation": "What was fixed and why"
        }}
        """
        
        try:
            response = self.model.generate_content(debug_prompt)
            json_start = response.text.find('{')
            json_end = response.text.rfind('}') + 1
            json_str = response.text[json_start:json_end]
            
            fix_data = json.loads(json_str)
            
            # Apply fixes
            for filename, content in fix_data.get("fixed_files", {}).items():
                project_data["files"][filename] = content
                
            return {
                "success": True,
                "explanation": fix_data.get("fix_explanation", ""),
                "updated_project": project_data
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def refactor_code(self, project_data: Dict, refactor_type: str) -> Dict:
        """Refactor code for different objectives"""
        
        refactor_prompts = {
            "readability": "Refactor for maximum readability and maintainability",
            "performance": "Optimize for performance and efficiency", 
            "size": "Minimize code size and bundle size",
            "security": "Enhance security and add security best practices"
        }
        
        prompt = f"""
        {refactor_prompts[refactor_type]} for this project:
        
        {json.dumps(project_data['files'], indent=2)}
        
        Return the refactored files in JSON format with explanations.
        """
        
        try:
            response = self.model.generate_content(prompt)
            # Parse and return refactored code
            return {"success": True, "refactored": response.text}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def explain_code(self, code: str, language: str) -> str:
        """Provide detailed code explanation"""
        
        prompt = f"""
        Explain this {language} code line by line with:
        1. What each function/class does
        2. Time/space complexity analysis
        3. Alternative approaches
        4. How a senior developer would improve it
        5. Potential issues or edge cases
        
        Code:
        {code}
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Explanation failed: {str(e)}"
    
    def security_scan(self, project_data: Dict, language: str) -> Dict:
        """Perform security analysis"""
        
        prompt = f"""
        Perform a comprehensive security analysis of this {language} project using OWASP guidelines:
        
        {json.dumps(project_data['files'], indent=2)}
        
        Identify:
        1. Security vulnerabilities
        2. Input validation issues
        3. Authentication/authorization flaws
        4. Data exposure risks
        5. Dependency vulnerabilities
        
        Return findings with severity levels and suggested fixes.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return {"success": True, "report": response.text}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def generate_cicd(self, project_data: Dict, language: str, platform: str) -> str:
        """Generate CI/CD configuration"""
        
        prompt = f"""
        Generate {platform} CI/CD configuration for this {language} project:
        
        Project: {project_data['project_name']}
        Dependencies: {project_data['dependencies']}
        Build Commands: {project_data['build_commands']}
        Test Commands: {project_data['test_commands']}
        
        Include:
        1. Build pipeline
        2. Test automation
        3. Security scanning
        4. Deployment steps
        5. Environment management
        
        Platform: {platform}
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"CI/CD generation failed: {str(e)}"

def create_project_files(project_data: Dict, base_path: str):
    """Create actual files from project data"""
    for filename, content in project_data["files"].items():
        file_path = os.path.join(base_path, filename)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

def create_zip_download(project_data: Dict) -> bytes:
    """Create downloadable zip file"""
    zip_buffer = tempfile.NamedTemporaryFile(delete=False, suffix='.zip')
    
    with zipfile.ZipFile(zip_buffer.name, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for filename, content in project_data["files"].items():
            zip_file.writestr(filename, content)
    
    with open(zip_buffer.name, 'rb') as f:
        zip_data = f.read()
    
    os.unlink(zip_buffer.name)
    return zip_data

def main():
    # Title and header
    st.title("🧙‍♂️ CodeOracle AI")
    st.markdown("**Autonomous Software Engineering Assistant** - From idea to deployment in minutes")
    
    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # API Key input
        api_key = st.text_input(
            "Gemini API Key",
            type="password",
            help="Enter your Google Gemini API key"
        )
        
        if not api_key:
            st.error("Please enter your Gemini API key to continue")
            st.stop()
        
        # Language selection
        language = st.selectbox(
            "Programming Language",
            ["Python", "JavaScript", "TypeScript", "Go", "Rust", "Java", "Kotlin", "C++"]
        )
        
        # Architecture pattern
        architecture = st.selectbox(
            "Architecture Pattern",
            ["Standard", "MVC", "Microservices", "Serverless", "Clean Architecture", "Hexagonal"]
        )
        
        # Advanced settings
        st.subheader("Advanced Settings")
        max_debug_iterations = st.slider("Max Debug Iterations", 1, 10, 3)
        auto_test = st.checkbox("Auto-run tests", value=True)
        auto_debug = st.checkbox("Auto-debug failures", value=True)
        
    # Initialize CodeOracle
    if 'oracle' not in st.session_state:
        st.session_state.oracle = CodeOracle(api_key)
    
    # Main interface tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🚀 Generate", "🔧 Build & Test", "🔍 Analysis", "📊 Dashboard", "🛡️ Security", "🚀 Deploy"
    ])
    
    with tab1:
        st.header("Project Generator")
        
        # Project generation form
        with st.form("project_form"):
            prompt = st.text_area(
                "Describe your project:",
                placeholder="Build a REST API for a todo app with user authentication, SQLite database, and CRUD operations",
                height=100
            )
            
            col1, col2 = st.columns(2)
            with col1:
                generate_btn = st.form_submit_button("🧙‍♂️ Generate Project", type="primary")
            with col2:
                template = st.selectbox(
                    "Quick Templates",
                    ["Custom", "Web App + Auth", "REST API", "ML Service", "CLI Tool", "Microservice"]
                )
        
        # Template auto-fill
        if template != "Custom":
            template_prompts = {
                "Web App + Auth": "Create a modern web application with user authentication, responsive design, and database integration",
                "REST API": "Build a RESTful API with CRUD operations, authentication, and comprehensive documentation", 
                "ML Service": "Create a machine learning inference service with model loading, prediction endpoints, and monitoring",
                "CLI Tool": "Build a command-line tool with argument parsing, configuration management, and user-friendly output",
                "Microservice": "Create a microservice with health checks, logging, metrics, and containerization"
            }
            prompt = template_prompts.get(template, prompt)
        
        if generate_btn and prompt:
            with st.spinner("🧙‍♂️ CodeOracle is weaving your project..."):
                project_data = st.session_state.oracle.generate_project(prompt, language, architecture)
                
                if project_data:
                    st.session_state.current_project = project_data
                    st.success("✨ Project generated successfully!")
                    
                    # Display project overview
                    st.subheader("📋 Project Overview")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown(f"**Name:** {project_data['project_name']}")
                        st.markdown(f"**Language:** {language}")
                        st.markdown(f"**Files:** {len(project_data['files'])}")
                    
                    with col2:
                        st.markdown(f"**Dependencies:** {len(project_data.get('dependencies', []))}")
                        st.markdown(f"**Architecture:** {architecture}")
                    
                    st.markdown(f"**Description:** {project_data['description']}")
                    
                    # File browser
                    st.subheader("📁 Generated Files")
                    selected_file = st.selectbox("View file:", list(project_data['files'].keys()))
                    
                    if selected_file:
                        file_ext = selected_file.split('.')[-1]
                        st.code(project_data['files'][selected_file], language=file_ext)
                    
                    # Download button
                    zip_data = create_zip_download(project_data)
                    st.download_button(
                        label="📦 Download Project ZIP",
                        data=zip_data,
                        file_name=f"{project_data['project_name']}.zip",
                        mime="application/zip"
                    )
    
    with tab2:
        st.header("Build & Test Pipeline")
        
        if 'current_project' not in st.session_state:
            st.info("Generate a project first to see build and test options")
        else:
            project = st.session_state.current_project
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("🔨 Build Project"):
                    with st.spinner("Building project..."):
                        # Create temporary directory
                        temp_dir = tempfile.mkdtemp()
                        create_project_files(project, temp_dir)
                        
                        # Run build commands
                        build_success = True
                        build_output = ""
                        
                        for cmd in project.get('build_commands', []):
                            try:
                                result = subprocess.run(
                                    cmd.split(),
                                    cwd=temp_dir,
                                    capture_output=True,
                                    text=True,
                                    timeout=60
                                )
                                build_output += f"$ {cmd}\n{result.stdout}\n"
                                if result.returncode != 0:
                                    build_success = False
                                    build_output += f"Error: {result.stderr}\n"
                            except Exception as e:
                                build_success = False
                                build_output += f"Build failed: {str(e)}\n"
                        
                        if build_success:
                            st.markdown('<div class="success-box">✅ Build successful!</div>', unsafe_allow_html=True)
                        else:
                            st.markdown('<div class="error-box">❌ Build failed</div>', unsafe_allow_html=True)
                        
                        st.code(build_output, language="bash")
            
            with col2:
                if st.button("🧪 Run Tests"):
                    with st.spinner("Running tests..."):
                        temp_dir = tempfile.mkdtemp()
                        create_project_files(project, temp_dir)
                        
                        test_results = st.session_state.oracle.run_tests(
                            temp_dir, 
                            language, 
                            project.get('test_commands', [])
                        )
                        
                        st.session_state.test_results = test_results
                        
                        if test_results["success"]:
                            st.markdown('<div class="success-box">✅ All tests passed!</div>', unsafe_allow_html=True)
                        else:
                            st.markdown('<div class="error-box">❌ Some tests failed</div>', unsafe_allow_html=True)
                        
                        st.code(test_results["output"], language="bash")
                        
                        if test_results["errors"]:
                            st.error("Test Errors:")
                            st.code(test_results["errors"], language="bash")
            
            with col3:
                if st.button("🔧 Auto-Debug"):
                    if 'test_results' in st.session_state and not st.session_state.test_results["success"]:
                        with st.spinner("Auto-debugging..."):
                            debug_result = st.session_state.oracle.debug_and_fix(
                                project,
                                st.session_state.test_results,
                                max_debug_iterations
                            )
                            
                            if debug_result["success"]:
                                st.session_state.current_project = debug_result["updated_project"]
                                st.success("🔧 Auto-debug completed!")
                                st.markdown(debug_result["explanation"])
                            else:
                                st.error(f"Auto-debug failed: {debug_result['error']}")
                    else:
                        st.info("No failing tests to debug")
            
            # Refactoring options
            st.subheader("🔄 Refactoring Options")
            refactor_col1, refactor_col2, refactor_col3, refactor_col4 = st.columns(4)
            
            with refactor_col1:
                if st.button("📚 Readability"):
                    with st.spinner("Refactoring for readability..."):
                        result = st.session_state.oracle.refactor_code(project, "readability")
                        if result["success"]:
                            st.success("Refactored for readability!")
                            st.markdown(result["refactored"])
            
            with refactor_col2:
                if st.button("⚡ Performance"):
                    with st.spinner("Optimizing performance..."):
                        result = st.session_state.oracle.refactor_code(project, "performance")
                        if result["success"]:
                            st.success("Optimized for performance!")
                            st.markdown(result["refactored"])
            
            with refactor_col3:
                if st.button("📦 Size"):
                    with st.spinner("Minimizing size..."):
                        result = st.session_state.oracle.refactor_code(project, "size")
                        if result["success"]:
                            st.success("Minimized bundle size!")
                            st.markdown(result["refactored"])
            
            with refactor_col4:
                if st.button("🛡️ Security"):
                    with st.spinner("Enhancing security..."):
                        result = st.session_state.oracle.refactor_code(project, "security")
                        if result["success"]:
                            st.success("Security enhanced!")
                            st.markdown(result["refactored"])
    
    with tab3:
        st.header("Code Analysis & Insights")
        
        if 'current_project' not in st.session_state:
            st.info("Generate a project first to see analysis options")
        else:
            project = st.session_state.current_project
            
            # Code explanation
            st.subheader("📖 Explain Code")
            explain_file = st.selectbox("Select file to explain:", list(project['files'].keys()))
            
            if st.button("🔍 Explain This File"):
                with st.spinner("Analyzing code..."):
                    explanation = st.session_state.oracle.explain_code(
                        project['files'][explain_file], 
                        language
                    )
                    st.markdown(explanation)
            
            # Architecture visualization
            st.subheader("🏗️ Architecture Overview")
            
            if st.button("📊 Visualize Architecture"):
                # Create a simple architecture diagram
                files = list(project['files'].keys())
                file_types = {}
                
                for file in files:
                    ext = file.split('.')[-1] if '.' in file else 'other'
                    file_types[ext] = file_types.get(ext, 0) + 1
                
                # Create pie chart of file types
                fig = px.pie(
                    values=list(file_types.values()),
                    names=list(file_types.keys()),
                    title="Project File Distribution"
                )
                st.plotly_chart(fig)
                
                # Dependency graph (simplified)
                st.subheader("📦 Dependencies")
                deps = project.get('dependencies', [])
                if deps:
                    dep_df = pd.DataFrame({'Dependency': deps, 'Type': ['External'] * len(deps)})
                    st.dataframe(dep_df)
                else:
                    st.info("No external dependencies found")
            
            # Code metrics
            st.subheader("📏 Code Metrics")
            
            total_lines = sum(len(content.split('\n')) for content in project['files'].values())
            total_files = len(project['files'])
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Files", total_files)
            col2.metric("Total Lines", total_lines)
            col3.metric("Avg Lines/File", round(total_lines/total_files))
            col4.metric("Dependencies", len(project.get('dependencies', [])))
    
    with tab4:
        st.header("📊 Project Health Dashboard")
        
        if 'current_project' not in st.session_state:
            st.info("Generate a project first to see the dashboard")
        else:
            project = st.session_state.current_project
            
            # Health score calculation (mock)
            health_score = 85  # This would be calculated based on various metrics
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Health Score", f"{health_score}%", "5%")
            with col2:
                st.metric("Test Coverage", "78%", "12%")
            with col3:
                st.metric("Security Rating", "A-", "0")
            
            # Project timeline (mock data)
            st.subheader("🕒 Project Timeline")
            timeline_data = pd.DataFrame({
                'Event': ['Generated', 'Built', 'Tested', 'Secured'],
                'Timestamp': [datetime.now().strftime('%H:%M:%S')] * 4,
                'Status': ['✅', '✅', '⏳', '⏳']
            })
            st.dataframe(timeline_data, use_container_width=True)
            
            # Code quality trends (mock chart)
            st.subheader("📈 Quality Trends")
            
            # Generate mock trend data
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
            st.plotly_chart(fig, use_container_width=True)
    
    with tab5:
        st.header("🛡️ Security Analysis")
        
        if 'current_project' not in st.session_state:
            st.info("Generate a project first to run security analysis")
        else:
            project = st.session_state.current_project
            
            if st.button("🔍 Run Security Scan"):
                with st.spinner("Scanning for security vulnerabilities..."):
                    security_result = st.session_state.oracle.security_scan(project, language)
                    
                    if security_result["success"]:
                        st.markdown("### 🛡️ Security Report")
                        st.markdown(security_result["report"])
                    else:
                        st.error(f"Security scan failed: {security_result['error']}")
            
            # Security checklist
            st.subheader("✅ Security Checklist")
            
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
            
            for item in security_items:
                st.checkbox(item, value=False)
    
    with tab6:
        st.header("🚀 Deployment & CI/CD")
        
        if 'current_project' not in st.session_state:
            st.info("Generate a project first to see deployment options")
        else:
            project = st.session_state.current_project
            
            # CI/CD platform selection
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("🔄 CI/CD Configuration")
                cicd_platform = st.selectbox(
                    "Platform:",
                    ["GitHub Actions", "GitLab CI", "CircleCI", "Jenkins"]
                )
                
                if st.button("Generate CI/CD Config"):
                    with st.spinner("Generating CI/CD configuration..."):
                        cicd_config = st.session_state.oracle.generate_cicd(
                            project, language, cicd_platform
                        )
                        st.code(cicd_config, language="yaml")
                        
                        # Download CI/CD config
                        st.download_button(
                            label="📥 Download CI/CD Config",
                            data=cicd_config,
                            file_name=f"{cicd_platform.lower().replace(' ', '_')}.yml",
                            mime="text/yaml"
                        )
            
            with col2:
                st.subheader("🐳 Containerization")
                
                if st.button("Generate Dockerfile"):
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
                    
                    with st.spinner("Generating Dockerfile..."):
                        try:
                            response = st.session_state.oracle.model.generate_content(dockerfile_prompt)
                            dockerfile_content = response.text
                            
                            st.code(dockerfile_content, language="dockerfile")
                            
                            st.download_button(
                                label="📥 Download Dockerfile",
                                data=dockerfile_content,
                                file_name="Dockerfile",
                                mime="text/plain"
                            )
                        except Exception as e:
                            st.error(f"Dockerfile generation failed: {str(e)}")
            
            # Deployment scripts
            st.subheader("🌐 Deployment Scripts")
            
            deployment_type = st.selectbox(
                "Deployment Target:",
                ["Docker Compose", "Kubernetes", "AWS ECS", "Google Cloud Run", "Azure Container Apps"]
            )
            
            if st.button("Generate Deployment Script"):
                deploy_prompt = f"""
                Generate deployment configuration for {deployment_type} for this project:
                
                Project: {project['project_name'
