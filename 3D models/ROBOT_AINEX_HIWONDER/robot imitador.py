import pyvista as pv
import os

# Rutas absolutas (funciona desde cualquier lugar)
ruta_robot = r"C:\Users\saulo\OneDrive\Desktop\Robot imitador\Modelo 3D\ROBOT_AINEX_HIWONDER\robot\robot.stl"
ruta_exo   = r"C:\Users\saulo\OneDrive\Desktop\Robot imitador\Modelo 3D\ROBOT_AINEX_HIWONDER\Exo\exoesqueleto.stl"

# Verificar archivos
if not os.path.exists(ruta_robot):
    print("❌ No se encontró robot.stl")
    exit()

if not os.path.exists(ruta_exo):
    print("❌ No se encontró exoesqueleto.stl")
    exit()

# Cargar modelos
robot = pv.read(ruta_robot)
exo   = pv.read(ruta_exo)

# Crear entorno 3D
plotter = pv.Plotter()
plotter.set_background("white")

# Agregar robot
plotter.add_mesh(
    robot,
    color="lightgray",
    show_edges=True,
    opacity=1.0
)

# Agregar exoesqueleto (color distinto)
plotter.add_mesh(
    exo,
    color="orange",
    show_edges=True,
    opacity=0.7
)

# Ejes globales
plotter.show_axes()

# Texto informativo
plotter.add_text(
    "Robot AINEX + Exoesqueleto\nEnsamblaje STL",
    position="upper_left",
    font_size=12
)

# Mostrar
plotter.show()
