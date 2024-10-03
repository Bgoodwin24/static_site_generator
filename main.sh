python3 src/main.py

cd public && python3 -m http.server 8888 &

sleep 2

if ! nc -z localhost 8888; then
    echo "Port 8888 is already in use or the server failed to start."
    exit 1
else
    echo "Server started successfully on port 8888!"
fi
