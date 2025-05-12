import open3d as o3d
import numpy as np
import copy

colors = {
    'white':  [1.0, 1.0, 1.0],
    'yellow': [1.0, 1.0, 0.0],
    'red':    [1.0, 0.0, 0.0],
    'orange': [1.0, 0.5, 0.0],
    'blue':   [0.0, 0.0, 1.0],
    'green':  [0.0, 1.0, 0.0],
    'black':  [0.0, 0.0, 0.0]
}

points = [
    [0, 0, 0], # P0 z = 0, face azul vermelha
    [1, 0, 0], # P1
    [2, 0, 0], # P2
    [2, 1, 0], # P3
    [1, 1, 0], # P4
    [0, 1, 0], # P5
    [0, 2, 0], # P6
    [1, 2, 0], # P7
    [2, 2, 0], # P8
    [0, 0, 1], # P9
    [1, 0, 1], # P10
    [2, 0, 1], # P11
    [2, 1, 1], # P12
    [1, 1, 1], # P13 interno
    [0, 1, 1], # P14
    [0, 2, 1], # P15
    [1, 2, 1], # P16
    [2, 2, 1], # P17
    [0, 0, 2], # P18 z = 2, face amarelo e verde
    [1, 0, 2], # P19
    [2, 0, 2], # P20
    [2, 1, 2], # P21
    [1, 1, 2], # P22
    [0, 1, 2], # P23
    [0, 2, 2], # P24
    [1, 2, 2], # P25
    [2, 2, 2], # P26
]

pcd = o3d.geometry.PointCloud()
point_cloud = np.asarray(np.array(points))
pcd.points = o3d.utility.Vector3dVector(point_cloud)
pcd.colors = o3d.utility.Vector3dVector([[0,0,0] for i in range(len(pcd.points))])

##### Gerar o volume do cubo para ofuscar os pontos atrás do cubo
def create_box(tx,ty,tz, color=colors["white"]):
    mesh_box = o3d.geometry.TriangleMesh.create_box(width=1,
                                                    height=1,
                                                    depth=1)
    mesh_box.compute_vertex_normals()
    mesh_box.compute_triangle_normals()

    # Get triangle data
    triangles = np.asarray(mesh_box.triangles)
    vertices = np.asarray(mesh_box.vertices)
    normals = np.asarray(mesh_box.triangle_normals)

    # Expand: one triangle = three new unique vertices
    new_vertices = []
    new_triangles = []
    new_colors = []

    for i, tri in enumerate(triangles):
        for j in range(3):
            new_vertices.append(vertices[tri[j]])
            new_colors.append(color)  # normalize [-1,1] to [0,1]
        new_triangles.append([3*i, 3*i + 1, 3*i + 2])

    #### Create new mesh with duplicated vertices
    colored_mesh = o3d.geometry.TriangleMesh()
    colored_mesh.vertices = o3d.utility.Vector3dVector(new_vertices)
    colored_mesh.triangles = o3d.utility.Vector3iVector(new_triangles)
    colored_mesh.vertex_colors = o3d.utility.Vector3dVector(new_colors)

    colored_mesh_translated = copy.deepcopy(colored_mesh).translate((tx, ty, tz))
    return colored_mesh_translated

cube1 = create_box(0,0,0, colors["red"])
cube2 = create_box(0,1,0)
cube3 = create_box(0,1,1, colors["yellow"])
cube4 = create_box(1,1,1)
cube5 = create_box(1,0,0)
cube6 = create_box(1,1,0, colors["blue"])
cube7 = create_box(0,0,1)
cube8 = create_box(1,0,1, colors["green"])

#### Eixos X(red arrow), Y(green arrow), Z(blue arrow)
mesh_frame = o3d.geometry.TriangleMesh.create_coordinate_frame( size=0.4, origin=[0, 0, 0])

o3d.visualization.draw_geometries([pcd, cube1, cube2, cube3, cube4, cube5, 
                                   cube6, cube7, cube8, mesh_frame] ,
                                   width=1024, height=768, zoom=1, mesh_show_wireframe =True )