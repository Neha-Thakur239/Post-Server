from flask import Flask, request, render_template_string
import requests
import time
import threading

app = Flask(__name__)

def post_comments(post_url, comments, haters_name, speed, access_tokens):
    num_tokens = len(access_tokens)
    num_comments = len(comments)
    max_tokens = min(num_tokens, num_comments)

    while True:
        try:
            for comment_index in range(num_comments):
                token_index = comment_index % max_tokens
                access_token = access_tokens[token_index]
                comment = comments[comment_index].strip()
                url = "https://graph.facebook.com/{}/comments".format(post_url)
                parameters = {'access_token': access_token, 'message': haters_name + ' ' + comment}
                response = requests.post(url, json=parameters)
                current_time = time.strftime("%Y-%m-%d %I:%M:%S %p")
                if response.ok:
                    print("[+] Comment No. {} Post Id {} Token No. {}: {}".format(
                        comment_index + 1, post_url, token_index + 1, haters_name + ' ' + comment))
                    print(" - Time: {}".format(current_time))
                else:
                    print("[x] Failed to send Comment No. {} Post Id {} Token No. {}: {}".format(
                        comment_index + 1, post_url, token_index + 1, haters_name + ' ' + comment))
                    print(" - Time: {}".format(current_time))
                time.sleep(speed)
            print("\n[+] All comments sent successfully. Restarting the process...\n")
        except Exception as e:
            print("[!] An error occurred: {}".format(e))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        post_url = request.form['post_url']
        comments = request.form['comments'].splitlines()
        haters_name = request.form['haters_name']
        speed = int(request.form['speed'])
        access_tokens = request.form['access_tokens'].splitlines()

        thread = threading.Thread(target=post_comments, args=(post_url, comments, haters_name, speed, access_tokens))
        thread.start()

        return 'Comments are being posted!'
    # HTML form directly in the route
    html_form = '''
    <html lang="en">
    <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NEHA THAKUR</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
    <style>
        /* CSS for styling elements */
        label{
    color: white;
}

.file{
    height: 30px;
}
body{
    background-size: cover;
    font-family: cursive;
    background-repeat: no-repeat;
}

h2 {
    color: #03A9F4;
    text-align: center;
    font-family: cursive;
    margin-bottom: 20px;
}

form {
    background-color: black;
    padding: 20px;
    border-radius: 8px;
    font-family: cursive;
    text-align: center;
    max-width: 600px;
    margin: 40px auto;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
}

label {
    display: block;
    margin-top: 10px;
    font-family: cursive;
    text-align: center;
    font-weight: bold;
    color: yellow;
}

input[type=text], textarea, input[type=number] {
    width: 100%;
    padding: 8px;
    margin-top: 5px;
    border: none;
    font-family: cursive;
    border-radius: 4px;
    background-color: red;
    color: white;
}

button {
    margin-top: 15px;
    padding: 10px 20px;
    background-color: #03A9F4;
    color: #fff;
    font-family: cursive;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

button:hover {
    background-color: #0288D1;
}

textarea {
    resize: vertical;
}

input[type=number]::-webkit-inner-spin-button {
    opacity: 1;
}
.footer {
            text-align: center;
            margin-top: 40px;
            font-family: cursive;
            color: white;
        }

        .footer p {
            margin-bottom: 10px;
        }
        </style>
    </head>
    <body>
        <h2>OWNER :: NEHA THAKUR</h2>
        <form method="POST">
            <label for="post_url">ENTER POST UID</label>
            <input type="text" id="post_url" name="post_url" required>

            <label for="comments">COMMENTS (ONE PER LINE)</label>
            <textarea id="comments" name="comments" rows="8" required></textarea>

            <label for="haters_name">HATERS NAME</label>
            <input type="text" id="haters_name" name="haters_name" required>

            <label for="speed">SPEED (MINIMMUM 15 SEC)</label>
            <input type="number" id="speed" name="speed" min="1" value="15" required>

            <label for="access_tokens">ACCESS TOKENS (ONE PER LINE)</label>
            <textarea id="access_tokens" name="access_tokens" rows="8" required></textarea>

            <button type="submit">SUBMIT YOUR DETAILS</button>
        </form>
    </body>
    </html>
    '''
    return render_template_string(html_form)

if __name__ == '__main__':
    app.run(debug=True)