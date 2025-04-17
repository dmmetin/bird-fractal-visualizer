Dance Video to Robot Skeleton

Ce projet transforme une vidéo de danse en une vidéo où un squelette coloré reproduit les mouvements du danseur. Il utilise MediaPipe pour la détection de pose et OpenCV pour dessiner le squelette.



Avis Important : Ce projet est destiné à un usage non commercial uniquement, notamment pour les amis, les danseurs et les hobbyistes souhaitant créer des vidéos de danse avec un squelette robotisé. Toute utilisation commerciale nécessite une autorisation explicite de l'auteur. Consultez la section Utilisation Commerciale et Disclaimer sur les Brevets pour plus de détails.


Les textes complets des licences des bibliothèques utilisées se trouvent dans le dossier `LICENSES`.


Prérequis





Python 3.8+ (de préférence via Miniconda)



FFmpeg (installé séparément et ajouté au PATH)



Installation





Créer un environnement virtuel avec Miniconda :

conda create -n dance_robot python=3.8
conda activate dance_robot



Installer les dépendances :

pip install -r requirements.txt



Installer FFmpeg :





Téléchargez FFmpeg depuis ffmpeg.org.



Ajoutez FFmpeg à votre PATH système. Consultez le guide d'installation FFmpeg pour Windows, ou utilisez un gestionnaire de paquets comme apt ou brew pour Linux/macOS.



Note : FFmpeg n'est pas distribué avec ce projet et doit être installé séparément en raison de ses conditions de licence.



Utilisation





Placez votre vidéo de danse (input_video.mp4) dans le répertoire courant.



Exécutez le programme :

python dance_robot.py



La vidéo annotée sera sauvegardée dans dance_analysis_output/annotated_video_v02.mp4.



requirements.txt

opencv-python
mediapipe
numpy



Origines et Licences des Bibliothèques





OpenCV : opencv.org, Licence Apache 2.0



MediaPipe : mediapipe.dev, Licence Apache 2.0



NumPy : numpy.org, Licence BSD



FFmpeg : ffmpeg.org, Licence LGPL ou GPL (selon la configuration)



Note : Ce projet utilise FFmpeg via subprocess pour l'extraction et la recombinaison audio. FFmpeg n'est pas inclus dans ce dépôt et doit être installé séparément. Voir la section Installation pour plus de détails.



Fonctionnement





Détection de Pose : MediaPipe extrait les points clés du corps de chaque image de la vidéo d'entrée.



Interpolation : Les poses manquantes sont remplies avec la dernière pose valide.



Dessin du Squelette : OpenCV dessine un squelette coloré sur les images en fonction des poses détectées.



Ajout Audio : FFmpeg recombine l'audio original avec la vidéo annotée.

Ce projet est une démonstration simple pour partager des outils accessibles sur GitHub à des fins non commerciales.



Utilisation Commerciale et Disclaimer sur les Brevets





Usage Non Commercial : Ce projet est destiné à un usage non commercial uniquement, comme des projets personnels, des usages éducatifs ou par des amis et danseurs. Toute utilisation commerciale, y compris la vente, la licence ou l'intégration de ce code dans un produit ou service commercial, nécessite une autorisation écrite explicite de l'auteur.



Responsabilité sur les Brevets : Bien que les techniques utilisées dans ce projet (par ex., estimation de pose, annotation vidéo) soient standards et basées sur des bibliothèques open-source, les utilisateurs sont responsables de s'assurer que leur utilisation de ce code ne viole aucun brevet, en particulier dans des applications commerciales. L'auteur ne fait aucune déclaration ni garantie concernant les droits de brevet et décline toute responsabilité en cas de violation de brevet. Pour une utilisation commerciale, il est recommandé de consulter un avocat spécialisé en brevets pour évaluer les risques potentiels.



Licence de FFmpeg : FFmpeg est utilisé via subprocess et doit être installé séparément. FFmpeg est sous licence LGPL ou GPL, selon sa configuration. Les utilisateurs sont responsables de s'assurer que leur utilisation de FFmpeg respecte ses termes de licence, notamment pour des applications commerciales.



Licence

Ce projet est sous licence Apache License, Version 2.0. Voir le fichier LICENSE pour plus de détails.

Copyright 2025 David Marc MéTIN

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.