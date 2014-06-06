import unittest
from app import hooks

def hook1():
    return True

def hook2(arg1, arg2, arg3):
    if arg1 == "arg1" and arg2 == "arg2" and arg3 == "arg3":
        return True

@hooks.add_hook("hook_test3")
def hook3():
    return True

def hook4():
    pass

def hook5():
    return True

class TestHooks(unittest.TestCase):
    def setUp(self):
        hooks.add("hook_test1", hook1)
        hooks.add("hook_test2", hook2)
        hooks.add("hook_test4", hook4)
        hooks.add("hook_test4", hook5)

    @classmethod
    def tearDownClass(self):
        for hook_type in ["hook_test" + str(x) for x in range(1, 5)]:
            del hooks.hooks[hook_type]

    def test_hook1(self):
        self.assertTrue(hooks.run("hook_test1"))

    def test_hook2(self):
        self.assertTrue(hooks.run("hook_test2", "arg1", arg2="arg2", arg3="arg3"))

    def test_hook3(self):
        self.assertTrue(hooks.run("hook_test3"))

    def test_hook4(self):
        self.assertTrue(hooks.run("hook_test4"))

    def test_hook5(self):
        self.assertIsNone(hooks.run("hook_test_missing"))
