# UPSC & PCS Quiz Generator
<img src ="https://github.com/Shivan118/Generative-AI-End-to-End-Project---UPSC-PCS-Education-Hub/blob/main/img.png" alt="MLBC">

### Problem Statement
The UPSC (Union Public Service Commission) and PCS (Provincial Civil Service) exam preparation process faces several challenges:

Limited access to quality practice questions
Difficulty in getting instant feedback on performance
Lack of personalized question difficulty adjustment
Time-consuming process of creating and evaluating practice tests
Need for comprehensive topic coverage across various subjects

This project addresses these challenges by providing an automated, AI-powered quiz generation system that creates customized practice questions for UPSC and PCS exam preparation.

### Industry Applications

1. Education & Test Prep

    - Coaching institutes
    - Online learning platforms
    - Self-study programs
    - Educational assessment tools

2. Competitive Exam Training

    - UPSC preparation centers
    - State PCS coaching
    - Government job exam preparation
    - Assessment centers

3. Corporate Training

    - Employee assessment
    - Professional development
    - Knowledge testing
    - Skill evaluation

## Tools & Technologies Used

### Core Technologies

    - Python 3.8+
    - Streamlit (for web interface)
    - Groq LLM API (for question generation)
    - Pandas (for data handling)

### Libraries & Frameworks

    - langchain-groq
    - pydantic
    - python-dotenv
    - streamlit
    - pandas

### Development Tools

    - VSCode/PyCharm (recommended IDE)
    - Git (version control)
    - Virtual Environment (venv)

### Project Setup

1. Clone the Repository
```bash
git clone <repository-url>
cd upsc-pcs-quiz-generator
```

2. Create Virtual Environment
```bash
conda create -p env python=3.10 -y
```

3. Install Dependencies
```bash
pip install -r requirements.txt
```

4. Environment Configuration Create a .env file in the root directory:
```bash
GROQ_API_KEY=your_groq_api_key_here
```

5. Run the Application
```bash
streamlit run app.py
```

### Project Structure
```bash
├── main.py                 # Main Streamlit application
├── utils.py               # Question generator utility
├── requirements.txt       # Project dependencies
├── .env                  # Environment variables
├── results/              # Generated quiz results
└── README.md            # Project documentation
```

### Features

1. Question Generation

    - Multiple choice questions
    - Fill in the blank questions
    - Customizable difficulty levels
    - Topic-specific questions

2. Quiz Management

    - Interactive quiz interface
    - Real-time scoring
    - Detailed feedback
    - Progress tracking

3. Result Analysis

    - Score calculation
    - Performance metrics
    - Exportable results
    - Historical data tracking

### Future Enhancements

1. Technical Improvements

    - Implement question caching for better performance
    - Add support for multiple LLM providers
    - Enhance error handling and retry mechanisms
    - Implement user authentication system

2. Feature Additions

    - Add more question types (matching, true/false, etc.)
    - Implement spaced repetition learning
    - Add progress tracking analytics
    - Include topic-wise performance analysis
    - Create custom quiz templates

3. User Experience

    - Add mobile-responsive design
    - Implement dark mode
    - Add multi-language support
    - Create user profile management
    - Add question difficulty auto-adjustment

4. Content & Integration

    - Integrate with study materials
    - Add pre-built question banks
    - Create topic suggestion system
    - Add collaborative quiz sharing
    - Implement peer comparison features
