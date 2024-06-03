import os 
import streamlit as st
import replicate
os.environ["REPLICATE_API_TOKEN"] = "r8_QiBcZr5wLin9KBFjNS5465464W2XeUoAO73XDao3"


# pre_prompt = "You are a helpful assistant. You do not respond as 'User' or pretend to be 'User'. You only respond once as 'Assistant'."

# question genration function

def generate_question(topic):
    prompt_input = f"Generate a simple and easy question based on the topic: {topic}."
    
    output = replicate.run(
        'a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5', 
        input={"prompt": f" {prompt_input} Assistant: ", 
               "temperature": 0.9, "top_p": 0.9, "max_length": 100, "repetition_penalty": 1}
    )
    
    full_response = "".join(output)
    return full_response.strip()

#  answer verification function

def verify_answer(question, user_answer):
    prompt_input = f"Question: {question}\nUser's Answer: {user_answer}\nIs the user's answer correct? Respond with 'Correct' or 'Incorrect' only."
    
    output = replicate.run(
        'a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5', 
        input={"prompt": f"{prompt_input} Assistant: ", 
               "temperature": 0.1, "top_p": 0.9, "max_length": 50, "repetition_penalty": 1}
    )
    
    full_response = "".join(output)
    return full_response.strip()

# Initialize session state
if 'question' not in st.session_state:
    st.session_state.question = ""

# Streamlit UI
st.title("Simple Question Generator and Answer Validator")

# Dropdown menu for selecting a topic
topics = ["Geography", "Health", "Sports"]
selected_topic = st.selectbox("Select a topic for the question:", topics)

#  question button
if st.button("Generate Question"):
    st.session_state.question = generate_question(selected_topic)
    st.write(f"Generated Question: {st.session_state.question}")

# Input box for user's answer
user_answer = st.text_input("Your Answer:")

# verify button
if st.button("Verify Answer"):
    if st.session_state.question:
        verification_result = verify_answer(st.session_state.question, user_answer)
        st.write(verification_result)
    else:
        st.write("Please generate a question first.")

