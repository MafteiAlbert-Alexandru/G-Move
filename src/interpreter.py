class Interpreter:
    @staticmethod
    def repeat_until_result(func, check):
        while(True):
            result = func()
            if check(result):
                return result[0]
            else:
                print(result[1].format(result))
            