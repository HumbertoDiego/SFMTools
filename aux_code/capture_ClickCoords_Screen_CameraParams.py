
import numpy as np
import open3d as o3d
import open3d.visualization.gui as gui
import open3d.visualization.rendering as rendering
import datetime
import json

# This example displays a point cloud and if you Ctrl-click on a point
# (Cmd-click on macOS) it will show the coordinates of the point.
# This example illustrates:
# - custom mouse handling on SceneWidget
# - getting a the depth value of a point (OpenGL depth)
# - converting from a window point + OpenGL depth to world coordinate
class ExampleApp:

    def __init__(self, cloud):
        # We will create a SceneWidget that fills the entire window, and then
        # a label in the lower left on top of the SceneWidget to display the
        # coordinate.
        self.clicked_point = (0, 0, 0)
        app = gui.Application.instance
        self.window = app.create_window("Open3D - GetCoord Example", 1024, 768)
        # Since we want the label on top of the scene, we cannot use a layout,
        # so we need to manually layout the window's children.
        self.window.set_on_layout(self._on_layout)
        self.widget3d = gui.SceneWidget()
        self.window.add_child(self.widget3d)
        self.info = gui.Label("")
        self.info.visible = False
        self.window.add_child(self.info)

        self.widget3d.scene = rendering.Open3DScene(self.window.renderer)

        mat = rendering.MaterialRecord()
        mat.shader = "defaultUnlit"
        # Point size is in native pixels, but "pixel" means different things to
        # different platforms (macOS, in particular), so multiply by Window scale
        # factor.
        mat.point_size = 3 * self.window.scaling
        mesh_frame = o3d.geometry.TriangleMesh.create_coordinate_frame( size=0.6, origin=[0, 0, 0])
        self.widget3d.scene.add_geometry("Coordinate Frame", mesh_frame, mat)
        self.widget3d.scene.add_geometry("Point Cloud", cloud, mat)

        bounds = self.widget3d.scene.bounding_box
        center = bounds.get_center()
        self.widget3d.setup_camera(60, bounds, center)
        self.widget3d.look_at(center, center - [0, 0, 3], [0, -1, 0])

        self.widget3d.set_on_mouse(self._on_mouse_widget3d)

        self.widget3d.set_on_key(self._on_key_widget3d)

    def _on_layout(self, layout_context):
        r = self.window.content_rect
        self.widget3d.frame = r
        pref = self.info.calc_preferred_size(layout_context,
                                             gui.Widget.Constraints())
        self.info.frame = gui.Rect(r.x,
                                   r.get_bottom() - pref.height, pref.width,
                                   pref.height)
    
    def _on_key_widget3d(self, event):
        if event.key == gui.KeyName.P and event.type == gui.KeyEvent.Type.DOWN:

            # Filenames
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            image_filename = f"screenshot_{timestamp}.png"
            camera_filename = f"camera_{timestamp}.json"

            # Get dimensions of the scene widget
            width = self.widget3d.frame.width
            height = self.widget3d.frame.height

            # Render to image using the correct function
            image = gui.Application.instance.render_to_image(self.widget3d.scene, width, height)

            ############ Before saving change color of the clicked point to red
            # Convert to NumPy array (shape: H x W x 3)
            img_np = np.asarray(image)

            # Change pixel at (x, y) to red
            view_matrix = self.widget3d.scene.camera.get_view_matrix()
            projection_matrix = self.widget3d.scene.camera.get_projection_matrix() 
            print("view_matrix:\n", view_matrix)
            # View transform (world → camera)
            view_space = view_matrix @ self.clicked_point
            # Projection (camera → clip)
            clip_space = projection_matrix @ view_space
            # Perspective divide → Normalized Device Coordinates (NDC)
            ndc = clip_space[:3] / clip_space[3]  # [x_ndc, y_ndc, z_ndc], range [-1, 1]

            # Map NDC to image coordinates (OpenGL-style: origin at bottom-left)
            col = int((ndc[0] + 1) * 0.5 * width)
            lin = int((1 - ndc[1]) * 0.5 * height)  # Invert y-axis
            print(self.clicked_point, "-->", [col,lin])
            
            img_np[lin-5:lin+5,col-5:col+5] = [255, 0, 0]  # Open3D uses row-major indexing: [y, x]

            # Convert back to Open3D image
            image = o3d.geometry.Image(img_np.astype(np.uint8))
            ############ End of color change

            # Save the modified image
            o3d.io.write_image(image_filename, image)
            print(f"Screenshot saved to {image_filename}")

            # Save camera parameters
            # Camera parameters
            cam = self.widget3d.scene.camera
            extrinsic = cam.get_model_matrix()  # 4x4 model-to-world space matrix
            extrinsic_inv = cam.get_view_matrix()  # 4x4 world-to-model space matrix
            # print("extrinsic:\n",extrinsic)
            # print("extrinsic_inv:\n",extrinsic_inv)
            # print("extrinsic_inv:\n",np.linalg.inv(extrinsic))
            # Get vertical field of view
            fov_deg = cam.get_field_of_view()  # vertical FOV in degrees
            fov_rad = np.deg2rad(fov_deg)

            # Approximate intrinsics from FOV
            print(fov_deg, cam.get_field_of_view_type())
            fy = 0.5 * height / np.tan(fov_rad / 2)
            fx = fy * (width / height)
            cx = width / 2.0
            cy = height / 2.0
            intrinsics = np.array([[fx, 0, cx], [0, fy, cy], [0, 0, 1]])
            print("intrinsics:\n",intrinsics)
            # TESTE
            p1 = intrinsics @ extrinsic_inv[:-1] @ self.clicked_point
            p1 = np.round(p1/p1[2])[:2]
            print("Computed red dot col, lin (p1=K1 @ T1 @ P): ", p1)
            print("Given red dot cam1 collin: ", [col, lin])
            # FIM TESTE

            # Convert to JSON-serializable
            camera_data = {
                "class_name" : "PinholeCameraParameters",
                "red_dot_collin": [col, lin],
                "red_dot_world": self.clicked_point.tolist(),
                "width": width,
                "height": height,
                "intrinsic": intrinsics.tolist(),
                "extrinsic": extrinsic_inv.tolist(),
            }

            with open(camera_filename, "w") as f:
                json.dump(camera_data, f, indent=4)
                print(f"Camera parameters saved to {camera_filename}")

            return gui.Widget.EventCallbackResult.CONSUMED
        return gui.Widget.EventCallbackResult.IGNORED

    def _on_mouse_widget3d(self, event):
        # We could override BUTTON_DOWN without a modifier, but that would
        # interfere with manipulating the scene.
        if event.type == gui.MouseEvent.Type.BUTTON_DOWN and event.is_modifier_down(
                gui.KeyModifier.CTRL):

            def depth_callback(depth_image):
                # Coordinates are expressed in absolute coordinates of the
                # window, but to dereference the image correctly we need them
                # relative to the origin of the widget. Note that even if the
                # scene widget is the only thing in the window, if a menubar
                # exists it also takes up space in the window (except on macOS).
                x = event.x - self.widget3d.frame.x
                y = event.y - self.widget3d.frame.y
                # Note that np.asarray() reverses the axes.
                depth = np.asarray(depth_image)[y, x]

                if depth == 1.0:  # clicked on nothing (i.e. the far plane)
                    text = ""
                else:
                    world = self.widget3d.scene.camera.unproject(
                        x, y, depth, self.widget3d.frame.width,
                        self.widget3d.frame.height)
                    text = "({:.3f}, {:.3f}, {:.3f})".format(
                        world[0], world[1], world[2])
                    print("Clicked on: ", [x,y], " --> ", world)
                    self.clicked_point = np.append(world, [1], axis =0) # Add 1 for homogeneous coordinates

                # This is not called on the main thread, so we need to
                # post to the main thread to safely access UI items.
                def update_label():
                    self.info.text = text
                    self.info.visible = (text != "")
                    # We are sizing the info label to be exactly the right size,
                    # so since the text likely changed width, we need to
                    # re-layout to set the new frame.
                    self.window.set_needs_layout()

                gui.Application.instance.post_to_main_thread(
                    self.window, update_label)

            self.widget3d.scene.scene.render_to_depth_image(depth_callback)
            return gui.Widget.EventCallbackResult.HANDLED
        return gui.Widget.EventCallbackResult.IGNORED


def main():
    app = gui.Application.instance
    app.initialize()

    # This example will also work with a triangle mesh, or any 3D object.
    # If you use a triangle mesh you will probably want to set the material
    # shader to "defaultLit" instead of "defaultUnlit".

    dataset = o3d.data.EaglePointCloud()
    pcd = o3d.io.read_point_cloud(dataset.path)
    ex = ExampleApp(pcd)

    app.run()


if __name__ == "__main__":
    main()
