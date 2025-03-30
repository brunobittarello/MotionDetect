# from pyptz.onvif_control import ONVIFCamera

# print('554')
# onvif_camera = ONVIFCamera('192.168.0.44', '554', 'admin', 'senha123')
# print('onvif_camera')
# pan, tilt, zoom = onvif_camera.get_ptz_status()
# print(pan, tilt, zoom)

from zeep.client import AsyncClient

class AsyncClient(AsyncClient):
    def create_service(self, binding_name, address):
        """Create a new AsyncServiceProxy for the given binding name and address.

        :param binding_name: The QName of the binding
        :param address: The address of the endpoint

        """
        print("HEERE")
        try:
            binding = self.wsdl.bindings[binding_name]
        except KeyError:
            raise ValueError(
                "No binding found with the given QName. Available bindings "
                "are: %s" % (", ".join(self.wsdl.bindings.keys()))
            )
        return AsyncServiceProxy(self, binding, address=address)

# 554
# 5000
from onvif import ONVIFCamera
print('ONVIFCamera 5000')
mycam = ONVIFCamera('192.168.0.45', 5000, 'admin', 'senha123', '')
print('Fim')