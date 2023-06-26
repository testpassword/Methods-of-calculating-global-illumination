from random import random, choice
import math
from collections import namedtuple
from time import time
from enum import Enum


Task = Enum('Task', ['PART1', 'PART2', 'PART3'])
PART = Task.PART1


class Vec3:
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, term): return Vec3(self.x + term.x, self.y + term.y, self.z + term.z)

    def __sub__(self, subtrahend): return Vec3(self.x - subtrahend.x, self.y - subtrahend.y, self.z - subtrahend.z)

    def __mul__(self, factor): return Vec3(self.x * factor, self.y * factor, self.z * factor)

    def __truediv__(self, divider): return Vec3(self.x / divider, self.y / divider, self.z / divider)

    def normalize(self):
        length = math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)
        return Vec3(self.x / length, self.y / length, self.z / length)

    def magnitude(self) -> float: return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def dot(self, v) -> float: return self.x * v.x + self.y * v.y + self.z * v.z

    def cross(self, v): return Vec3(self.y * v.z - self.z * v.y, self.z * v.x - self.x * v.z, self.x * v.y - self.y * v.x)

    def to_limicept_point(self) -> tuple: return self.x * 1000, self.y * 1000, self.z * 1000


Polygon = namedtuple('Polygon', 'v1 v2 v3')
Circle = namedtuple('Circle', 'radius center_x center_z')


def chunks(l: list, chunk_size: int):
    for i in range(0, len(l), chunk_size):
        yield l[i:i + chunk_size]


def measurable(fn: callable) -> callable:
    def inner(*args, **kwargs):
        s = time()
        res = fn(*args, **kwargs)
        f = time()
        print('{} = {} sec'.format(fn.__name__, f - s))
        return res
    return inner


def write_to_rayset_file(output_path: str, points: list):
    name = output_path.split('/')[-1].split('.')[0]
    ext = '.ray'
    if not output_path.endswith(ext):
        output_path += ext
    with open(output_path, 'w') as f:
        header = '\n'.join(['Rayset', '  Name {}'.format(name), '  ColorModel RGB', '  NormalFlux 100', '  Scale 1', '  RayNumber {}'.format(len(points)), '  RayFlux Relative', '  Rays\n']) 
        f.write(header)
        for i in range(len(points)):
            f.write('   '.join([str(it) for it in [points[i].x, points[i].z, points[i].y, DIRECTION.x, DIRECTION.z, DIRECTION.y]]) + '   1   1   1\n')


def write_to_HDR(output_path: str, points: list):
    ext = '.nit'
    if not output_path.endswith(ext):
        output_path += ext
    
    def gen_channel_template(resolution: int) -> list:
        return [[0 for _ in range(resolution)] for _ in range(resolution)]
    
    color_channels = [gen_channel_template(600) for i in range(3)]
    for p in points:
        choice(color_channels)[int(p.x)][int(p.z)] = 100  # make fun colors
    PostProcessor(PPDataUnits.ILLUMINANCE, [], *color_channels).SaveToHDR(output_path, overwrite = OverwriteMode.OVERWRITE)


@measurable
def calc_polygon_distribution(p: Polygon, size: int, offset = 0, method: str = 'mirroring') -> list:
    """
    methods: 'mirroring', 'rejecting'
    """
    points = [p.v1, p.v2, p.v3]

    def clone_with_offset(orig: Vec3) -> Vec3:
        def new_val(attr_name: str):
            val = getattr(orig, attr_name)
            return val + offset if val == 0 else val * 60 - offset
        return Vec3(new_val('x'), new_val('y'), new_val('z'))
    
    if offset != 0:
        points = [clone_with_offset(p) for p in points]
    v1_2 = points[1] - points[0]
    v1_3 = points[2] - points[0]

    def calc_point(r1, r2):
        return ((v1_2.normalize() * r1) * v1_2.magnitude()) + ((v1_3.normalize() * r2) * v1_3.magnitude()) + points[0]

    if method == 'mirroring':
        for i in range(size):
            r1, r2 = [random() for i in range(2)]
            if r1 + r2 > 1:
                r1 = 1 - r1
                r2 = 1 - r2
            points += [calc_point(r1, r2)]
    elif method == 'rejecting':
        rejected = 0
        hitted = 0
        while hitted < size:
            r1, r2 = [random() for i in range(2)]
            if r1 + r2 > 1:
                rejected += 1
                continue
            points += [calc_point(r1, r2)]
            hitted += 1
    else:
        raise ValueError('unrecognized "method" param, choose between "mirroring" and "rejecting"')
    return points


@measurable
def calc_circle_distribution(c: Circle, size: int, radius_zoom = 1, center_offset = 0, method: str = 'mirroring') -> list:
    """
    methods: 'no_rejecting', 'rejecting'
    """
    points = []
    if method == 'no_rejecting':
        for i in range(size):
            r1, r2 = [random() for i in range(2)]
            theta = 2 * math.pi * r1
            r = c.radius * radius_zoom * math.sqrt(r2)
            x = (c.center_x + center_offset) + r * math.cos(theta)
            z = (c.center_z + center_offset) + r * math.sin(theta)
            points += [Vec3(x, 0, z)]            
    elif method == 'rejecting':
        rejected = 0
        hitted = 0
        normal = DIRECTION
        v = Vec3(
            -normal.y / (normal.x + normal.y)**2,
            normal.x / (normal.x + normal.y)**2,
            0
        )
        u = normal.cross(v)
        while hitted < size:
            r1, r2 = [random() for i in range(2)]
            if r1**2 + r2**2 > 1:
                rejected += 1
                continue
            points += [normal - v * c.radius - u * c.radius + v * c.radius * 2 * r1 + u * c.radius * 2 * r2]
            hitted += 1
    else:
        raise ValueError('unrecognized "method" param, choose between "no_rejecting" and "rejecting"')
    return points
    

def calc_observer(s: Scene, o: ObserverNode):
    LoadScene(s)
    imaps = s.IMapsParams()
    imaps.req_acc = 0.01
    imaps.time_limit = 60
    imaps.SetObserverAsAccSource(o)
    KERNEL.CalculateIMaps()
    s.SaveObsResultsObsres(OverwriteMode.OVERWRITE)
    KERNEL.UnloadScene(True)


def run_for_polygon(rays_num: int):
    out_filename = 'rays_{rays_num}_polygon'.format(rays_num=rays_num)
    if PART == Task.PART1:
        write_to_rayset_file(out_filename, calc_polygon_distribution(POLYGON, rays_num))
        scene = Scene(name='polygon_scene')
        mesh = GetClass(Shape, 'Triangle')()
        mesh.p1 = polygon_vertices[0].to_limicept_point()
        mesh.p2 = polygon_vertices[1].to_limicept_point()
        mesh.p3 = polygon_vertices[2].to_limicept_point()
        mesh_node = MeshNode(mesh, name='polygon')
        light_node = LightNode(Light('polygone light', RaySet(out_filename + '.ray')))
        obs = PlaneObserver()
        obs.res = (600, 600)
        obs.phenom = ObserverData.ILLUM
        obs.org = (-500, 0, -500)
        obs.x_side = (0, 0, 11000)
        obs.y_side = (11000, 0, 0)
        obs.dir = DIRECTION.to_limicept_point()
        obs_node = ObserverNode(obs, name=out_filename)
        for n in [mesh_node, light_node, obs_node]:
            scene.AddNode(n)
        calc_observer(scene, obs_node)
    if PART == Task.PART2:
        write_to_HDR(out_filename, calc_polygon_distribution(POLYGON, rays_num, 30))
    if PART == Task.PART3:
       if rays_num == 1000 * K:
            print('comparing methods time:')
            calc_polygon_distribution(POLYGON, rays_num, method='mirroring')
            print('next...')
            calc_polygon_distribution(POLYGON, rays_num, method='rejecting')
    


def run_for_circle(rays_num: int):
    out_filename = 'rays_{rays_num}_circle'.format(rays_num=rays_num)
    if PART == Task.PART1:
        write_to_rayset_file(out_filename, calc_circle_distribution(CIRCLE, rays_num))
        scene = Scene(name='circle_scene')
        mesh = GetClass(Shape, 'Ring')()
        mesh.radius1 = 0
        mesh.radius2 = circle_radius * 1000
        mesh.rsub = 60
        mesh_node = MeshNode(mesh, name='circle')
        mesh_node.Rotate(90, 0, 0)
        light_node = LightNode(Light('circle light', RaySet(out_filename + '.ray')))
        obs = PlaneObserver()
        obs.res = (600, 600)
        obs.phenom = ObserverData.ILLUM
        obs.org = (-10000, 0, -10000)
        obs.x_side = (20000, 0, 0)
        obs.y_side = (0, 0, 20000)
        obs.dir = DIRECTION.to_limicept_point()
        obs_node = ObserverNode(obs, name=out_filename)
        for n in [mesh_node, light_node, obs_node]:
            scene.AddNode(n)
        calc_observer(scene, obs_node)
    if PART == Task.PART2:
        write_to_HDR(out_filename, calc_circle_distribution(CIRCLE, rays_num, 30, 300))
    if PART == Task.PART3:
        print('comparing methods time:')
        calc_circle_distribution(CIRCLE, rays_num, method='no_rejecting')
        print('next...')
        calc_circle_distribution(CIRCLE, rays_num, method='rejecting')


TASK_FILEPATH = 'lr2_var6.txt'
with open(TASK_FILEPATH, 'r', encoding='utf-8') as f:
    raw_task = [int(it) for it in f.readlines()[-1].split()]
polygon_vertices = [Vec3(*it) for it in chunks(raw_task[1:10], 3)]
POLYGON = Polygon(*polygon_vertices)
circle_radius = raw_task[13]
CIRCLE = Circle(circle_radius, 0, 0)
DIRECTION = Vec3(*raw_task[10:13])
K = 1000
KERNEL = GetKernel()
for rays_num in [K, 10 * K, 100 * K, 1000 * K]:
    run_for_polygon(rays_num)
    run_for_circle(rays_num)
