from component import Component
from GasTurbineEfficiency import compressor_efficiency
from GasTurbineEfficiency import combustor_efficiency
from GasTurbineEfficiency import turbine_efficiency
from GasTurbineEfficiency import lookupTable


class Leaf(Component):
    """
    The Leaf class represents the end objects of a composition. A leaf can't
    have any children.

    Usually, it's the Leaf objects that do the actual work, whereas Composite
    objects only delegate to their sub-components.
    """

    def __init__(self,name) -> None:
        self.name = name 

    def operation(self) -> str:
        if self.name == "Compressor":
            data = self.get_data
            compressor_efficiency()
        if self.name == "Combustor":
            combustor_efficiency()
        if self.name == "Turbine":
            turbine_efficiency()
        return  
    
    