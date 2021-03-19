# Slide-Folder-Rainmeter-Skin

Ce skin rainmeter permet de créer des dossiers qui se présente comme 1 seule icone, qui s'étend quand on passe la souris par dessus.

## Create new group

Pour créer un groupe, il vous suffit d'aller dans @Ressources/ et de créer un dossier qui aura le nom principal. Ensuite, mettez dedans les icones, au format que vous voulez, avec le nom que vous voudrez voir sur le bureau (exemple : "Minecraft.ico")

Ouvrez ensuite Config.ini, et ajoutez dedans le groupe sous cette forme :

```ini
[{Category name}]
category=["{chemin vers le .exe de l'application}"]
direction=right ; peut aussi être left

{nom de la 1er app (le même que son icon)}=["{chemin vers le .exe de l'app}"]
{nom de la 2e app (le même que son icon)}=["{chemin vers le .exe de l'app}"]
; etc...
```

> Exemple :

```ini
[Battle.net]
direction=right
category=["C:\Program Files (x86)\Battle.net\Battle.net Launcher.exe"]

Hearthstone=["C:\Program Files (x86)\Hearthstone\Hearthstone Beta Launcher.exe"]
```

Il ne vous reste plus qu'à lancer le fichier `script_create.exe` et vos skins seront créers automatiquement !