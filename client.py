from component import Component
from leaf import Leaf
from composite import Composite

# def client_code(component: Component) -> None:
#     """
#     The client code works with all of the components via the base interface.
#     """

#     print(f"RESULT: {component.operation()}", end="")


# def client_code2(component1: Component, component2: Component) -> None:
#     """
#     Thanks to the fact that the child-management operations are declared in the
#     base Component class, the client code can work with any component, simple or
#     complex, without depending on their concrete classes.
#     """

#     if component1.is_composite():
#         component1.add(component2)

#     print(f"RESULT: {component1.operation()}", end="")

# # This way the client code can support the simple leaf components...
# simple = Leaf()
# print("Client: I've got a simple component:")
# client_code(simple)
# print("\n")

# simple2 = Leaf()
# # ...as well as the complex composites.
# tree = Composite()

# tree.add(simple)
# tree.add(simple2)
# client_code(tree)

# block = Composite()
# block.add(tree)
# client_code(block)

# branch1 = Composite()
# branch1.add(Leaf())
# branch1.add(Leaf())

# branch2 = Composite()
# branch2.add(Leaf())

# tree.add(branch1)
# tree.add(branch2)

# print("Client: Now I've got a composite tree:")
# client_code(tree)
# print("\n")

# print("Client: I don't need to check the components classes even when managing the tree:")
# client_code2(tree, simple)


Engine = Composite("Gasturbine")
# Engine.set_SensorID()
Engine.set_supparam()