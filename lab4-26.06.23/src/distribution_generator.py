from random import uniform, random
from math import pi, cos, sin, radians


def parse_table(table_filename: str) -> dict:
    dgr_table = {}
    with open(table_filename, 'r') as f:
        raw_table = [l.replace('\n', '') for l in f.readlines()]
    for i, line in enumerate(raw_table):
        if 'def' not in line:
            k, v = line.split()
            dgr_table[k] = float(v) if v.replace('.', '').isnumeric() else v
        else:
            # delta angle counting
            step = 180 / (dgr_table['theta'] - 1)
            result = []
            for j in range(i + 1, len(raw_table) - 1):
                result += list(map(lambda phi: (len(result) * step, float(phi)), raw_table[j].split()))
            dgr_table['def'] = result
            break
    return dgr_table


def binary_search(v: list, n: float) -> tuple:
    l = 0
    r = len(list(filter(None, v))) + 2
    while (l + 1) < r:
        m = int((l + r) / 2)
        if v[m] < n:
            l = m
        else:
            r = m
    return r, l


def dgr_to_sphere_distribution(dgr_table_path: str, rays_num: int):
    dgr_dict = parse_table(dgr_table_path)
    thetas = [radians(idx * 6) for idx, theta in enumerate(dgr_dict['def'])]
    probably_angle_phi = [sin(thetas[idx]) * theta[1] for idx,theta in enumerate(dgr_dict['def'])]
    integral = []
    
    for i, _ in enumerate(probably_angle_phi):
         # by trapezoid method
        integral_of_sample = lambda: ((thetas[i] - thetas[i - 1]) * (probably_angle_phi[i] + probably_angle_phi[i - 1]) / 2) + integral[i - 1] if integral[i - 1:] else 0
        integral += [integral_of_sample()]

    max_val = max(integral)
    integral = [theta / max_val for theta in integral]  # distribution function

    def gen_ray() -> tuple:
        r, l = binary_search(integral, random())
        interpol = 0
        rnd_local_intensity = dgr_dict['NormalFlux']
        # interolation to reduce lines on graph
        while rnd_local_intensity > interpol:
            rnd_theta = uniform(thetas[l], thetas[r])
            interpol = probably_angle_phi[l] + (probably_angle_phi[r] - probably_angle_phi[l])/(thetas[r]-thetas[l]) * (rnd_theta - thetas[l])
            rnd_local_intensity = uniform(0, max(probably_angle_phi[l], probably_angle_phi[r]))
        fi = 2 * pi * random()
        return RADIUS * sin(rnd_theta) * cos(fi), cos(rnd_theta) * RADIUS, RADIUS * sin(rnd_theta) * sin(fi)  # x, y, z
    
    return [gen_ray() for _ in range(rays_num)]


def write_to_rayset_file(output_path: str, rays: list):
    name = output_path.split('/')[-1].split('.')[0]
    ext = '.ray'
    if not output_path.endswith(ext):
        output_path += ext
    with open(output_path, 'w') as f:
        header = '\n'.join(['Rayset', '  Name {}'.format(name), '  ColorModel RGB', '  NormalFlux 100', '  Scale 0.0010000', '  RayNumber {}'.format(len(rays)), '  RayFlux Relative', '  Rays\n']) 
        f.write(header)
        for r in rays:
            f.write('	{r[0]}   {r[1]}   {r[2]}   {r[0]}   {r[1]}   {r[2]}   1   1   1\n'.format(r=r))


def create_observer_prototype(name: str, width: int, height: int) -> ObserverNode:
    return ObserverNode(
        GonioObserver(
            res=(width, height), 
            phenom=ObserverData.ILLUM
        ), 
        name=name
    )


K = 1000
RADIUS = 1
KERNEL = GetKernel()
for rays_num in [10 * K, 100 * K, 1 * K * K, 10 * K * K]:
    rayset_path = 'rays_{}.ray'.format(rays_num)
    print('generating of {}'.format(rayset_path))
    write_to_rayset_file(rayset_path, dgr_to_sphere_distribution('lambert.dgr', rays_num))
    scene = Scene(name=rayset_path.split('/')[-1].split('.')[0])
    for n in [
        LightNode(
            Light(
                'sphere light', 
                RaySet(rayset_path), 
                total_flux=pi * 1000
            )
        ), 
        # DO NOT CREATE OBSERVERS WITH RES HEIGHT == 91 LIKE IT'S SAID IN THE TASK, THE MINIMAL HEIGHT SHOULD BE 100
        create_observer_prototype('distribution', 180, 100), 
        create_observer_prototype('plot', 1, 100)
    ]: 
        scene.AddNode(n)
    LoadScene(scene)
    imaps = scene.IMapsParams()
    imaps.time_limit = 10
    print('calculating imaps for {}'.format(scene.name))
    KERNEL.CalculateIMaps()
    scene.SaveObsResultsObsres(OverwriteMode.OVERWRITE)
    KERNEL.UnloadScene(True)
