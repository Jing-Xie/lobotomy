from androguard.core.analysis import analysis
from androguard.decompiler.dad import decompile
from datetime import datetime
from blessings import Terminal
t = Terminal()


class SocketEnum(object):

    values = {

        "java.net.ServerSocket": [

            "accept",
            "bind",
            "close",
            "getLocalPort",
            "getChannel",
            "getInetAddress",
            "getLocalSocketAddress",
            "getReceiveBufferSize",
            "getReuseAddress",
            "getSoTimeout",
            "isBound",
            "isClose",
            "setPerformancePreferences",
            "setReceiveBufferSize",
            "setReuseAddress",
            "setSoTimeout",
            "setSocketFactory"

        ]

    }


class Socket(object):

    name = "socket"

    def __init__(self, apks):

        super(Socket, self).__init__()
        self.apks = apks
        self.enum = SocketEnum()

    def run(self):

        """
        Search for socket service API implemenations
        """

        x = analysis.uVMAnalysis(self.apks.get_vm())
        vm = self.apks.get_vm()

        if x:
            print(t.green("[{0}] ".format(datetime.now()) + t.yellow("Performing surgery ...")))
            # Get enum values
            #
            for a, b in self.enum.values.items():
                for c in b:
                    paths = x.get_tainted_packages().search_methods("{0}".format(a), "{0}".format(c), ".")
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
                                              "{0}".format(c)))
                                        print(t.green("[{0}] ".format(datetime.now()) +
                                                      t.yellow("Class: ") +
                                                      "{0}".format(method.get_class_name())))
                                        print(t.green("[{0}] ".format(datetime.now()) +
                                                      t.yellow("Method: ") +
                                                      "{0}".format(method.get_name())))

                                        print(method.show())
                                        print(d.get_source())