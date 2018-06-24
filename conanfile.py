from conans import ConanFile, AutoToolsBuildEnvironment, tools
import os


class BreakpadConan(ConanFile):
    name = "breakpad"
    version = "master"
    license = "BSD-3-Clause"
    url = "https://chromium.googlesource.com/breakpad/breakpad"
    description = (
        "Breakpad is a set of client and server components which implement"
        " a crash-reporting system.")
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "fPIC": [True, False],
        "include_breakpad": [True, False],
        "include_breakpad_client": [True, False]
    }
    default_options = "fPIC=True", "include_breakpad=True", "include_breakpad_client=True"
    generators = "cmake"

    source_subfolder = "source_subfolder"
    build_subfolder = "build_subfolder"

    def source(self):
        gsource_template = "{}/+archive/{}.tar.gz"
        source_path = gsource_template.format(self.url, self.version)
        tools.get(source_path, destination=self.source_subfolder)
        lss_url = "https://chromium.googlesource.com/linux-syscall-support"
        lss_path = gsource_template.format(lss_url, "master")
        tools.get(
            lss_path,
            destination=os.path.join(
                self.source_subfolder, "src", "third_party", "lss"))

    def build(self):
        source_folder = os.path.abspath(self.source_subfolder)
        package_folder = os.path.abspath(self.package_folder)
        tools.mkdir(self.build_subfolder)
        with tools.chdir(self.build_subfolder):
            autotools = AutoToolsBuildEnvironment(self)
            autotools.configure(
                    configure_dir=source_folder,
                    args=["--prefix={}".format(package_folder)])
            autotools.make()
            autotools.install()

    def package(self):
        with tools.chdir(self.package_folder):
            tools.mkdir('license')
            os.rename('share/doc/breakpad-0.1/LICENSE', 'license/LICENSE')
            tools.rmdir('share')

    def package_info(self):
        # Required since breakpad headers assume it is at the top-level.
        self.cpp_info.includedirs = ["include/breakpad"]
        libs = []
        if self.options.include_breakpad:
            libs.append("breakpad")
        if self.options.include_breakpad_client:
            libs.append("breakpad_client")
        self.cpp_info.libs = libs
        if not self.settings.os == "Windows":
            self.cpp_info.cppflags = ["-pthread"]
        self.env_info.path.append(os.path.join(self.package_folder, "bin"))
