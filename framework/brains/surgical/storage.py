from androguard.core.analysis import analysis
from androguard.decompiler.dad import decompile
from datetime import datetime
from blessings import Terminal
t = Terminal()


class InsecureStorageEnum(object):

    values = [

        "getExternalFilesDir",
        "getSharedPreferences",
        "openFileOutput"
        "openFileInput"
    ]


class InsecureStorage(object):

    name = "storage"

    def __init__(self, apks):

        super(InsecureStorage, self).__init__()
        self.apks = apks
        self.enum = InsecureStorageEnum()

    def run(self):

        """
        Search for storage API usage within target class and methods
        """

        x = analysis.uVMAnalysis(self.apks.get_vm())
        vm = self.apks.get_vm()

        if x:
            print(t.green("[{0}] ".format(datetime.now()) + t.yellow("Performing surgery ...")))
            # Get enum values
            #
            for v in self.enum.values:
                # This returns PathP
                # objects into a list
                #
                paths = x.get_tainted_packages().search_methods("android.content.Context", "{0}".format(v), ".")

                if paths:
                    for p in paths:
                        for method in self.apks.get_methods():
                            if method.get_name() == p.get_src(vm.get_class_manager())[1]:
                                if method.get_class_name() == p.get_src(vm.get_class_manager())[0]:

                                    mx = x.get_method(method)
                                    d = decompile.DvMethod(mx)
                                    d.process()

                                    print(t.green("[{0}] ".format(datetime.now()) +
                                          t.yellow("Found: ") +
                                          "{0}".format(v)))
                                    print(t.green("[{0}] ".format(datetime.now()) +
                                                  t.yellow("Class: ") +
                                                  "{0}".format(method.get_class_name())))
                                    print(t.green("[{0}] ".format(datetime.now()) +
                                                  t.yellow("Method: ") +
                                                  "{0}".format(method.get_name())))

                                    print(method.show())
                                    print(d.get_source())
