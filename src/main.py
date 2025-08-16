import streamlit as st
import os
import tempfile
import subprocess
from dotenv import load_dotenv
from src.code_oracle import CodeOracle
from src.ui import (
    setup_page_config,
    load_custom_css,
    render_sidebar,
    render_main_content,
    render_generate_tab,
    render_project_overview,
    render_build_test_tab,
    render_analysis_tab,
    render_dashboard_tab,
    render_security_tab,
    render_deploy_tab,
    render_footer
)
from src.utils import create_project_files

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
    load_dotenv()
    init_session_state()
    setup_page_config()
    load_custom_css()

    language, architecture, max_debug_iterations, auto_test, auto_debug = render_sidebar()

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        st.error("⚠️ Please set your GEMINI_API_KEY in a .env file to continue")
        st.stop()

    if st.session_state.oracle is None:
        st.session_state.oracle = CodeOracle(api_key)
        st.success("✅ Singularity-AI Initialized!")

    tab1, tab2, tab3, tab4, tab5, tab6 = render_main_content()

    with tab1:
        prompt = render_generate_tab(language, architecture)
        if prompt:
            with st.spinner("🔮 Singularity-AI is crafting your project..."):
                project_data = st.session_state.oracle.generate_project(prompt, language, architecture)
                if project_data:
                    st.session_state.current_project = project_data
                    st.session_state.generation_status = "success"
                    total_lines = sum(len(content.split('\n')) for content in project_data['files'].values())
                    st.session_state.project_metrics = {
                        'total_files': len(project_data['files']),
                        'total_lines': total_lines,
                        'avg_lines_per_file': round(total_lines / len(project_data['files'])) if project_data.get('files') else 0,
                        'dependencies': len(project_data.get('dependencies', []))
                    }
                else:
                    st.session_state.generation_status = "error"

        render_project_overview(language, architecture)

    with tab2:
        action = render_build_test_tab(language, max_debug_iterations)
        if action == "build":
            with st.spinner("🏗️ Building project..."):
                temp_dir = tempfile.mkdtemp()
                create_project_files(st.session_state.current_project, temp_dir)
                build_success = True
                build_output = ""
                for cmd in st.session_state.current_project.get('build_commands', []):
                    try:
                        result = subprocess.run(cmd.split(), cwd=temp_dir, capture_output=True, text=True, timeout=60)
                        build_output += f"$ {cmd}\n{result.stdout}\n"
                        if result.returncode != 0:
                            build_success = False
                            build_output += f"Error: {result.stderr}\n"
                    except Exception as e:
                        build_success = False
                        build_output += f"Build failed: {str(e)}\n"
                st.session_state.build_output = {"success": build_success, "output": build_output}
        elif action == "test":
            with st.spinner("🔬 Running tests..."):
                temp_dir = tempfile.mkdtemp()
                create_project_files(st.session_state.current_project, temp_dir)
                test_results = st.session_state.oracle.run_tests(temp_dir, language, st.session_state.current_project.get('test_commands', []))
                st.session_state.test_results = test_results
        elif action == "debug":
            with st.spinner("🤖 Auto-debugging..."):
                debug_result = st.session_state.oracle.debug_and_fix(st.session_state.current_project, st.session_state.test_results, max_debug_iterations)
                if debug_result["success"]:
                    st.session_state.current_project = debug_result["updated_project"]
                    st.success("🔧 Auto-debug completed!")
                    st.markdown(debug_result["explanation"])
                else:
                    st.error(f"Auto-debug failed: {debug_result['error']}")
        elif action and action.startswith("refactor"):
            refactor_type = action.split("_")[1]
            with st.spinner(f"🔄 Refactoring for {refactor_type}..."):
                result = st.session_state.oracle.refactor_code(st.session_state.current_project, refactor_type)
                if result["success"]:
                    st.session_state.refactor_results[refactor_type] = result["refactored"]

    with tab3:
        render_analysis_tab(language)

    with tab4:
        render_dashboard_tab()

    with tab5:
        action = render_security_tab(language)
        if action == "scan":
            with st.spinner("🛡️ Scanning for security vulnerabilities..."):
                security_result = st.session_state.oracle.security_scan(st.session_state.current_project, language)
                st.session_state.security_report = security_result

    with tab6:
        render_deploy_tab(language)

    render_footer()

if __name__ == "__main__":
    main()
