from pynput.mouse import Controller

mouse = Controller()

# Spostiamo il mouse di 10 unità verso destra
mouse.move(50, 0)
print("Mouse moved successfully!")