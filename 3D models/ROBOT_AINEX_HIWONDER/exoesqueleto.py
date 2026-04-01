import pyvista as pv
import os

# Ruta absoluta del STL
ruta_stl = r"C:\Users\saulo\OneDrive\Desktop\Robot imitador\Modelo 3D\ROBOT_AINEX_HIWONDER\Exo\exoesqueleto.stl"

if not os.path.exists(ruta_stl):
    print("❌ No se encontró el archivo STL")
    exit()

# Cargar modelo
mesh = pv.read(ruta_stl)

# Obtener límites
xmin, xmax, ymin, ymax, zmin, zmax = mesh.bounds
dx = xmax - xmin
dy = ymax - ymin
dz = zmax - zmin

# Crear visor
plotter = pv.Plotter()
plotter.set_background("white")

# Agregar el modelo
plotter.add_mesh(
    mesh,
    color="lightgray",
    show_edges=True
)

# Agregar ejes globales
plotter.show_axes()

# ---- MEDIDAS VISUALES ----

# Línea X
line_x = pv.Line((xmin, ymin, zmin), (xmax, ymin, zmin))
plotter.add_mesh(line_x, color="red", line_width=3)
plotter.add_point_labels(
    [(xmin + xmax)/2, ymin, zmin],
    [f"X = {dx:.2f} mm"],
    font_size=14,
    text_color="red"
)

# Línea Y
line_y = pv.Line((xmin, ymin, zmin), (xmin, ymax, zmin))
plotter.add_mesh(line_y, color="green", line_width=3)
plotter.add_point_labels(
    [xmin, (ymin + ymax)/2, zmin],
    [f"Y = {dy:.2f} mm"],
    font_size=14,
    text_color="green"
)

# Línea Z
line_z = pv.Line((xmin, ymin, zmin), (xmin, ymin, zmax))
plotter.add_mesh(line_z, color="blue", line_width=3)
plotter.add_point_labels(
    [xmin, ymin, (zmin + zmax)/2],
    [f"Z = {dz:.2f} mm"],
    font_size=14,
    text_color="blue"
)

# Texto informativo
plotter.add_text(
    "Entorno 3D – Robot AINEX\nMedidas reales del STL",
    position="upper_left",
    font_size=12
)

# Mostrar entorno
plotter.show()
