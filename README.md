# SFMTools
Papiros de Structure from Motion e processamento fotogramétrico

### 1. Hands-On em triangulação, fototriangulação e aerotriangulação [fototriangulação.ipynb](https://github.com/HumbertoDiego/SFMTools/blob/main/fototriangulação.ipynb).
### &nbsp; &nbsp; 1.a Hands-On em calibração de câmeras em um objeto com um padrão 3D [calibração_3DPattern.ipynb](https://github.com/HumbertoDiego/SFMTools/blob/main/calibração_3DPattern.ipynb).
### 2. Hands-On em fototriangulação para múltiplas visadas [fototriangulação_MVS.ipynb](https://github.com/HumbertoDiego/SFMTools/blob/main/fototriangulação_MVS.ipynb).
### 3. Hands-On em fototriangulação pelo método dos feixes perspectivos (bundle-adjustment) [fototriangulação_BA.ipynb](https://github.com/HumbertoDiego/SFMTools/blob/main/fototriangulação_BA.ipynb).
### &nbsp; &nbsp; 3.a Hands-On em técnicas de correpondência automática de pontos em imagens sobrepostas [getCorrespondences.ipynb](https://github.com/HumbertoDiego/SFMTools/blob/main/getCorrespondences.ipynb).
### &nbsp; &nbsp; 3.b Hands-On em estimativa inicial da transformação espaço-objeto para espaço-imagem [fundamentalMatrix.ipynb](https://github.com/HumbertoDiego/SFMTools/blob/main/fundamentalMatrix.ipynb).
<br>
Requistos:

- Anaconda
    - conda create -n myenv python=3.12 ipykernel jupyter
    - conda activate myenv
    - pip install pillow defusedxml xmptools numpy matplotlib pyproj geopandas contextily sympy requests gdown open3d scipy ipython-autotime opencv-python

   
<!-- 
git init
git remote add origin https://github.com/HumbertoDiego/SFMTools
git pull origin main
# Do and push changes:
git add * ; git commit -m "general updates"; git push -u origin main
#Pull changes
git pull origin main 
 -->
