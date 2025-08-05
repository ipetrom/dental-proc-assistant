# 🦷 Dental Procedure Assistant - AI-Powered Documentation System

> **Educational Project & Concept Testing**  
> This is an educational proof-of-concept project designed to explore AI-powered solutions for healthcare documentation. It demonstrates how machine learning can assist medical professionals in streamlining routine administrative tasks.

## 🎯 Problem Statement

Modern healthcare professionals, particularly dentists, spend countless hours on paperwork and documentation. After each procedure, dentists must write detailed, professional descriptions of the treatment performed - a time-consuming process that takes valuable time away from patient care.

Our **Dental Procedure Assistant** addresses this challenge by leveraging AI to generate professional medical documentation templates, significantly reducing the administrative burden on healthcare providers.

## 💡 How It Works

The system uses historical dental procedure descriptions to intelligently generate dynamic templates with the most commonly used options:

### 1. **AI Template Generation**
- Analyzes existing procedure descriptions from `descriptions.json`
- Identifies patterns and recurring elements
- Generates structured templates with placeholders for variable information

### 2. **Smart Option Suggestions**
The system extracts the **3 most frequent options** for each field, for example:
- **Surface Type**: `okluzyjną` (occlusal), `mezjalną` (mesial), `dystalną` (distal)
- **Material Type**: `kompozyt bulk-fill`, `kompozyt nanohybrydowy`, `glasjonomer`
- **Tooth Number**: `26`, `45`, `36`
- **Procedure Class**: `klasy I`, `klasy II`, `klasy V`

### 3. **Flexible Input System**
- Provides **3 most common options** for quick selection
- Includes **"Other"** option for custom input when standard options don't fit
- Allows dentists to maintain precision while saving time

### 4. **Natural Language Output**
Generates professional, coherent descriptions like:
> *"Ząb 26 – ubytek klasy II obejmujący powierzchnie mezjalną i okluzyjną (MO). Koferdam, matryca sekcyjna + pierścień. Kompozyt bulk‑fill do 4 mm, warstwa wierzchnia nanohybrydowa. Punkt styczny prawidłowo odtworzony."*

## 🚀 Technology Stack

- **Backend**: Python, FastAPI
- **Frontend**: Streamlit for interactive UI
- **AI Integration**: OpenAI GPT-4 for intelligent text generation
- **Data Processing**: JSON-based procedure database
- **Template Engine**: Jinja2 for dynamic content rendering

## 📁 Project Structure

dentist_recommendation/
├── app.py                 # Streamlit application
├── main.py               # FastAPI backend
├── template_builder.py   # Core AI template generation logic
├── openai_utils.py       # OpenAI API integration
├── descriptions.json     # Training data with procedure descriptions
├── templates/            # HTML templates for web interface
└── tests.py             # Testing utilities

## 🎬 Demo Video

See the application in action below - demonstrating the complete workflow from procedure selection to final documentation generation:

*[Demo video would be attached here]*

## 🛠️ Installation & Setup

1. **Clone the repository**
```bash
git clone https://github.com/ipetrom/dentist_recommendation.git
cd dentist_recommendation
```

2. **Set up virtual environment**
```bash
python -m venv .venv
source .venv/bin/activate  # On Mac/Linux
```

3. **Install dependencies**
```bash
pip install streamlit openai python-dotenv fastapi uvicorn
```

4. **Configure OpenAI API**
```bash
echo "OPENAI_API_KEY=your_api_key_here" > .env
```

5. **Run the application**
```bash
# Streamlit interface
streamlit run app.py
```

## 🎯 Use Cases

- **Dental Clinics**: Streamline procedure documentation
- **Medical Training**: Educational tool for proper documentation practices
- **Healthcare IT**: Demonstration of AI integration in medical workflows
- **Research**: Analysis of medical documentation patterns

## 🔮 Future Enhancements

- Integration with dental practice management systems
- Multi-language support for international practices
- Advanced analytics on procedure patterns
- Voice-to-text integration for hands-free documentation
- HIPAA-compliant cloud deployment

## ⚠️ Disclaimer

This is an educational project intended for learning and concept demonstration purposes. It should not be used in production medical environments without proper validation, compliance checks, and medical professional oversight.

---

**Built with ❤️ for the healthcare community**

