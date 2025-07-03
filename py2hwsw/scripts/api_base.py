# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

import inspect

from dataclasses import field

from iob_base import fail_with_msg

#
# Utility functions
#


def empty_list():
    return field(default_factory=list)


def empty_dict():
    return field(default_factory=dict)


#
# API-Internal object conversion functions
#


def convert2api(internal_obj):
    """
    Convert given internal object to corresponding API object.

    Attributes:
        internal_obj (object): internal object
    Returns:
        object: api object
    """
    pass


def convert2internal(api_obj):
    """
    Convert given API object to corresponding internal object.

    Attributes:
        api_obj (object): API object
    Returns:
        object: internal object
    """
    pass


#
# API functions
#


def get_methods(cls):
    """
    Returns all non-default methods in a class (includes ones inherited from superclasses)

    Attributes:
        cls (class): class
    Returns:
        dict: methods of the class and their type hints
    """
    methods = {}
    for name in dir(cls):
        attr = getattr(cls, name)
        if inspect.isfunction(attr) and not name.startswith("__"):
            signature = inspect.signature(attr)
            methods[name] = signature
    return methods


def get_local_methods(cls):
    """
    Returns all non-default methods in a class (does NOT include ones inherited from superclasses)

    Attributes:
        cls (class): class
    Returns:
        dict: methods of the class and their type hints
    """
    methods = {}
    for name in cls.__dict__:
        attr = getattr(cls, name)
        if inspect.isfunction(attr) and not name.startswith("__"):
            signature = inspect.signature(attr)
            methods[name] = signature
    return methods


def has_body(func):
    """Check if a function has a body."""
    source = inspect.getsource(func)
    body = source.strip().split("\n")[1:]
    if (len(body) == 1 or (len(body) > 1 and '"' in body[-2])) and body[
        -1
    ].strip() == "pass":
        return False
    return True


def api_for(internal_reference):
    """
    Decorator for API classes and methods.
    """
    # Check if reference is class
    if isinstance(internal_reference, type):
        return api_class_for(internal_reference)
    # Check if reference is function
    elif callable(internal_reference):
        return api_method_for(internal_reference)


def api_class_for(internal_cls):
    """
    Decorator for creating class API interface. Apply this decorator to every class in the API.

    This decorator:
    1) Passes attributes defined in the API class to the internal class (via arguments to the internal classes's constructor)
    2) Creates setters/getters for every attribute of API class, but actually accessing internal classes's attributes.
    3) Replaces (abstract) API methods with functions that call the corresponding internal class methods.
    4) Removes attributes from API class. This prevents user from trying to access attributes directly.

    From point of view of the user (even when checking api.py code), he only sees API class with the (getters/setters of the) attributes and methods defined in it.
    The user may instantiate any API class and use its attributes/methods. This decorator will handle the instantiation of the internal class and hide it from user.

    With this decorator, when the user instantiates API class, two objects are created: the API object and the internal object.
    The API object is returned to user. The internal object is stored internally by py2.
    The API and internal objects have a unique id and are associated with each other in a mapping stored internally by py2.

    When py2 needs to pass objects to the user, py2 should only pass API objects (converting from internal objects if needed).
    When the user needs to pass objects to py2, he passes API objects, which py2 will convert to internal objects.

    Attributes:
        internal_cls (class): Reference to internal class that will extend functionality of API class being decorated.
    Returns:
        class: Updated API class
    """

    # Create decorator dynamically for the API class
    def decorator(cls):
        # Get attributes and their default values
        attributes = {k: cls.__dict__[k] for k in cls.__annotations__}
        local_methods = get_local_methods(cls)
        methods = get_methods(cls)

        # Update constructor of the API class
        def new_init(self, *args, **kwargs):
            print("API class constructor called: ", cls.__name__)
            print(
                "Attributes: ", attributes
            )  # Dictionary with attributes and their types
            print(
                "Annotations: ", cls.__annotations__
            )  # Dictionary with attributes and their types
            print("Methods: ", methods)  # Dictionary with methods and their types

            # Instantiate internal class with API attributes
            internal_obj = internal_cls(
                self, attributes, cls.__annotations__, args, kwargs
            )

            # Store reference to internal object
            self.__internal_obj = internal_obj

        cls.__init__ = new_init

        # Local utility functions
        def _generate_setter(attribute_name):
            """
            Function to generate setter for a given attribute.
            Setter will pass the given value to the corresponding attribute in the internal object.
            """

            def setter(self, value):
                # print("Setter called for attribute: ", attribute_name)
                setattr(self.__internal_obj, attribute_name, value)

            return setter

        def _generate_getter(attribute_name):
            """
            Function to generate getter for a given attribute.
            Getter will get value from the corresponding attribute in the internal object.
            """

            def getter(self):
                # print("Getter called for attribute: ", attribute_name)
                return getattr(self.__internal_obj, attribute_name)

            return getter

        def _generate_method_wrapper(method_name):
            """
            Function to generate wrapper for a given method.
            Wrapper will call the corresponding method in the internal object.
            """

            def wrapper(self, *args, **kwargs):
                assert hasattr(
                    self.__internal_obj, method_name
                ), f"[Py2HWSW bug]: Missing implementation for API method '{method_name}' of class '{cls.__name__}'!"
                # print("Method called: ", method_name)
                return getattr(self.__internal_obj, method_name)(*args, **kwargs)

            return wrapper

        # Generate and add setters/getters for each attribute of API class, referencing values from corresponding attribute in internal object
        for name in cls.__annotations__:
            setattr(cls, f"set_{name}", _generate_setter(name))
            setattr(cls, f"get_{name}", _generate_getter(name))

        # Replace API methods by calls to the internal methods
        for name in local_methods:
            # Ensure method is abstract (does not have body) in API class
            assert not has_body(
                getattr(cls, name)
            ), f"API method '{name}' must be abstract."

            # Call corresponding method in internal class
            setattr(cls, name, _generate_method_wrapper(name))

        # Remove class attributes from API class
        # This will make sure user cannot access them directly.
        for name in cls.__annotations__:
            # Note: This only removes attribute from class, but not from __annotations__.
            delattr(cls, name)

        # Create getter to obtain internal object
        # Method name start with '_' to signal that user should not call it. Maybe we could find a way to prevent the user from calling it entirely?
        def _get_py2hwsw_internal_obj(self):
            """
            Method to convert API object to internal Py2HWSW object.
            This method should NOT be called by user code!

            Py2HWSW may call this method for API objects obtained from the user. This allows Py2HWSW to access extended functionality of internal objects.
            User should never have access to internal objects, so this method is reserved for Py2HWSW.

            Returns:
                internal_obj (object): internal Py2HWSW object
            """
            return self.__internal_obj

        cls._get_py2hwsw_internal_obj = _get_py2hwsw_internal_obj

        return cls

    return decorator


def api_method_for(internal_method):
    """
    Decorator for creating method API interface. Apply this decorator to every isolated method in the API.

    This decorator:
    1) Replaces the (abstract) API method with a new one that calls the corresponding internal method.

    """

    # Create decorator dynamically for the API class
    def decorator(func):
        return internal_method

    return decorator


#
# Internal functions
#


def api_class(cls):
    """
    Decorator for internal methods that extend functionality of API methods.

    This decorator:
    1) Adds constructor that accepts new attributes via arguments (the ones defined in the API class).

    Attributes received by constructor will be added to this internal class.

    """

    original_init = cls.__init__

    # Update constructor of the internal class
    def new_init(self, *args, **kwargs):
        if len(args) != 5:
            fail_with_msg(
                f"Py2HWSW bug: Internal class '{cls.__name__}' must not be instantiated directly! Please instantiate API class instead."
            )
        else:
            api_object_reference = args[0]  # object
            new_attributes = args[1]  # dict
            new_attributes_annotations = args[2]  # dict
            user_args = args[3]  # list
            user_kwargs = args[4]  # dict

        print("Internal class constructor called: ", cls.__name__)
        print("Received attributes: ", new_attributes)

        # Update internal class attributes
        for attribute_name, default_value in new_attributes.items():
            setattr(
                self, attribute_name, user_kwargs.pop(attribute_name, default_value)
            )
        # Update attributes type hints
        self.__class__.__annotations__ |= new_attributes_annotations

        # Throw error if there are unknown arguments
        if user_args:
            fail_with_msg(
                f"Unknown constructor arguments for class '{cls.__name__}': {user_args}"
            )
        if user_kwargs:
            fail_with_msg(
                f"Unknown constructor arguments for class '{cls.__name__}': {user_kwargs}"
            )

        # Store reference to API object
        self.__api_obj = api_object_reference

        # Call original init
        original_init(self)

    cls.__init__ = new_init

    # Create getter to obtain API object
    def get_api_obj(self):
        """
        Method to convert internal Py2HWSW object to API object.
        Py2HWSW should call this method for every internal object before passing it to the user.

        Returns:
            api_obj (object): API object. This object can be passed and freely modified by the user.
        """
        return self.__api_obj

    cls.get_api_obj = get_api_obj

    return cls
