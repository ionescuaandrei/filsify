# Chat App - OS-HW Project

This repository contains the code for a simple chat application developed as part of an Operating Systems course. The application is designed to facilitate private communication between two users, emphasizing simplicity and privacy.

## How to Run This App

### 1. Prerequisites

Ensure that you have the following installed on your system:
- **Linux Debian 12** (or a similar distribution)
- **Apache2** (with CGI enabled)
- **MariaDB**
- **ncat** (for real-time updates)

### 2. Setting Up the Environment

#### Apache2 Installation and Configuration:
- Install Apache2:
  ```bash
  sudo apt-get update
  sudo apt-get install apache2
  ```
- Enable the CGI module:
  ```bash
  sudo a2enmod cgi
  sudo systemctl restart apache2
  ```
- Verify the CGI configuration in `/etc/apache2/conf-enabled/serve-cgi-bin.conf`.
- Restart the Apache2 service after making changes:
  ```bash
  sudo systemctl restart apache2
  ```

#### MariaDB Installation and Configuration:
- Install MariaDB:
  ```bash
  sudo apt-get install mariadb-server
  sudo systemctl start mariadb
  ```
- Create the database and user:
  ```sql
  CREATE DATABASE chatapp;
  CREATE USER 'chatuser'@'localhost' IDENTIFIED BY 'ChatPassword!';
  GRANT ALL PRIVILEGES ON chatapp.* TO 'chatuser'@'localhost';
  FLUSH PRIVILEGES;
  ```
- Create the `messages` table:
  ```sql
  USE chatapp;
  CREATE TABLE messages (
      id INT AUTO_INCREMENT PRIMARY KEY,
      username VARCHAR(50),
      message TEXT,
      timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  );
  ```

### 3. Setting Up the Application

#### CGI Scripts:
- Navigate to the CGI directory:
  ```bash
  cd /usr/lib/cgi-bin
  ```
- Create the `get_message.cgi` script:
  ```bash
  touch get_message.cgi
  chmod 777 get_message.cgi
  ```
  Script content:
  ```bash
  #!/bin/bash

  echo "Content-Type: text/html"
  echo ""

  echo "<!DOCTYPE html>"
  echo "<html><body><ul>"

  mysql -u chatuser -pChatPassword! -D chatapp -e "SELECT username, message FROM messages ORDER BY timestamp DESC LIMIT 10;" | tail -n +2 | while read -r username message; do
      echo "<li><strong>$username:</strong> $message</li>"
  done

  echo "</ul></body></html>"
  ```
- Create the `save_message.cgi` script:
  ```bash
  touch save_message.cgi
  chmod 777 save_message.cgi
  ```
  Script content:
  ```bash
  #!/bin/bash

  echo "Content-Type: text/plain"
  echo ""

  if [ -z "$CONTENT_LENGTH" ]; then
      echo "No POST data received."
      exit 1
  fi

  read -n $CONTENT_LENGTH POST_DATA

  USERNAME=$(echo "$POST_DATA" | grep -oP 'username=\K[^&]+')
  MESSAGE=$(echo "$POST_DATA" | grep -oP 'message=\K.*' | sed 's/%\([0-9A-Fa-f][0-9A-Fa-f]\)/\\x\1/g' | xargs -0 printf "%b")

  mysql -u chatuser -pChatPassword! -D chatapp -e "INSERT INTO messages (username, message) VALUES ('$USERNAME', '$MESSAGE');" 2>&1

  echo "$USERNAME: $MESSAGE" | ncat --send-only localhost 12345 2>&1

  echo "Message saved and broadcasted!"
  ```

#### Frontend:
- Place the `index.html` file in the appropriate directory (e.g., `/var/www/html`).
  ```html
  <!DOCTYPE html>
  <html>
  <head>
      <title>Minimal Chat App</title>
  </head>
  <body>
      <h1>Chat App</h1>

      <!-- Form to send a message -->
      <form method="POST" action="/cgi-bin/save_message.cgi">
          <input type="text" name="username" placeholder="Username" required>
          <input type="text" name="message" placeholder="Message" required>
          <button type="submit">Send</button>
      </form>

      <h2>Recent Messages</h2>
      <iframe src="/cgi-bin/get_message.cgi" width="100%" height="200"></iframe>

      <h2>Real-Time Updates</h2>
      <p>To get real-time messages, use the following command in your terminal:</p>
      <pre><strong>ncat localhost 12345</strong></pre>
  </body>
  </html>
  ```

### 4. Running the Application

1. Open a browser and navigate to `http://localhost` to access the chat interface.
2. Open two terminal windows:
   - **First Terminal:** Start the Apache2 server if it is not already running:
     ```bash
     sudo systemctl start apache2
     ```
   - **Second Terminal:** Start listening for real-time messages on port `12345` using `ncat`:
     ```bash
     ncat -l 12345
     ```
3. Use the web interface to submit a message. The app will confirm that the message was saved successfully.
4. Return to the main page to see the submitted message displayed in the "Recent Messages" section.
5. Check the terminal where `ncat` is running to view real-time message updates.

### 5. Troubleshooting

- Ensure that all services (Apache2 and MariaDB) are running properly.
- Verify that the CGI scripts have the correct permissions and are in the right directory.
- Check the database connection and credentials if messages are not being saved or retrieved correctly.
- Confirm that the `ncat` command is installed and configured to listen on the specified port.

### 6. Future Improvements

- Add user authentication for enhanced security.
- Improve the frontend using CSS and JavaScript for a modern user experience.
- Implement group chat functionality.

Feel free to contribute or suggest further improvements to this project!

[![Watch the video](https://img.youtube.com/vi/https://www.youtube.com/watch?v=xmxb9OQx2MU/0.jpg)](https://www.youtube.com/watch?v=https://www.youtube.com/watch?v=xmxb9OQx2MU)


