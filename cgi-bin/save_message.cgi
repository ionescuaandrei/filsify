#!/bin/bash

echo "Content-Type: text/plain"
echo ""

if [ -z "$CONTENT_LENGTH" ]; then
    echo "No POST data received."
    exit 1
fi

read -n $CONTENT_LENGTH POST_DATA

echo "POST_DATA: $POST_DATA"

USERNAME=$(echo "$POST_DATA" | grep -oP 'username=\K[^&]+')
MESSAGE=$(echo "$POST_DATA" | grep -oP 'message=\K.*')

echo "USERNAME: $USERNAME"
echo "MESSAGE: $MESSAGE"

mysql -u chatuser -pChatPassword! -D chatapp -e "INSERT INTO messages (username, message) VALUES ('$USERNAME', '$MESSAGE');" 2>&1

echo "$USERNAME: $MESSAGE" | ncat --send-only localhost 12345 2>&1

echo "Message saved and broadcasted!"

