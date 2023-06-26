from enum import Enum

Task = Enum('Task', ['PART1', 'PART2'])
COLOR_DISTRIBUTION = ([1.0] * 41, range(380, 790, 10))
RADIUS = 1300
Kd = 0.98
Kd_ = 0.3  # Kd'
LIGHT_FLUX = 130
CONE_ANGLE = 15
LIGHT_POS = (0, 0, -100)
LIGHT_DIR = (0, 0, -1)
PART = Task.PART1
H = 390


def format_name(is_x: bool = False, is_y: bool = False, is_z: bool = False) -> str:
    # change direction, it's depend on variant
    return '{x}_{y}_{z}'.format(x='-R' if is_x else 0, y='-R' if is_y else 0, z='R' if is_z else 0)


def create_observer_prototype(is_x: bool = False, is_y: bool = False, is_z: bool = False) -> tuple:
    po = PlaneObserver()
    po.res = (3, 3)
    po.thresh_ang = 90  
    po.phenom = ObserverData.ILLUM
    node = ObserverNode(po)
    node.name = format_name(is_x, is_y, is_z)
    return po, node


def create_camera(angle: tuple, is_x: bool = False, is_y: bool = False, is_z: bool = False):
    cam = Camera(6, RADIUS)
    cam_transform = XYZTransform()
    cam_transform.pos = (0, 0, 0)
    cam_transform.x_rot_ang = angle[0]
    cam_transform.y_rot_ang = angle[1]
    cam_transform.z_rot_ang = angle[2]
    cam.tr = cam_transform
    cam.name = format_name(is_x, is_y, is_z)
    return cam


if PART == Task.PART1:
    def create_mesh() -> tuple:
        sphere = GetClass(Shape, 'Sphere')(name = 'mySphere', radius = RADIUS)
        real_sphere = sphere.parts[0]
        real_sphere.surf_attrs.front_side.kd = Kd
        real_sphere.surf_attrs.front_side.kd_color = SpecSurfColor(*COLOR_DISTRIBUTION)
        real_sphere.front_medium = scene.GetMedium('env')
        real_sphere.back_medium = scene.GetMedium('env')
        sphere_node = MeshNode(sphere)
        sphere_tr = XYZTransform()
        sphere_tr.pos = (0, 0, 0)
        sphere_node.tr = sphere_tr
        return [sphere_node]
else:
    def create_mesh():
        def __create_ellipsoid(Kd: float, hz_is_positive: bool = True) -> tuple:
            te = GetClass(Shape, 'TruncatedEllipsoid')()
            te.axes = tuple([RADIUS * 2] * 3)
            te.hz = (RADIUS - H) * (1 if hz_is_positive else -1)
            te.rev = hz_is_positive
            te.parts[0].surf_attrs.front_side.kd = Kd
            te.parts[0].surf_attrs.front_side.kd_color = SpecSurfColor(*COLOR_DISTRIBUTION)
            te.parts[0].front_medium = scene.GetMedium('env')
            te.parts[0].back_medium = scene.GetMedium('env')
            te_node = MeshNode(te)
            te_transform = XYZTransform()
            te_transform.pos = (0, 0, 0)
            te_node.tr = te_transform
            return te_node
        return [__create_ellipsoid(Kd), __create_ellipsoid(Kd_, False)]


scene = Scene(name='p{p}'.format(p=PART.value))
mesh_nodes = create_mesh()
ls = GetLibrary(Light).GetItem('Cone')
ls.radiometric = True
ls.total_flux = LIGHT_FLUX
ls.cone_angle = CONE_ANGLE
ls.color = SpecLightColor(*COLOR_DISTRIBUTION)
light_node = LightNode(ls, name = 'coneLight')
light_node.medium = scene.GetMedium('env')
light_tr = Transform()
light_tr.pos = LIGHT_POS
light_tr.azim = 0
light_tr.rot = 0
light_tr.tilt = 0
light_node.tr = light_tr
light_node.targ_dist = RADIUS + LIGHT_POS[2]  # change index, it's depends on variant

OBSERVER_OFFSET = 4  # the shift is necessary so that the edges of the observers do not go beyond the sphere
po, onode = create_observer_prototype(is_x=True)  # -R_0_0                                   
po.org = (-RADIUS + OBSERVER_OFFSET, -25, 25)
po.dir = (-300, 0, 0)
po.x_side = (0, 50, 0)
po.y_side = (0, 0, -50)
po1, onode1 = create_observer_prototype(is_y=True)  # 0_-R_0                         
po1.org = (-25, -RADIUS + OBSERVER_OFFSET, 25)
po1.dir = (0, -300, 0)
po1.x_side = (50, 0, 0)
po1.y_side = (0, 0, -50)
po2, onode2 = create_observer_prototype(is_z=True)  # 0_0_R
po2.org = (25, -25, RADIUS - OBSERVER_OFFSET)
po2.dir = (0, 0, 300)
po2.x_side = (-50, 0, 0)
po2.y_side = (0, 50, 0)

camera_R_0_0 = create_camera((90, 0, 90), is_x=True)
camera_0_R_0 = create_camera((-90, 0, 0), is_y=True)
camera_0_0_R = create_camera((180, 0, 90), is_z=True)
for c in [camera_R_0_0, camera_0_R_0, camera_0_0_R]:
    scene.Notebook().AddCamera(c)

for n in [light_node, onode, onode1, onode2] + mesh_nodes:
    scene.AddNode(n)
cm = ColorModel([it * 10 + 370 for it in range(1, 42)])
cm.SetSpectral()
scene.color_model = cm
LoadScene(scene)

imaps = scene.IMapsParams()
imaps.req_acc = 0.01
imaps.time_limit = 300
imaps.SetObserverAsAccSource(onode1)
kernel = GetKernel()
kernel.CalculateIMaps()

if PART == Task.PART1:
    pt_params = scene.PTRenderParams()
    pt_params.is_lum = False
    pt_params.path = 'p1_'
    pt_params.time_limit = 300
    pt_params.res = (64, 64)
    pt_params.store_illum = True
    pt_params.store_irrad = True
    for cam in scene.Notebook().cameras:
        cam.Apply()
        pt_params.suffix = cam.name + '_pt'
        kernel.PTRender()
scene.Save('p{p}'.format(p=PART.value), OverwriteMode.OVERWRITE)