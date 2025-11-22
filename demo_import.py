"""
DevKit-Zero Import Demo
This script demonstrates how to import and use DevKit-Zero tools in your own code.
"""

# 1. Import specific tools
from devkit_zero import formatter, random_gen, diff_tool

print("--- Formatter Demo ---")
bad_code = "def hello( ):print( 'world' )"
formatted, error = formatter.format_code(bad_code, language="python")
print(f"Original: {bad_code}")
print(f"Formatted:\n{formatted}")

# 3. Use the Random Generator
print("\n--- Random Generator Demo ---")
uuid_val = random_gen.generate_uuid()
password = random_gen.generate_secure_password(length=12)
print(f"UUID: {uuid_val}")
print(f"Secure Password: {password}")

# 4. Use the Diff Tool
print("\n--- Diff Tool Demo ---")
text1 = "Hello World"
text2 = "Hello Python"
diff_result = diff_tool.compare_text(text1, text2)
print("Diff Result:")
print("".join(diff_result))
