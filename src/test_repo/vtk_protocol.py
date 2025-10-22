# Standard library imports
import os

# Third party imports
import vtkmodules.vtkRenderingVolumeOpenGL2
from vtkmodules.web import protocols as vtk_protocols
from vtkmodules.vtkIOXML import vtkXMLGenericDataObjectReader
from vtkmodules.vtkRenderingCore import vtkDataSetMapper, vtkActor
from wslink import register as exportRpc

# Local application imports

class VtkView(vtk_protocols.vtkWebProtocol):
    def __init__(self):
        super().__init__()
        self.DATA_FOLDER_PATH = os.getenv("DATA_FOLDER_PATH")

    def get_data_base(self):
        return self.getSharedObject("db")

    def get_renderer(self):
        return self.getSharedObject("renderer")

    def get_object(self, id):
        return self.get_data_base()[id]

    def get_protocol(self, name):
        for p in self.coreServer.getLinkProtocols():
            if type(p).__name__ == name:
                return p

    def render(self, view=-1):
        self.get_protocol("vtkWebPublishImageDelivery").imagePush({"view": view})

    def register_object(self, id, reader, filter, actor, mapper, textures):
        self.get_data_base()[id] = {
            "reader": reader,
            "filter": filter,
            "actor": actor,
            "mapper": mapper,
            "textures": textures,
        }

    def deregister_object(self, id):
        del self.get_data_base()[id]


    @exportRpc("mesh.register")
    def registerMesh(self, params):
        print(f"{params=}", flush=True)
        id = params["id"]
        file_name = params["file_name"]
        reader = vtkXMLGenericDataObjectReader()
        filter = {}
        mapper = vtkDataSetMapper()
        mapper.SetInputConnection(reader.GetOutputPort())
        actor = vtkActor()
        self.register_object(id, reader, filter, actor, mapper, {})

        reader.SetFileName(os.path.join(self.DATA_FOLDER_PATH, file_name))

        actor.SetMapper(mapper)
        mapper.SetColorModeToMapScalars()
        mapper.SetResolveCoincidentTopologyLineOffsetParameters(1, -0.1)
        mapper.SetResolveCoincidentTopologyPolygonOffsetParameters(2, 0)
        mapper.SetResolveCoincidentTopologyPointOffsetParameter(-2)

        renderWindow = self.getView("-1")
        renderer = renderWindow.GetRenderers().GetFirstRenderer()
        renderer.AddActor(actor)
        renderer.ResetCamera()
        renderWindow.Render()
        self.render()








    


    