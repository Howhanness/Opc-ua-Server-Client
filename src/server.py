
import sys
sys.path.append(".")

from IPython import embed
import opcua

class SubClient(opcua.SubscriptionClient):
    def __init_(self, *args):
        self.val = None
    def data_change(self, handle, node, val, attr):
        print("New data change event", handle, node, val, attr)
        self.val = val

    def prt(self):
        print("prt called")


if __name__ == "__main__":
    server = opcua.Server(True)
    server.set_endpoint("opc.tcp://localhost:4845")
    server.load_cpp_addressspace(True)
    #s.add_xml_address_space("standard_address_space.xml")
    #s.add_xml_address_space("user_address_space.xml")
    server.start()
    try:
        root = server.get_root_node()
        print("I got root folder: ", root)
        objects = server.get_objects_node()
        print("I got objects folder: ", objects)

        #Now adding some object to our addresse space from server side
        test = objects.add_folder("testfolder")
        myvar = test.add_variable("myvar", [16, 56])
        myprop = test.add_property("myprop", 9.9)
       
        #Now subscribing to changes on server side
        # callback does not work yet.. but soon
        sclt = SubClient()
        sub = server.create_subscription(100, sclt)
        handle = sub.subscribe_data_change(myvar) #keep handle if you want to delete the particular subscription later

        embed()
    finally:
        server.stop()

