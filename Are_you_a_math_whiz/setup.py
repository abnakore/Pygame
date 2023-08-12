import cx_Freeze

executables = [cx_Freeze.Executable("main.py", icon="datas/icon.ico", base = "Win32GUI")]

cx_Freeze.setup(
    name="Are You A Math Whiz?",
    options={"build_exe": {"packages": ["pygame", "pygame_textinput", "random", "sys"], "include_files": [
                                                                     "datas", "resources"
                                                                    ]}},
    executables = executables
)
# “ ” " "