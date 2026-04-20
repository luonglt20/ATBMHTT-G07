def djb2(s):
    h = 5381
    for c in s:
        h = ((h << 5) + h + ord(c)) & 0xFFFFFFFF
    return h

for name in ['KERNEL32.DLL', 'USER32.DLL', 'WinExec', 'MessageBoxA',
             'kernel32.dll', 'user32.dll', 'Kernel32.dll', 'User32.dll']:
    print(f'{name:20s} = 0x{djb2(name):08x}')
