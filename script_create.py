import glob
import os
import sys
import requests
from PIL import Image
from configparser import ConfigParser

os.chdir(os.path.dirname(sys.argv[0]))  # Place de répertoire de travail dans le même dossier que le script

#  try:  # Permet de renvoyer l'erreur peut importe où elle se trouve dans le programme, sans le quitter pour autant.
gist_url = 'https://gist.githubusercontent.com/AiroPi/54e11509fac8db37eb2be1ae18b2ef38/raw/pattern.ini'  # On recupère le fichier exemple directement en ligne, qui permet de mettre a jour l'apparence sans toucher au fichier.'
pattern_file = requests.get(gist_url)

config = ConfigParser()  # On ouvre le fichier .ini qui liste tout les raccourcis que l'on souhaite faire.
config.optionxform = str
config.read('@Resources/Config.ini')

for path in glob.glob('@Resources/*/*'):  # on parcours tout les dossiers dans les ressources pour acceder a toutes les images.
    if os.path.isdir(path):
        continue  # Si c'est un dossier, ce n'est donc pas une image :)

    filename, file_ext = os.path.splitext(path)  # On récupère son nom et son type (png, ico...)
    if file_ext.upper() != '.ICO':  # Si ce n'est pas une icone, on le converti en icone, pour qu'elle soit plus légère et ne fasse pas buguer le skin.
        print('Conversion de '+filename+file_ext+' en .ico')

        img = Image.open(path)
        icon_sizes = [(64,64)]

        if not os.path.isdir(os.path.split(path)[0]+'\\non_ico'):  # Si il n'y a pas déjà de dossier non_icon/ dans le dossier ressource, on le créer.
            os.mkdir(os.path.split(path)[0]+'\\non_ico')

        img = img.convert('RGBA')  # On le converti pour avoir de la transparence.
        img.save(filename+'.ico', sizes=icon_sizes)  # On l'enregistre en .ico, avec un petit taille.
        os.replace(path, '{p[0]}\\non_ico\\{p[1]}'.format(p=os.path.split(path)))  # on déplace l'ancienne image dans le fichier non_icon/

print('')

def create_section_config():
    """Function to create a new Config object based on the Exemple.ini file."""
    _section_config = ConfigParser()  # We create the current section Config based on the exemple
    _section_config.optionxform = str
    if os.path.isfile('pattern.ini'):  # Soit à partir de l'Exemple local, soit a partir de l'exemple en ligne.
        _section_config.read('pattern.ini')
        return _section_config

    _section_config.read_string(pattern_file.text)

    return _section_config


print("Nous allons créer votre widget pour ces catégories :", ", ".join(config.sections()))
for section in [config[section_name] for section_name in config.sections()]:  # We go through the different sections (exemple: uPlay, Steam…)
    if section.name == "Default":
        continue
    print(f"En cours pour {section.name}...")

    section_config = create_section_config()
    direction = section.pop('direction', 'right')  # Will decide if the widget will be oriented to the right or left (default to right)

    print(direction)
    print(direction == 'right')
    if direction == 'right':
        list_index_positions = list(range(len(section.items())))
    else:
        list_index_positions = list(reversed(range(len(section.items()))))

    sections_to_append = []

    app_number = 1
    app_icons = {os.path.splitext(os.path.basename(path))[0].lower(): path.replace('@Resources', '#@#')
                for path in glob.glob(rf"@Resources\{section.name}\*")}
    print(app_icons)

    section_config['MeterAppsShape']['Shape'] = section_config['MeterAppsShape']['Shape'].format(len(section))
    section_config['MeterActiveOverShape']['Shape'] = section_config['MeterActiveOverShape']['Shape'].format(list_index_positions[0])
    
    
    for app_name, app_path in section.items():  # We go through all images regarding the current section (in the SECTION_NAME file in @ressource)
        MeterAppShapeIcon = dict(section_config['MeterAppShapeIcon'])
        MeterAppIcon = dict(section_config['MeterAppIcon'])
        MeterAppText = dict(section_config['MeterAppText'])

        MeterAppIcon['LeftMouseUpAction'] = app_path

        if app_name == 'category':
            MeterAppIcon['ImageName'] = app_icons.get(section.name.lower(), 'introuvable')
            MeterAppText['Text'] = section.name

            MeterAppShapeIcon['Shape'] = MeterAppShapeIcon['Shape'].format(list_index_positions[0])
            MeterAppIcon['X'] = MeterAppIcon['X'].format(list_index_positions[0])
            MeterAppIcon['Container'] = MeterAppIcon['Container'].format(0)
            MeterAppText['FontColor'] = MeterAppText['FontColor'].format(255)

            MeterAppIcon.pop('Group')
            MeterAppIcon.pop('Hidden')
            MeterAppIcon.pop('ImageAlpha')
            MeterAppText.pop('Group')

            sections_to_append.insert(0, (MeterAppShapeIcon, MeterAppIcon, MeterAppText))
            print(f"....raccourcis pour l'application-catégorie {section.name} configuré")
            continue

        MeterAppText['Text'] = app_name
        MeterAppIcon['ImageName'] = app_icons.get(app_name.lower(), 'introuvable')
        
        MeterAppShapeIcon['Shape'] = MeterAppShapeIcon['Shape'].format(list_index_positions[app_number])
        MeterAppIcon['X'] = MeterAppIcon['X'].format(list_index_positions[app_number])
        MeterAppIcon['Container'] = MeterAppIcon['Container'].format(app_number)
        MeterAppText['FontColor'] = MeterAppText['FontColor'].format('#Alpha#')

        sections_to_append.append((MeterAppShapeIcon, MeterAppIcon, MeterAppText))
        print(f"....raccourcis pour l'application {app_name} configuré")
        app_number += 1

    del section_config['MeterAppShapeIcon']
    del section_config['MeterAppIcon']
    del section_config['MeterAppText']

    for app_index, app_meters in enumerate(sections_to_append):
        section_config[f'MeterAppShapeIcon{app_index}'] = app_meters[0]
        section_config[f'MeterAppIcon{app_index}'] = app_meters[1]
        section_config[f'MeterAppText{app_index}'] = app_meters[2]


    if section.name not in [name for name in os.listdir(".") if os.path.isdir(name)]:
        os.mkdir(section.name)
    with open(section.name + '/' + section.name + '.ini', 'w') as configfile:
        section_config.write(configfile)

    print(f"Section {section.name} créée avec succès !\n")

input('Appuyez sur un touche pour fermer...')
