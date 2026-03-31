# ⚙️ Reparo — AI-Assisted Self-Healing Compiler

> *A smart compiler that doesn't just throw errors — it helps you fix them.*

---

## 🚀 Overview

**Reparo** is a custom-built compiler and programming language called **Replon** (`.rpl` files), built from scratch in Python with a focus on developer experience.

Unlike traditional compilers that simply stop at errors, Reparo introduces a **self-healing engine** that:

- Detects errors
- Explains them clearly with line and column info
- Suggests possible fixes
- *(Future)* Automatically corrects code using AI

---

## 🧠 Key Features

### 🔹 Replon Language

- Simple, clean syntax inspired by Python
- Supports integers, floats, strings, booleans, null
- Arithmetic, comparison, and logical operators
- `if` / `elif` / `else` blocks
- `while` loops
- `print()` statements
- Single-line comments with `#`

### 🔹 Lexer (Tokenisation Engine)

- Reads raw `.rpl` source code character by character
- Produces a structured token stream
- Tracks line and column numbers for every token
- Supports: identifiers, numbers (int + float), strings, keywords, operators, punctuation

### 🔹 Parser (AST Builder)

- Recursive-descent parser
- Builds an Abstract Syntax Tree (AST) from the token stream
- Correct operator precedence: `*` and `/` bind tighter than `+` and `-`
- Handles: assignments, print, if/elif/else, while, unary operators, grouped expressions

### 🔹 Self-Healing Engine *(coming soon)*

- Will detect and classify errors automatically
- Suggest fixes for common mistakes
- Evolving into a full AI-powered correction system

---

## 🧩 Current Architecture

```
Source Code (.rpl)
        │
        ▼
    [ Lexer ]  ──────────────────► Token Stream
        │
        ▼
   [ Parser ]  ──────────────────► Abstract Syntax Tree (AST)
        │
        ▼
[ Semantic Analyser ]  ──────────► (stub — coming next)
        │
        ▼
  [ Interpreter ]  ───────────────► (stub — coming next)
        │
        ▼
[ AI Self-Healing Engine ]  ──────► (stub — future)
```

---

## 📂 Project Structure

```
reparo/
│
├── main.py                  ← fallback entry point (python main.py)
├── reparo_cli.py            ← CLI entry point (reparo run / lex / parse)
├── setup.py                 ← installs the `reparo` command
│
├── lexer/
│   ├── tokens.py            ← Token class + token type constants + KEYWORDS
│   ├── lexer.py             ← Lexer — converts source text to tokens
│   ├── main.py              ← standalone lexer runner (dev use)
│   └── tests/
│       └── test1.rpl        ← sample Replon program
│
├── parser/
│   ├── parser.py            ← Recursive-descent parser
│   └── ast/
│       └── nodes.py         ← All AST node classes
│
├── semantic/
│   └── analyzer.py          ← Semantic analyser (stub)
│
├── executor/
│   └── interpreter.py       ← Tree-walk interpreter (stub)
│
└── ai_engine/
    ├── bug_detector.py      ← Bug detection engine (stub)
    └── error_fixer.py       ← Fix suggestion engine (stub)
```

---

## ▶️ Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/reparo.git
cd reparo
```

### 2. Install the `reparo` command

```bash
pip install -e .
```

This registers `reparo` as a shell command — just like `python` — so you can run it from anywhere.

### 3. Run a Replon program

```bash
reparo run myfile.rpl
```

---

## 💻 CLI Commands

| Command | What it does |
|---|---|
| `reparo run <file.rpl>` | Full pipeline — lex, parse, and run |
| `reparo lex <file.rpl>` | Show only the token stream (debug) |
| `reparo parse <file.rpl>` | Show only the AST (debug) |

---

## 🗣️ Replon Language — Quick Reference

```replon
# This is a comment

# Variables
a = 10
b = 20.5
name = "Reparo"
flag = true
nothing = null

# Arithmetic (correct precedence: * before +)
result = a + b * 2

# Comparison
if a != b {
    print(result)
}

# if / elif / else
if a > 100 {
    print("big")
} elif a > 5 {
    print("medium")
} else {
    print("small")
}

# While loop
counter = 0
while counter < 3 {
    counter = counter + 1
}
```

---

## 🧪 Example Output

Running `reparo run lexer/tests/test1.rpl` produces:

```
[Reparo] Running: lexer/tests/test1.rpl

────────────────────────────────────────────────────────────
  Token Stream
────────────────────────────────────────────────────────────
  Token(IDENTIFIER, 'a')
  Token(OPERATOR, '=')
  Token(NUMBER, '10')
  ...
  Token(EOF)

────────────────────────────────────────────────────────────
  Abstract Syntax Tree
────────────────────────────────────────────────────────────
  (ASSIGN a = 10)
  (ASSIGN b = 20.5)
  (ASSIGN name = "Reparo")
  (ASSIGN result = (a + (b * 2)))
  (IF (a != b) THEN [(PRINT result)])
  (WHILE (counter < 3) DO [(ASSIGN counter = (counter + 1))])
  ...
```

---

## 🔮 Roadmap

- [x] Lexer — tokenisation with line/col tracking
- [x] Parser — recursive-descent, full operator precedence
- [x] AST nodes — all expression and statement types
- [x] `reparo` CLI command (`run`, `lex`, `parse`)
- [ ] Semantic analyser — type checking, undefined variable detection
- [ ] Interpreter — execute Replon programs
- [ ] AI Bug Detector — classify errors automatically
- [ ] AI Error Fixer — suggest and apply fixes
- [ ] Function definitions and calls
- [ ] Standard library (math, string utils)
- [ ] Natural language → Replon code

---

## 🎯 Why Reparo?

Traditional compilers:
> ❌ `Error at line 3`

Reparo:
> ✅ `[ParseError] Expected ')' at line 3, col 12 — did you forget to close the expression?`

---

## 🛠️ Tech Stack

- **Language:** Python 3.10+
- **Concepts:** Compiler Design, Lexical Analysis, Recursive Descent Parsing, AST
- **Future AI Integration:** Rule-based → ML-based error correction

---

## 🤝 Contributing

This is an experimental project exploring the intersection of compiler design and AI. Contributions, ideas, and feedback are welcome.

---

## 📌 Author

**Anshul Bhardwaj**
Computer Science Engineering Student — passionate about AI, systems, and building real-world tech.

---

## ⭐ If you like this project

Give it a star and follow the journey as Reparo evolves into a full AI-powered development tool.
