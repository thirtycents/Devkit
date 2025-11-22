# DevKit-Zero Demo Script

## 1. Introduction (0:00 - 0:30)

"Hello everyone. Today I'm presenting **DevKit-Zero**, a zero-dependency developer toolkit designed for Python and JavaScript developers. It provides a suite of 12 essential tools that work out-of-the-box without installing heavy third-party libraries."

**Key Features:**

- **Zero Dependencies**: Only requires Python standard library (and `tkinter` for GUI).
- **3 Modes**: GUI, CLI, and Importable Library.
- **Cross-Platform**: Works on Windows, macOS, and Linux.

---

## 2. GUI Demonstration (0:30 - 2:00)

*Action: Double-click `start_gui.bat` or run `python -m devkit_zero.gui_main`*

"Let's start with the Graphical User Interface. As you can see, it's a clean, native interface."

**Scenario A: Code Formatting**

1. Select **Code Formatter** from the tool list.
2. Paste some messy Python code:
   ```python
   def  test( ):print( "hello" )
   ```
3. Click **Format Code**.
4. Show the clean result:
   ```python
   def test():
       print("hello")
   ```

**Scenario B: Random Data**

1. Select **Random Generator**.
2. Choose **Type: UUID** -> Click **Generate**.
3. Choose **Type: Password**, set Length to 20 -> Click **Generate**.
4. "This is great for quickly generating test data."

**Scenario C: Regex Tester**

1. Select **Regex Tester**.
2. Select **Common Pattern: Email**.
3. Type a text: `Contact us at support@example.com or sales@test.co.uk`.
4. Click **Test Regex**.
5. Show the highlighted matches and extracted groups.

---

## 3. CLI Demonstration (2:00 - 3:00)

*Action: Open Terminal*

"For automation and terminal lovers, DevKit-Zero offers a powerful CLI."

**Command 1: Help**

```bash
python -m devkit_zero.cli --help
```

"You can see all available tools listed here."

**Command 2: Quick Format**

```bash
python -m devkit_zero.cli format --input "a=1;b=2" --language python
```

"It formats code directly in the terminal."

**Command 3: Generate UUID**

```bash
python -m devkit_zero.cli random uuid
```

---

## 4. Import / Library Usage (3:00 - 4:00)

*Action: Open `demo_import.py` in VS Code*

"Finally, the most powerful feature: You can use DevKit-Zero as a library in your own projects."

**How to Import:**
"Simply import the package `devkit_zero`."

```python
from devkit_zero import formatter, random_gen

# Use the formatter programmatically
code = "x=1"
clean_code, error = formatter.format_code(code, "python")

# Generate data
user_id = random_gen.generate_uuid()
```

*Action: Run `python demo_import.py`*
"Here we see the script running, utilizing the toolkit's internal logic for our own needs."

---

## 5. Conclusion

"DevKit-Zero is your lightweight, all-in-one companion for daily development tasks. Thank you."
