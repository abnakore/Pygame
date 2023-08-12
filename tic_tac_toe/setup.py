import cx_Freeze

executables = [cx_Freeze.Executable("tic_tac_toe.py", icon="icon.ico", base = "Win32GUI")]

cx_Freeze.setup(
    name="Tic Tac Toe",
    options={"build_exe": {"packages": ["pygame"], "include_files": [
                                                                     "icon.ico", "icon.png", "README.txt", "DripDrop.wav",
                                                                     "e1.png", "HighWhoosh.wav", "LowWhoosh.wav", 
                                                                     "multiplayer.png", "o.png", "oc.png", "op.png",
                                                                     "single_player.png", "SuctionCup.wav",  "DunDunDun.wav",
                                                                     "Tada.wav", "x.png", "xc.png", "xp.png", "sample.PNG"
                                                                    ]}},
    executables = executables
)