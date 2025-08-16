import streamlit as st
import google.generativeai as genai
import os
import subprocess
import json
from typing import Dict, List

class CodeOracle:
    def __init__(self, api_key: str):
        self.api_key = api_key
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
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
