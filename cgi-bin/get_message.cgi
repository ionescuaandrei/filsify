#!/bin/bash

echo "Content-Type: text/html"
echo ""

echo "<!DOCTYPE html>"

mysql -u chatuser -pChatPassword! -D chatapp -e "SELECT username, message FROM messages ORDER BY timestamp DESC LIMIT 10;" | tail -n +2 | while read -r username message; do
    echo "<li><strong>$username:</strong> $message</li>"
done

echo "</ul></body></html>"

