#!/bin/bash

echo "📁 [Step 1] Creating Python virtual environment in ~/.venv ..."
echo python3 -m venv ~/.venv

echo "🚀 [Step 2] Activating virtual environment ..."
echo source ~/.venv/bin/activate

echo "📦 [Step 3] Installing requirements if requirements.txt exists ..."
if [ -f "requirements.txt" ]; then
    echo pip install --upgrade pip
    echo pip install -r requirements.txt
else
    echo "⚠️  No requirements.txt found, skipping pip install."
fi

echo "🛑 [Step 4] Deactivating virtual environment ..."
echo deactivate

echo "✅ Done. Virtual environment is ready at ~/.venv"


