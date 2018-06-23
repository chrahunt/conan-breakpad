import os

from conans import ConanFile, CMake, tools
from conans.errors import ConanException
from six import StringIO


class BreakpadTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    def build(self):
        cmake = CMake(self)
        # Current dir is "test_package/build/<build_id>" and CMakeLists.txt is
        # in "test_package"
        cmake.configure()
        cmake.build()

    def test(self):
        if tools.cross_building(self.settings):
            return
        with tools.chdir("bin"):
            # Take output explicitly to hide expected "Segmentation fault"
            # message
            buf = StringIO()
            try:
                self.run(".%sexample" % os.sep, output=buf)
                raise RuntimeError('example should have crashed!')
            except ConanException as e:
                # should be "Error 35584 while executing ./example"
                output = buf.getvalue()
                if 'Segmentation fault' not in output or 'Dump path' not in output:
                    self.output.error(
                        'Expected error not found while executing example.\n'
                        'Output:\n{}'.format(buf.getvalue()))
                    raise
