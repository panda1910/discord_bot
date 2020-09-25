import os

def solve(pen):
    ex = """except Exception as e:
    traceback.print_exc(file=log)\n"""
    with open("t2.py", "w+") as file:
        text = "\n  ".join(pen)
        file.write("""import traceback\nlog = open("log.txt", "w")\n""")
        file.write("try:\n  ")
        file.writelines(text)
        file.write('\n')
        file.write(ex)
        file.write("log.close()")

pen = """print("Hello")
print("hh")""".split('\n')
solve(pen)