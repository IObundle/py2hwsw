# User API for interfacing with Py2HWSW
#
# Py2HWSW has 3 user interfaces in total:
# - Dictionary/JSON interface
# - Short notation interface
# - API interface

# To achieve backwards compatibility, consider the following best practices:
#
# - Add new methods, don't change existing ones:
#       When adding new functionality, introduce new methods or interfaces instead of
#       modifying existing ones. This ensures that existing user code will not break.
# - Use default values or optional parameters:
#       When adding new parameters to existing methods, use default values or make
#       them optional to avoid breaking existing user code.
# - Avoid removing methods or interfaces:
#       Once a method or interface is published, avoid removing it in future versions.
#       Instead, consider deprecating it and providing a replacement or alternative
#       implementation.
# - Document changes and deprecations:
#       Clearly document any changes, deprecations, or removals in your API, including
#       the version number or identifier where the change occurred. This helps users
#       understand the impact of updates and plan accordingly.


from abc import ABC, abstractmethod

# NOTE: Update version every time API changes!
API_VERSION = "1.0"

#
# Example of abstract classes
#


class Printable(ABC):
    @abstractmethod
    def print(self):
        pass


class Shareable(ABC):
    @abstractmethod
    def share(self):
        pass


#
# Confs
#

# Each conf has:
# name: str = ""
# kind: str = "P"
# value: str | int | bool = ""
# min_value: str | int = "NA"
# max_value: str | int = "NA"
# descr: str = "Default description"
# if_defined: str = ""
# if_not_defined: str = ""
# doc_only: bool = False

# Each group of confs may have:
# name: str = ""
# descr: str = "Default description"
# confs: list = field(default_factory=list) # List of confs
# doc_only: bool = False
# doc_clearpage: bool = False
