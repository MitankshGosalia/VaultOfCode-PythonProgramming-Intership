from flask import Flask, render_template_string, request

app = Flask(__name__)

# Store messages
chat_log = []

# HTML template for the web page
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>AI Encoder and Decoder </title>
    <style>
        body {
            background-color: #1e1e1e;
            color: #fff;
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
        }
        .container {
            background-color: #282828;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 0 15px rgba(0, 0, 0, 0.2);
            width: 80%;
            max-width: 700px;
        }
        h1 {
            text-align: center;
            margin-bottom: 30px;
        }
        .input-container {
            display: flex;
            align-items: center;
            margin-bottom: 20px;
        }
        .input-container input {
            flex-grow: 1;
            padding: 15px;
            border: 1px solid #555;
            border-radius: 5px;
            margin-right: 10px;
            background-color: #333;
            color: #fff;
        }
        .input-container button[type="submit"] {
            padding: 15px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            background-color: #4CAF50;
            color: white;
            margin-right: 10px;
        }
        .input-container button[type="submit"]:hover {
            background-color: #45a049;
        }
        .input-container input[type="number"] {
            width: 80px;
            padding: 15px;
            border: 1px solid #555;
            border-radius: 5px;
            margin-right: 10px;
            background-color: #333;
            color: #fff;
        }
        .input-container .icon {
            width: 20px;
            height: 20px;
            fill: white;
            margin-right: 10px;
        }
        .chat-log {
            padding: 20px;
            border: 1px solid #555;
            border-radius: 5px;
            background-color: #333;
            color: #fff;
            overflow-y: auto;
            max-height: 400px;
        }
        .chat-log .message {
            margin-bottom: 15px;
            padding: 15px;
            border-radius: 5px;
        }
        .chat-log .user-message {
            background-color: #007bff;
            text-align: right;
        }
        .chat-log .bot-message {
            background-color: #ffc107;
            text-align: left;
        }
        .copy-button {
            cursor: pointer;
            padding: 5px;
            margin-left: 10px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
        }
    </style>
    <script>
        function copyToClipboard(text) {
            navigator.clipboard.writeText(text).then(function() {
                alert('Copied to clipboard!');
            }, function(err) {
                console.error('Async: Could not copy text: ', err);
            });
        }
    </script>
</head>
<body>
    <div class="container">
        <h1>AI Encoder and Decoder </h1>
        <form method="post">
            <div class="input-container">
                <input type="text" name="message" placeholder="Type your message here..." required>
                <input type="number" name="shift" placeholder="Enter shift number" required>
                <button type="submit" name="action" value="encode">
                    <svg class="icon" viewBox="0 0 24 24">
                        <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 14.5v-9l6 4.5-6 4.5z" />
                    </svg>
                </button>
                <button type="submit" name="action" value="decode">
                    <svg class="icon" viewBox="0 0 24 24">
                        <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 14.5v-9l-6 4.5 6 4.5z" />
                    </svg>
                </button>
                <button type="submit" name="action" value="send">
                     <svg class="arrow" viewBox="0 0 24 24">
                         <path d="M16.01 11H4v2h12.01v3L20 12l-3.99-4z" />
                     </svg>
               </button>
            </div>
        </form>
        <div class="chat-log">
            {% if chat_log %}
                {% for message in chat_log %}
                    <div class="message {% if message['is_user'] %}user-message{% else %}bot-message{% endif %}">
                        <strong>{{ message['username'] }}:</strong> {{ message['text'] }}
                        {% if not message['is_user'] %}
                            <button class="copy-button" onclick="copyToClipboard('{{ message['text'] }}')">Copy</button>
                        {% endif %}
                    </div>
                {% endfor %}
            {% endif %}
        </div>
    </div>
</body>
</html>
"""

def shift_letter(letter, shift, encode=True):
    if letter.isalpha():
        ascii_offset = 65 if letter.isupper() else 97
        shift = shift if encode else -shift
        return chr((ord(letter) - ascii_offset + shift) % 26 + ascii_offset)
    return letter

def process_message(message, shift, encode=True):
    return ''.join(shift_letter(char, shift, encode) for char in message)

@app.route('/', methods=['GET', 'POST'])
def index():
    global chat_log
    result = None
    if request.method == 'POST':
        message = request.form['message']
        shift = int(request.form['shift'])
        action = request.form['action']

        if action == 'encode':
            result = process_message(message, shift, encode=True)
        elif action == 'decode':
            result = process_message(message, shift, encode=False)
        elif action == 'send':
            result = message

        # Store the original message and the result
        chat_log.append({'is_user': True, 'username': 'User', 'text': message})
        chat_log.append({'is_user': False, 'username': 'Bot', 'text': result})
        
    return render_template_string(HTML_TEMPLATE, chat_log=chat_log)

if __name__ == '__main__':
    app.run(debug=True)
