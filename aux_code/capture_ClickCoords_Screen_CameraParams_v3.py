
import numpy as np
import open3d as o3d

import open3d as o3d
import numpy as np

def pick_points(pcd, mesh_frame):
    print("1) Please pick at least three correspondences using [shift + left click]")
    print(" Press [shift + right click] to undo point picking")
    print("2) After picking points, press 'Q' to close the window")

    vis = o3d.visualization.VisualizerWithEditing()
    vis.create_window("Open3D - GetCoord Example", 1024, 768)
    vis.add_geometry(pcd)
    vis.add_geometry(mesh_frame)
    # Rode uma iteração de visualização (necessário para inicializar a câmera)
    vis.poll_events()
    vis.update_renderer()

    ctr = vis.get_view_control()
    ctr.set_lookat(np.array([ 1.3800420165061951, 2.763045072555542, 1.3682200312614441 ]))
    ctr.set_front(np.array( [ -0.8102398120616997, -0.042542061007454335, -0.58455249550015587 ]))
    ctr.set_up(np.array( [ -0.12981544781968604, -0.95956399978807505, 0.24976965351716651 ]))

    params = ctr.convert_to_pinhole_camera_parameters()
    K = params.intrinsic.intrinsic_matrix
    w = params.intrinsic.width
    h = params.intrinsic.height
    T = params.extrinsic

    # print("Intrinsic:", w,  h, "\n", K)
    # print("Extrinsic:\n" , T)

    vis.run() # user picks points
    vis.destroy_window()

    coordinates = np.asarray(pcd.points)[vis.get_picked_points()]
    # Create a column of ones
    ones_column = np.ones((coordinates.shape[0], 1))
    coordinates = np.hstack((coordinates, ones_column))
    print("3D coordinates:\n", coordinates)

    pixel = K @ T[:-1] @ coordinates.T
    pixel = np.round(pixel/pixel[2])[:2]
    print("Pixel coordinates:\n", pixel.T)

    return coordinates, pixel

if __name__ == "__main__":
    dataset = o3d.data.EaglePointCloud()
    pcd = o3d.io.read_point_cloud(dataset.path)
    mesh_frame = o3d.geometry.TriangleMesh.create_coordinate_frame( size=30, origin=[0, 0, 0])

    coords, pixels = pick_points(pcd, mesh_frame)
    # print("Picked points:\n", coords)
