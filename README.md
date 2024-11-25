# ReproduceVtkPointsVisibilityError

python3 -m venv venv
source venv/bin/activate
pip install pytest pytest-xprocess
pip install vtk
pip install -e .
pytest
