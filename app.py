# Import required libraries
import streamlit as st
import pandas as pd
import random
from utils import QuestionGenerator
import os

# Main class to handle quiz functionality
class QuizManager:
    def __init__(self):
        # Initialize empty lists to store questions, user answers and results
        self.questions = []
        self.user_answers = []
        self.results = []

    def generate_questions(self, generator, topic, question_type, difficulty, num_questions):
        # Reset all lists before generating new questions
        self.questions = []
        self.user_answers = []
        self.results = []

        try:
            # Generate specified number of questions
            for _ in range(num_questions):
                # Handle Multiple Choice Questions
                if question_type == "Multiple Choice":
                    question = generator.generate_mcq(topic, difficulty.lower())
                    self.questions.append({
                        'type': 'MCQ',
                        'question': question.question,
                        'options': question.options,
                        'correct_answer': question.correct_answer
                    })
                # Handle Fill in the Blank Questions
                else:
                    question = generator.generate_fill_blank(topic, difficulty.lower())
                    self.questions.append({
                        'type': 'Fill in the Blank',
                        'question': question.question,
                        'correct_answer': question.answer
                    })
        except Exception as e:
            # Display error if question generation fails
            st.error(f"Error generating questions: {e}")
            return False
        return True

    def attempt_quiz(self):
        # Display questions and collect user answers
        for i, q in enumerate(self.questions):
            # Display question with bold formatting
            st.markdown(f"**Question {i+1}: {q['question']}**")
            
            # Handle MCQ input using radio buttons
            if q['type'] == 'MCQ':
                user_answer = st.radio(
                    f"Select an answer for Question {i+1}", 
                    q['options'], 
                    key=f"mcq_{i}"
                )
                self.user_answers.append(user_answer)
            # Handle Fill in the Blank input using text input
            else:
                user_answer = st.text_input(
                    f"Fill in the blank for Question {i+1}", 
                    key=f"fill_blank_{i}"
                )
                self.user_answers.append(user_answer)

    def evaluate_quiz(self):
        # Reset results before evaluation
        self.results = []
        # Evaluate each question and user answer pair
        for i, (q, user_ans) in enumerate(zip(self.questions, self.user_answers)):
            # Create base result dictionary
            result_dict = {
                'question_number': i + 1,
                'question': q['question'],
                'question_type': q['type'],
                'user_answer': user_ans,
                'correct_answer': q['correct_answer'],
                'is_correct': False
            }
            
            # Evaluate MCQ answers
            if q['type'] == 'MCQ':
                result_dict['options'] = q['options']
                result_dict['is_correct'] = user_ans == q['correct_answer']
            # Evaluate Fill in the Blank answers
            else:
                result_dict['options'] = []
                result_dict['is_correct'] = user_ans.strip().lower() == q['correct_answer'].strip().lower()
            
            self.results.append(result_dict)

    def generate_result_dataframe(self):
        # Convert results to pandas DataFrame
        if not self.results:
            return pd.DataFrame()
        return pd.DataFrame(self.results)

    def save_to_csv(self, filename='quiz_results.csv'):
        try:
            # Check if results exist
            if not self.results:
                st.warning("No results to save. Please complete the quiz first.")
                return None
            
            # Generate DataFrame from results
            df = self.generate_result_dataframe()
            
            # Create unique filename with timestamp
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            unique_filename = f"quiz_results_{timestamp}.csv"
            
            # Ensure results directory exists
            os.makedirs('results', exist_ok=True)
            full_path = os.path.join('results', unique_filename)
            
            # Save results to CSV
            df.to_csv(full_path, index=False)
            
            # Display success message
            st.success(f"Results saved to {full_path}")
            return full_path
        except Exception as e:
            # Handle any errors during saving
            st.error(f"Failed to save results: {e}")
            return None

def main():
    # Configure Streamlit page
    st.set_page_config(page_title="UPSC & PCS Question Generator", page_icon="📝")
    
    # Initialize session state variables
    if 'quiz_manager' not in st.session_state:
        st.session_state.quiz_manager = QuizManager()
    if 'quiz_generated' not in st.session_state:
        st.session_state.quiz_generated = False
    if 'quiz_submitted' not in st.session_state:
        st.session_state.quiz_submitted = False

    # Set page title
    st.title("UPSC & PCS Question Generator")

    # Create sidebar for quiz settings
    st.sidebar.header("Quiz Settings")
    
    # API selection dropdown
    api_choice = st.sidebar.selectbox(
        "Select API", 
        ["Groq"], 
        index=0
    )

    # Question type selection
    question_type = st.sidebar.selectbox(
        "Select Question Type", 
        ["Multiple Choice", "Fill in the Blank"], 
        index=0
    )

    # Topic input field
    topic = st.sidebar.text_input(
        "Enter Topic", 
        placeholder="Indian History, Geography, etc."
    )

    # Difficulty level selection
    difficulty = st.sidebar.selectbox(
        "Difficulty Level", 
        ["Easy", "Medium", "Hard"], 
        index=1
    )

    # Number of questions input
    num_questions = st.sidebar.number_input(
        "Number of Questions", 
        min_value=1, 
        max_value=10, 
        value=5
    )

    # Generate quiz button handler
    if st.sidebar.button("Generate Quiz"):
        st.session_state.quiz_submitted = False
        generator = QuestionGenerator()
        st.session_state.quiz_generated = st.session_state.quiz_manager.generate_questions(
            generator, topic, question_type, difficulty, num_questions
        )
        st.rerun()

    # Display quiz if generated
    if st.session_state.quiz_generated and st.session_state.quiz_manager.questions:
        st.header("Quiz")
        st.session_state.quiz_manager.attempt_quiz()
        
        # Submit quiz button handler
        if st.button("Submit Quiz"):
            st.session_state.quiz_manager.evaluate_quiz()
            st.session_state.quiz_submitted = True
            st.rerun()
    
    # Display results if quiz is submitted
    if st.session_state.quiz_submitted:
        st.header("Quiz Results")
        results_df = st.session_state.quiz_manager.generate_result_dataframe()
        
        # Show results if available
        if not results_df.empty:
            # Calculate and display score
            correct_count = results_df['is_correct'].sum()
            total_questions = len(results_df)
            score_percentage = (correct_count / total_questions) * 100
            
            st.write(f"Score: {correct_count}/{total_questions} ({score_percentage:.1f}%)")
            
            # Display detailed results for each question
            for _, result in results_df.iterrows():
                question_num = result['question_number']
                if result['is_correct']:
                    st.success(f"✅ Question {question_num}: {result['question']}")
                else:
                    st.error(f"❌ Question {question_num}: {result['question']}")
                    st.write(f"Your Answer: {result['user_answer']}")
                    st.write(f"Correct Answer: {result['correct_answer']}")
                
                st.markdown("---")
            
            # Save results button handler
            if st.button("Save Results"):
                saved_file = st.session_state.quiz_manager.save_to_csv()
                if saved_file:
                    with open(saved_file, 'rb') as f:
                        st.download_button(
                            label="Download Results",
                            data=f.read(),
                            file_name=os.path.basename(saved_file),
                            mime='text/csv'
                        )
        else:
            st.warning("No results available. Please complete the quiz first.")

# Entry point of the application
if __name__ == "__main__":
    main()