from tc.inner.checkers import MessageWrapper

class CheckFailed(TypeError):
    def __init__(self, template, value):
        if isinstance(template, MessageWrapper):
            self.fail_message = template.on_fail(value)
        else:
            self.fail_message = template
        self.value = value

    def __str__(self):
        return f"{self.fail_message}: {repr(self.value)}"

    def __repr__(self):
        return "CheckFailed(" + repr(self.fail_message) + ", " + repr(self.value) + ")"