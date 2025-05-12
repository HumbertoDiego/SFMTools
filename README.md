# SFMTools
Papiros de Structure from Motion e processamento fotogramétrico

### 1. Notebook sobre a teoria da triangulação, fototriangulação e aerotriangulação [fototriangulação.ipynb](https://github.com/HumbertoDiego/SFMTools/blob/main/fototriangulação.ipynb).
### 2. Notebook sobre a teoria da fototriangulação para múltiplas visadas [fototriangulação_MVS.ipynb](https://github.com/HumbertoDiego/SFMTools/blob/main/fototriangulação_MVS.ipynb).
### 3. Notebook sobre a teoria da fototriangulação pelo método dos feixes perspectivos (bundle-adjustment) [fototriangulação_BundleAdjustment.ipynb](https://github.com/HumbertoDiego/SFMTools/blob/main/fototriangulação_BundleAdjustment.ipynb).


Requistos:

- Anaconda
    - conda create -n myenv python=3.12 ipykernel jupyter
    - conda activate myenv
    - pip install pillow defusedxml xmptools numpy matplotlib pyproj geopandas contextily sympy requests gdown

   
<!-- 
git init
git remote add origin https://github.com/HumbertoDiego/SFMTools
git pull origin main
# Do and push changes:
git add * ; git commit -m "general updates"; git push -u origin main
#Pull changes
git pull origin main
 -->