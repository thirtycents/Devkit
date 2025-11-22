def used_function():
    return "called"

def unused_function():
    return "not called"

class TestClass:
    def used_method(self):
        return "called"
    
    def unused_method(self):
        return "not called"

# 调用部分函数
used_function()
TestClass().used_method()