import streamlit as st
import google.generativeai as genai
import os
import tempfile
import zipfile
import subprocess
import json
import time
import ast
import re # IMPROVEMENT: Import the regular expression module
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import shutil

# Page config
st.set_page_config(
    page_title="Singularity-AI",
    page_icon="♾️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Singularity-AI theme
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

class CodeOracle:
    def __init__(self, api_key: str):
        self.api_key = api_key
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        self.projects = {}
        
    def generate_project(self, prompt: str, language: str, architecture: str = "standard") -> Dict:
        """Generate a complete project from natural language prompt"""
        
        # IMPROVEMENT: The prompt now asks the AI to wrap the JSON in markdown code blocks for reliable parsing.
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
        
        Return the response as a JSON object inside a markdown code block with this exact structure:
        ```json
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
        ```
        """
        
        try:
            response = self.model.generate_content(system_prompt)
            
            # IMPROVEMENT: Use regex to find the JSON block, which is more reliable.
            match = re.search(r"```json\s*(.+?)\s*```", response.text, re.DOTALL)
            if not match:
                st.error("Failed to parse the project structure from the AI's response.")
                # For debugging: show the raw response from the AI
                st.code(response.text, language="text")
                return None

            json_str = match.group(1)
            project_data = json.loads(json_str)
            return project_data
            
        except json.JSONDecodeError as e:
            st.error(f"Generation failed: Could not decode JSON. Error: {str(e)}")
            st.code(json_str, language="json") # Show the invalid JSON
            return None
        except Exception as e:
            st.error(f"An unexpected error occurred during generation: {str(e)}")
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
        
        # IMPROVEMENT: The prompt now asks the AI to wrap the JSON in markdown code blocks.
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
        
        Return only the corrected files that need changes inside a markdown JSON block like this:
        ```json
        {{
            "fixed_files": {{
                "filename": "corrected content"
            }},
            "fix_explanation": "What was fixed and why"
        }}
        ```
        """
        
        try:
            response = self.model.generate_content(debug_prompt)

            # IMPROVEMENT: Use regex for more reliable parsing of the fix data.
            match = re.search(r"```json\s*(\{.*?\})\s*```", response.text, re.DOTALL)
            if not match:
                return {"success": False, "error": "Could not parse the fix from the AI's response."}
            
            json_str = match.group(1)
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
    # Ensure base directory exists
    os.makedirs(base_path, exist_ok=True)
    
    for filename, content in project_data["files"].items():
        file_path = os.path.join(base_path, filename)
        
        # Create directory if filename contains subdirectories
        file_dir = os.path.dirname(file_path)
        if file_dir and file_dir != base_path:
            os.makedirs(file_dir, exist_ok=True)
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            st.error(f"Failed to create file {filename}: {str(e)}")
            continue

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

# Initialize session state variables to prevent reruns
def init_session_state():
    """Initialize all session state variables"""
    if 'oracle' not in st.session_state:
        st.session_state.oracle = None
    if 'current_project' not in st.session_state:
        st.session_state.current_project = None
    if 'test_results' not in st.session_state:
        st.session_state.test_results = None
    if 'generation_status' not in st.session_state:
        st.session_state.generation_status = None
    if 'build_output' not in st.session_state:
        st.session_state.build_output = None
    if 'security_report' not in st.session_state:
        st.session_state.security_report = None
    if 'cicd_configs' not in st.session_state:
        st.session_state.cicd_configs = {}
    if 'refactor_results' not in st.session_state:
        st.session_state.refactor_results = {}
    if 'explanations' not in st.session_state:
        st.session_state.explanations = {}
    if 'project_metrics' not in st.session_state:
        st.session_state.project_metrics = {}

def main():
    # Initialize session state
    init_session_state()
    
    # Title and header with new theme
    st.markdown('<h1>♾️ Singularity-AI</h1>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Where AI meets infinity <span class="infinity">♾️</span></div>', unsafe_allow_html=True)
    
    # Sidebar configuration
    with st.sidebar:
        st.markdown("### ⚙️ Configuration")
        
        # API Key input
        api_key = st.text_input(
            "🔑 Gemini API Key",
            type="password",
            help="Enter your Google Gemini API key",
            key="api_key_input"
        )
        
        if not api_key:
            st.error("⚠️ Please enter your Gemini API key to continue")
            st.stop()
        
        # Initialize CodeOracle only once
        if st.session_state.oracle is None:
            st.session_state.oracle = CodeOracle(api_key)
            st.success("✅ Singularity-AI Initialized!")
        
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
    
    # Main interface tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "✨ Generate", "🔧 Build & Test", "🔍 Analysis", "📊 Dashboard", "🛡️ Security", "🎉 Deploy"
    ])
    
    with tab1:
        st.markdown("### 🎯 Project Generator")
        
        # Project generation form
        col1, col2 = st.columns([3, 1])
        
        with col1:
            prompt = st.text_area(
                "📝 Describe your project:",
                #value=default_prompt,
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
        
        # Template auto-fill
        # Template auto-fill - set default value based on template
        template_prompts = {
            "Custom": "",
            "Web App + Auth": "Create a modern web application with user authentication, responsive design, and database integration",
            "REST API": "Build a RESTful API with CRUD operations, authentication, and comprehensive documentation", 
            "ML Service": "Create a machine learning inference service with model loading, prediction endpoints, and monitoring",
            "CLI Tool": "Build a command-line tool with argument parsing, configuration management, and user-friendly output",
            "Microservice": "Create a microservice with health checks, logging, metrics, and containerization"
        }
        
        # Set the default prompt value based on template selection
        default_prompt = template_prompts.get(template, "")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🧙‍♂️ Generate Project", type="primary", key="generate_btn"):
                if prompt:
                    with st.spinner("🔮 Singularity-AI is crafting your project..."):
                        project_data = st.session_state.oracle.generate_project(prompt, language, architecture)
                        
                        if project_data:
                            st.session_state.current_project = project_data
                            st.session_state.generation_status = "success"
                            
                            # Calculate initial metrics
                            total_lines = sum(len(content.split('\n')) for content in project_data['files'].values())
                            st.session_state.project_metrics = {
                                'total_files': len(project_data['files']),
                                'total_lines': total_lines,
                                'avg_lines_per_file': round(total_lines/len(project_data['files'])),
                                'dependencies': len(project_data.get('dependencies', []))
                            }
                        else:
                            st.session_state.generation_status = "error"
                else:
                    st.error("⚠️ Please provide a project description")
        
        # Display project overview (persistent)
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
            
            # File browser
            st.markdown("### 📁 Generated Files")
            selected_file = st.selectbox(
                "View file:", 
                list(project['files'].keys()),
                key="file_browser"
            )
            
            if selected_file:
                file_ext = selected_file.split('.')[-1] if '.' in selected_file else 'text'
                st.code(project['files'][selected_file], language=file_ext)
            
            # Download button
            col1, col2 = st.columns(2)
            with col1:
                zip_data = create_zip_download(project)
                st.download_button(
                    label="📦 Download Project ZIP",
                    data=zip_data,
                    file_name=f"{project['project_name']}.zip",
                    mime="application/zip",
                    key="download_zip"
                )
    
    with tab2:
        st.markdown("### 🔧 Build & Test Pipeline")
        
        if not st.session_state.current_project:
            st.markdown('<div class="info-box">ℹ️ Generate a project first to see build and test options</div>', unsafe_allow_html=True)
        else:
            project = st.session_state.current_project
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("🔨 Build Project", key="build_btn"):
                    with st.spinner("🏗️ Building project..."):
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
                        
                        st.session_state.build_output = {
                            "success": build_success,
                            "output": build_output
                        }
            
            # Display build results (persistent)
            if st.session_state.build_output:
                if st.session_state.build_output["success"]:
                    st.markdown('<div class="success-box">✅ Build successful!</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="error-box">❌ Build failed</div>', unsafe_allow_html=True)
                
                st.code(st.session_state.build_output["output"], language="bash")
            
            with col2:
                if st.button("🧪 Run Tests", key="test_btn"):
                    with st.spinner("🔬 Running tests..."):
                        temp_dir = tempfile.mkdtemp()
                        create_project_files(project, temp_dir)
                        
                        test_results = st.session_state.oracle.run_tests(
                            temp_dir, 
                            language, 
                            project.get('test_commands', [])
                        )
                        
                        st.session_state.test_results = test_results
            
            # Display test results (persistent)
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
                        with st.spinner("🤖 Auto-debugging..."):
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
            st.markdown("### 🔄 Refactoring Options")
            refactor_col1, refactor_col2, refactor_col3, refactor_col4 = st.columns(4)
            
            with refactor_col1:
                if st.button("📚 Readability", key="refactor_readability"):
                    with st.spinner("📖 Refactoring for readability..."):
                        result = st.session_state.oracle.refactor_code(project, "readability")
                        if result["success"]:
                            st.session_state.refactor_results["readability"] = result["refactored"]
            
            # Display readability refactor result (persistent)
            if "readability" in st.session_state.refactor_results:
                with st.expander("📚 Readability Refactor Result"):
                    st.markdown(st.session_state.refactor_results["readability"])
            
            with refactor_col2:
                if st.button("⚡ Performance", key="refactor_performance"):
                    with st.spinner("🚀 Optimizing performance..."):
                        result = st.session_state.oracle.refactor_code(project, "performance")
                        if result["success"]:
                            st.session_state.refactor_results["performance"] = result["refactored"]
            
            # Display performance refactor result (persistent)
            if "performance" in st.session_state.refactor_results:
                with st.expander("⚡ Performance Refactor Result"):
                    st.markdown(st.session_state.refactor_results["performance"])
            
            with refactor_col3:
                if st.button("📦 Size", key="refactor_size"):
                    with st.spinner("📉 Minimizing size..."):
                        result = st.session_state.oracle.refactor_code(project, "size")
                        if result["success"]:
                            st.session_state.refactor_results["size"] = result["refactored"]
            
            # Display size refactor result (persistent)
            if "size" in st.session_state.refactor_results:
                with st.expander("📦 Size Refactor Result"):
                    st.markdown(st.session_state.refactor_results["size"])
            
            with refactor_col4:
                if st.button("🛡️ Security", key="refactor_security"):
                    with st.spinner("🔒 Enhancing security..."):
                        result = st.session_state.oracle.refactor_code(project, "security")
                        if result["success"]:
                            st.session_state.refactor_results["security"] = result["refactored"]
            
            # Display security refactor result (persistent)
            if "security" in st.session_state.refactor_results:
                with st.expander("🛡️ Security Refactor Result"):
                    st.markdown(st.session_state.refactor_results["security"])
    
    with tab3:
        st.markdown("### 🔍 Code Analysis & Insights")
        
        if not st.session_state.current_project:
            st.markdown('<div class="info-box">ℹ️ Generate a project first to see analysis options</div>', unsafe_allow_html=True)
        else:
            project = st.session_state.current_project
            
            # Code explanation
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
            
            # Display explanation (persistent)
            if explain_file in st.session_state.explanations:
                with st.expander(f"📖 Explanation: {explain_file}"):
                    st.markdown(st.session_state.explanations[explain_file])
            
            # Architecture visualization
            st.markdown("### 🏗️ Architecture Overview")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📊 Visualize Architecture", key="viz_arch_btn"):
                    # Create a simple architecture diagram
                    files = list(project['files'].keys())
                    file_types = {}
                    
                    for file in files:
                        ext = file.split('.')[-1] if '.' in file else 'other'
                        file_types[ext] = file_types.get(ext, 0) + 1
                    
                    # Store visualization data in session state
                    st.session_state.arch_viz_data = file_types
            
            # Display architecture visualization (persistent)
            if hasattr(st.session_state, 'arch_viz_data'):
                # Create pie chart of file types
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
                
                # Dependency graph (simplified)
                st.markdown("### 📦 Dependencies")
                deps = project.get('dependencies', [])
                if deps:
                    dep_df = pd.DataFrame({'Dependency': deps, 'Type': ['External'] * len(deps)})
                    st.dataframe(dep_df, use_container_width=True)
                else:
                    st.info("No external dependencies found")
            
            # Code metrics
            st.markdown("### 📏 Code Metrics")
            
            st.markdown("### 📏 Code Metrics")
           
            if hasattr(st.session_state, 'project_metrics') and st.session_state.project_metrics:
               metrics = st.session_state.project_metrics
               col1, col2, col3, col4 = st.columns(4)
               col1.metric("Total Files", metrics['total_files'])
               col2.metric("Total Lines", metrics['total_lines'])
               col3.metric("Avg Lines/File", metrics['avg_lines_per_file'])
               col4.metric("Dependencies", metrics['dependencies'])
            elif st.session_state.current_project:
               # Fallback calculation if metrics not available
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
    
    with tab4:
        st.markdown("### 📊 Project Health Dashboard")
        
        if not st.session_state.current_project:
            st.markdown('<div class="info-box">ℹ️ Generate a project first to see the dashboard</div>', unsafe_allow_html=True)
        else:
            project = st.session_state.current_project
            
            # Health score calculation (mock)
            health_score = 85  # This would be calculated based on various metrics
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("🏥 Health Score", f"{health_score}%", "5%")
            with col2:
                test_coverage = "78%" if st.session_state.test_results and st.session_state.test_results["success"] else "0%"
                st.metric("🧪 Test Coverage", test_coverage, "12%")
            with col3:
                security_rating = "A-" if "security" in st.session_state.refactor_results else "C"
                st.metric("🛡️ Security Rating", security_rating, "0")
            
            # Project timeline (mock data)
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
            
            # Code quality trends (mock chart)
            st.markdown("### 📈 Quality Trends")
            
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
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white'
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with tab5:
        st.markdown("### 🛡️ Security Analysis")
        
        if not st.session_state.current_project:
            st.markdown('<div class="info-box">ℹ️ Generate a project first to run security analysis</div>', unsafe_allow_html=True)
        else:
            project = st.session_state.current_project
            
            if st.button("🔍 Run Security Scan", key="security_scan_btn"):
                with st.spinner("🛡️ Scanning for security vulnerabilities..."):
                    security_result = st.session_state.oracle.security_scan(project, language)
                    st.session_state.security_report = security_result
            
            # Display security report (persistent)
            if st.session_state.security_report:
                if st.session_state.security_report["success"]:
                    st.markdown("### 🛡️ Security Report")
                    st.markdown(st.session_state.security_report["report"])
                else:
                    st.error(f"Security scan failed: {st.session_state.security_report['error']}")
            
            # Security checklist
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
    
    with tab6:
        st.markdown("### 🪄 Deployment & CI/CD")
        
        if not st.session_state.current_project:
            st.markdown('<div class="info-box">ℹ️ Generate a project first to see deployment options</div>', unsafe_allow_html=True)
        else:
            project = st.session_state.current_project
            
            # CI/CD platform selection
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
                
                # Display CI/CD config (persistent)
                if cicd_platform in st.session_state.cicd_configs:
                    st.code(st.session_state.cicd_configs[cicd_platform], language="yaml")
                    
                    # Download CI/CD config
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
                
                # Display Dockerfile (persistent)
                if hasattr(st.session_state, 'dockerfile_content'):
                    st.code(st.session_state.dockerfile_content, language="dockerfile")
                    
                    st.download_button(
                        label="📥 Download Dockerfile",
                        data=st.session_state.dockerfile_content,
                        file_name="Dockerfile",
                        mime="text/plain",
                        key="download_dockerfile"
                    )
            
            # Deployment scripts
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
            
            # Display deployment config (persistent)
            if hasattr(st.session_state, 'deploy_configs') and deployment_type in st.session_state.deploy_configs:
                st.code(st.session_state.deploy_configs[deployment_type], language="yaml")
                
                # Determine file extension based on deployment type
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
            
            # Environment management
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
            
            # Display environment config (persistent)
            if hasattr(st.session_state, 'env_configs') and env_type in st.session_state.env_configs:
                st.code(st.session_state.env_configs[env_type], language="bash")
                
                st.download_button(
                    label=f"📥 Download {env_type} Config",
                    data=st.session_state.env_configs[env_type],
                    file_name=f".env.{env_type.lower()}",
                    mime="text/plain",
                    key=f"download_env_{env_type}"
                )

    # Footer with new theme
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

if __name__ == "__main__":
    main()
