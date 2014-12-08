from libs.olacabs_service import OlacabsService
import libs.helper_functions as helper_functions
from test_service_base import ServiceTester

class TestOlacabsService(ServiceTester):
    @property
    def service(self):
        return OlacabsService

    def test_name(self):
        self.assertEqual(self.name, "Olacabs")
