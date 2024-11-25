def test_mesh_point_size(server):

    server.call("mesh.register", [{"id": "123456789", "file_name": "vertex_attribute.vtp"}])
    assert server.compare_image(3, "register.jpeg") == True

    server.call("mesh.point_size", [{"id": "123456789", "size": 10}])
    assert server.compare_image(3, "mesh_point_size.jpeg") == True
