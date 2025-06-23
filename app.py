from flask import Flask, request, render_template, session, redirect, url_for
import ollama
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-123'

# Initialize conversation history
def init_conversation():
    session['conversation'] = []
    session['mode'] = None

@app.route("/", methods=["GET", "POST"])
def home():
    if 'conversation' not in session:
        init_conversation()
    
    if request.method == "POST":
        # Handle mode selection
        if 'mode' in request.form:
            session['mode'] = request.form['mode']
            return redirect(url_for('home'))
        
        # Handle user query
        query = request.form.get("query", "").strip()
        if query:
            return process_query(query)
        
        # Handle feedback
        if 'feedback' in request.form:
            return handle_feedback(request.form['feedback'])
    
    return render_template("index.html", 
                         conversation=session['conversation'],
                         mode=session['mode'])

def process_query(query):
    prompt = ""
    if session['mode'] == 'answer':
        prompt = f"Answer this question concisely: {query}"
    elif session['mode'] == 'summarize':
        prompt = f"Summarize this text in 3 bullet points:\n{query}"
    elif session['mode'] == 'generate':
        prompt = f"Generate creative text about: {query}"
    elif session['mode'] == 'fun':
        prompt = f"Respond in a funny way to: {query}"
    
    try:
        response = ollama.chat(
            model='llama3',
            messages=[{'role': 'user', 'content': prompt}]
        )
        ai_response = response['message']['content']
        session['conversation'].extend([
            {'role': 'user', 'content': query},
            {'role': 'assistant', 'content': ai_response}
        ])
    except Exception as e:
        ai_response = f"Error: {str(e)}"
    
    return render_template("index.html",
                         conversation=session['conversation'],
                         mode=session['mode'],
                         show_feedback=True)

def handle_feedback(feedback):
    print(f"Feedback received: {feedback}")
    return render_template("index.html",
                         conversation=session['conversation'],
                         mode=session['mode'])

if __name__ == "__main__":
    app.run(debug=True)