from random import random
import math
from collections import namedtuple


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


def write_to_rayset_file(output_path: str, points: list):
    name = output_path.split('/')[-1].split('.')[0]
    ext = '.ray'
    if not output_path.endswith(ext):
        output_path += ext
    with open(output_path, 'w') as f:
        header = '\n'.join(['Rayset', '  Name {}'.format(name), '  ColorModel RGB', '  NormalFlux 100', '  Scale 1', '  RayNumber {}'.format(len(points)), '  RayFlux Relative', '  Rays\n']) 
        f.write(header)
        for i in range(len(points)):
            f.write('   '.join([str(it) for it in [points[i].x, points[i].y, points[i].z] * 2]) + '   1   1   1\n')


def calc_sphere_distribution(size: int, method: str) -> list:
    """
    methods: 'uniform', 'lambert'
    """

    def to_vec() -> Vec3:
        r1, r2 = [random() for i in range(2)]
        h = -RADUIS + 2 * RADUIS * r1
        phi = 2 * math.pi * r2
        theta = math.acos(h / RADUIS)
        x = RADUIS * math.sin(theta) * math.cos(phi)
        y = RADUIS * math.cos(theta)
        z = RADUIS * math.sin(theta) * math.sin(phi)
        return Vec3(x, y, z) if method == 'uniform' else (Vec3(x, y, z) + Vec3(0, RADUIS, 0)).normalize()
    
    return [to_vec() for _ in range(size)]
    

def calc_observer(rayset_path: str):
    s = Scene(name=rayset_path.split('/')[-1].split('.')[0])
    LoadScene(s)
    light_node = LightNode(Light('sphere light', RaySet(rayset_path)))
    light_tr = Transform()
    if 'uniform' in rayset_path:
        light_tr.azim = 180
        light_tr.tilt = 90
        light_tr.rot = 180
        light_node.tr = light_tr
    obs = GonioObserver()
    obs.res = 180, 91
    obs.thresh_ang = 180
    obs.dir = 0, 0, 346
    obs.greenwich = 346, 0, 0
    obs_node = ObserverNode(obs)
    for n in [light_node, obs_node]:
        s.AddNode(n)
    imaps = s.IMapsParams()
    imaps.req_acc = 0.01
    imaps.time_limit = 60
    KERNEL.CalculateIMaps()
    s.SaveObsResultsObsres(OverwriteMode.OVERWRITE)
    KERNEL.UnloadScene(True)


def run_uniform(rays_num: int):
    print('run uniform for {}'.format(rays_num))
    out_filename = 'rays_{rays_num}_uniform.ray'.format(rays_num=rays_num)
    write_to_rayset_file(out_filename, calc_sphere_distribution(rays_num, 'uniform'))
    calc_observer(out_filename)


def run_lambert(rays_num: int):
    print('run lambert for {}'.format(rays_num))
    out_filename = 'rays_{rays_num}_lambert.ray'.format(rays_num=rays_num)
    write_to_rayset_file(out_filename, calc_sphere_distribution(rays_num, 'lambert'))
    calc_observer(out_filename)


TASK_FILEPATH = 'lr2_var6.txt'
with open(TASK_FILEPATH, 'r', encoding='utf-8') as f:
    raw_task = [int(it) for it in f.readlines()[-1].split()]
RADUIS = raw_task[13]
DIRECTION = Vec3(*raw_task[10:13])
K = 1000
KERNEL = GetKernel()
for rays_num in [10 * K, 100 * K, 1000 * K]:
    run_uniform(rays_num)
    run_lambert(rays_num)
