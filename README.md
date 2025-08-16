<div align="center">
  <h1 align="center">
    <span style="font-size: 4rem;">♾️</span>
    <br>
    Singularity-AI
  </h1>
  <p align="center">
    <strong>Autonomous Software Engineering Assistant</strong>
  </p>
  <p align="center">
    Where AI meets infinity. Generate, test, debug, and deploy code with the power of generative AI.
  </p>
</div>

<p align="center">
  <img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License">
  <img src="https://img.shields.io/badge/Language-Python-3776AB.svg" alt="Language">
  <img src="https://img.shields.io/badge/Framework-Streamlit-FF4B4B.svg" alt="Framework">
  <img src="https://img.shields.io/badge/AI-Google_Gemini-4285F4.svg" alt="AI">
</p>

---

## 🚀 Introduction

Singularity-AI is a powerful and intuitive Streamlit application that acts as an autonomous software engineering assistant. It leverages the capabilities of Google's Gemini large language model to provide a seamless experience for generating, testing, debugging, refactoring, and deploying software projects. Whether you're a seasoned developer looking to accelerate your workflow or a beginner learning to code, Singularity-AI is your go-to tool for building high-quality software.

## ✨ Features

- **Project Generation:** Describe your project in natural language and watch as Singularity-AI generates a complete, multi-file project structure with production-ready code.
- **Automated Testing:** Automatically run tests for your generated projects to ensure code quality and correctness.
- **Autonomous Debugging:** If tests fail, Singularity-AI can autonomously analyze the errors and attempt to fix the code.
- **Code Refactoring:** Refactor your code for readability, performance, size, or security with a single click.
- **In-depth Code Analysis:** Get detailed explanations of your code, including complexity analysis and suggestions for improvement.
- **Security Scanning:** Perform security analysis on your projects to identify and mitigate potential vulnerabilities.
- **CI/CD and Deployment:** Generate CI/CD configurations for popular platforms like GitHub Actions and create deployment scripts for Docker, Kubernetes, and more.
- **Interactive Dashboard:** Visualize project metrics, health scores, and quality trends over time.

## 🛠️ Installation & Setup

Follow these steps to get Singularity-AI up and running on your local machine.

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/Singularity-AI.git
cd Singularity-AI
```

### 2. Create a Virtual Environment

It's recommended to use a virtual environment to manage dependencies.

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### 3. Install Dependencies

Install the required Python packages using pip.

```bash
pip install -r requirements.txt
```

### 4. Set Up Your API Key

Singularity-AI uses the Google Gemini API. You'll need to get an API key from the [Google AI Studio](https://aistudio.google.com/).

Once you have your key, create a `.env` file in the root of the project directory by copying the example file:

```bash
cp .env.example .env
```

Now, open the `.env` file and add your Gemini API key:

```
GEMINI_API_KEY="YOUR_API_KEY_HERE"
```

## 🏃‍♀️ How to Run

With the setup complete, you can run the Streamlit application with a single command:

```bash
streamlit run src/main.py
```

This will start the application, and you can access it in your web browser at `http://localhost:8501`.

## 📖 How to Use

1.  **Configure Your Project:** Use the sidebar to select the programming language and architecture pattern for your project.
2.  **Generate a Project:** In the "Generate" tab, describe the project you want to build and click "Generate Project".
3.  **Build and Test:** Once your project is generated, head to the "Build & Test" tab to run build commands and execute tests.
4.  **Analyze and Refactor:** Use the "Analysis" tab to get code explanations and the "Build & Test" tab to refactor your code.
5.  **Deploy:** In the "Deploy" tab, generate CI/CD configurations, Dockerfiles, and deployment scripts for your project.

## 🙌 Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

Please see the [CONTRIBUTING.md](CONTRIBUTING.md) file for details on how to contribute to the project.

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
