import PySimpleGUI as sg
import shutil
import os
import subprocess
import screeninfo

desktop_file = """[Desktop Entry]
Name=Glava GUI
Type=Application
Exec=EXECCOMMAND
Terminal=false
"""

monitors = []
for m in screeninfo.get_monitors():
    monitors += [str(len(monitors) + 1)]
print(monitors)


def is_system_dark_mode():  # check if gtk darkmode is enabled
    with open(os.environ['HOME'] + '/.config/gtk-3.0/settings.ini') as f:
        if 'gtk-application-prefer-dark-theme=1' in f.read():
            return True
    return False


def run_glava(module='bars', desktop=False):
    glava_cmd = ['glava']
    glava_cmd += ['-m ' + module]
    if desktop:
        glava_cmd += ['--desktop']
    print(glava_cmd)
    subprocess.Popen(glava_cmd)


"""def read_glava_config():
    configuration = [0, 0, 1920, 1080]  # x,y,w,h

    glava_config_file = os.environ['HOME'] + '/.config/glava/rc.glsl'
    if not os.path.isfile(glava_config_file):   # create user config if does not exist
        subprocess.run(['glava', '--copy-config'])
    with open(glava_config_file) as f:
        for line in f.readlines():
            if 'setgeometry' in line:
                cfg = line.split(' ')
                try:
                    configuration[0] = int(cfg[2])  # x
                    configuration[1] = int(cfg[3])  # y
                    configuration[2] = int(cfg[4])  # width
                    configuration[3] = int(cfg[5])  # height
                except:
                    print('error while reading configuration #1001')

    return configuration"""


def apply_configuration(module, desktop, monitor, taskbar, startup):
    screen = screeninfo.get_monitors()[monitor - 1]

    glava_config_file = os.environ['HOME'] + '/.config/glava/rc.glsl'
    if not os.path.isfile(glava_config_file):   # create user config if does not exist
        subprocess.run(['glava', '--copy-config'])
    with open(glava_config_file + '.new', 'w') as nf:
        with open(glava_config_file) as f:
            for line in f.readlines():
                if 'setgeometry' in line:
                    line = '#request setgeometry ' + str(screen.x) + ' ' + str(screen.y) + ' ' + str(screen.width) + ' ' + str(screen.height - taskbar)
                nf.write(line)
    shutil.move(glava_config_file + '.new', glava_config_file)

    if startup:
        glava_cmd = 'glava -m ' + module
        if desktop:
            glava_cmd += ' --desktop'
        open(os.environ['HOME'] + '/.config/autostart/glava-gui.desktop', 'w').write(desktop_file.replace('EXECCOMMAND', glava_cmd))
    else:
        if os.path.isfile(os.environ['HOME'] + '/.config/autostart/glava-gui.desktop'):
            os.remove(os.environ['HOME'] + '/.config/autostart/glava-gui.desktop')



if is_system_dark_mode():
    sg.theme('Topanga')
else:
    sg.theme('Default1')

# configuration = read_glava_config()

layout = [ [sg.Text('GUI for Glava audio spectrum visualizer')],
           [sg.Text('Effect/Module', size=(25, 1)), sg.InputCombo(['bars', 'radial', 'graph', 'wave', 'circle'], 'bars')],
           [sg.Text('Show as desktop wallpaper', size=(25, 1)), sg.Checkbox('', True)],
           [sg.Text('Show on monitor', size=(25, 1)), sg.InputCombo(monitors, monitors[0])],
           [sg.Text('Taskbar height', size=(25, 1)), sg.InputText(0, size=(10, 1))],
           [sg.Text('Launch on start', size=(25, 1)), sg.Checkbox('')],
           [sg.Button('Save & Launch'), sg.Button('Exit')] ]

window = sg.Window('glava-gui', layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == 'Save & Launch':
        apply_configuration(values[0], values[1], int(values[2]), int(values[3]), values[4])
        run_glava(values[0], values[1])
        break

window.close()
