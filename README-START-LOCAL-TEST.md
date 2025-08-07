# 🚀 Start Local Test Environment

This guide explains how to start the **Charlotte Everley** project locally for quick testing.

---

## 📂 Prerequisites

- **Python 3** installed  
- Terminal access (macOS, Linux, or Windows with Git Bash)
- This repository cloned locally

---

## ▶️ Quick Start

You can start the local server in **two ways**:

### 1. Using the Project Script
```bash
./prj-start-local-test.sh
````

This will:

* Start the server using the project’s `charlotteeverley-site/runserver.sh`
* Output a URL to open in your browser

### 2. Using the Python HTTP Server

```bash
./start-local-test.sh
```

This will:

* Start a simple Python server at `http://localhost:8000/`
* Serve files directly from the repo

---

## 🔗 Access in Browser

After running either script, open:

```
http://localhost:8000/charlotteeverley-site/gallery.html
```

Or, if the project script starts a custom server, follow the on-screen instructions.

---

## 🛑 Stop the Server

Press:

```
CTRL + C
```

in the terminal where the server is running.

---

## 💡 Notes

* If you make changes to HTML, CSS, or JS files, simply refresh your browser — no need to restart the server.
* For membership banner testing, verify clicks go to:

```
https://charlotteeverley.foundral.tech/membership/free/
```
