# SPDX-FileCopyrightText: 2025 IObundle
#
# SPDX-License-Identifier: MIT

# This module contains utility functions and decorators for the API interface.
# These functions should only be used by Py2HWSW developers.

import inspect
import importlib

from dataclasses import field, Field

from iob_base import fail_with_msg

#
# Utility functions
#


def empty_list():
    return field(default_factory=list)


def empty_dict():
    return field(default_factory=dict)


def get_field_default_value(field_obj):
    """Parse a given dataclass field to get the default value."""
    if field_obj.default_factory is not None:
        return field_obj.default_factory()
    return field_obj.default


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
    return internal_obj.get_api_obj()


def convert2internal(api_obj):
    """
    Convert given API object to corresponding internal object.

    Attributes:
        api_obj (object): API object
    Returns:
        object: internal object
    """
    return api_obj._get_py2hwsw_internal_obj()


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


# A constant random value that is very unlikely to be used by user/developer code.
# This value is used to distinguish between automated API calls and user/developer code calls.
SPECIAL_ARGUMENT_VALUE = "special_argument_value"


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
        # Store annotations for access in subclasses if needed
        if not hasattr(cls, "__parent_annotations"):
            cls.__parent_annotations = {}
        # Append currrent class annotations to ones inherited from parent
        all_annotations = cls.__parent_annotations | cls.__annotations__
        cls.__parent_annotations = all_annotations

        # Store class dict for access in subclasses if needed
        if not hasattr(cls, "__parent_dict"):
            cls.__parent_dict = {}
        # Append current class dict to ones inherited from parent
        all_dict = cls.__parent_dict | cls.__dict__
        cls.__parent_dict = all_dict

        # Get attributes and their default values
        attributes = {k: all_dict[k] for k in all_annotations}
        local_methods = get_local_methods(cls)

        # Update constructor of the API class
        def new_init(self, *args, **kwargs):
            # For debug:
            # print("API class constructor called: ", cls.__name__)
            # print("Attributes: ", attributes)
            # print("Annotations: ", all_annotations)
            # print("Methods: ", get_methods(cls))

            # Instantiate internal class with API attributes
            internal_obj = internal_cls(
                SPECIAL_ARGUMENT_VALUE,  # Special internal argument to identify API calls
                self,
                attributes,
                all_annotations,
                args,
                kwargs,
            )

            # Store reference to internal object
            self.__internal_obj = internal_obj

        cls.__init__ = new_init

        # Local utility functions
        def _generate_setter(attribute_name, datatype):
            """
            Function to generate setter for a given attribute.
            Setter will pass the given value to the corresponding attribute in the internal object.
            """

            def setter(self, value):
                # print("Setter called for attribute: ", attribute_name)
                setattr(self.__internal_obj, attribute_name, value)

            setter.__doc__ = f"""\
            Setter for the '{attribute_name}' attribute.
            Args:
                {attribute_name} ({datatype}): Value to set for '{attribute_name}'.
            """

            return setter

        def _generate_getter(attribute_name, datatype):
            """
            Function to generate getter for a given attribute.
            Getter will get value from the corresponding attribute in the internal object.
            """

            def getter(self):
                # print("Getter called for attribute: ", attribute_name)
                return getattr(self.__internal_obj, attribute_name)

            getter.__doc__ = f"""\
                Getter for the '{attribute_name}' attribute.
                Returns:
                    {datatype}: Value of '{attribute_name}'.
                """

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
                return getattr(self.__internal_obj, method_name)(*args, **kwargs)

            return wrapper

        # Generate and add setters/getters for each attribute of API class, referencing values from corresponding attribute in internal object
        for name, datatype in cls.__annotations__.items():
            datatype_name = (
                datatype.__name__ if hasattr(datatype, "__name__") else datatype
            )
            setattr(cls, f"set_{name}", _generate_setter(name, datatype_name))
            setattr(cls, f"get_{name}", _generate_getter(name, datatype_name))

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

        def get_supported_attributes(self):
            """
            Get all attributes supported by the API class of this object.

            Returns:
                dict: Dictionary with attribute name and type
            """
            return self.__class__.__parent_annotations

        cls.get_supported_attributes = get_supported_attributes

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


def internal_api_class(api_module, api_class_name, allow_unknown_args=False):
    """
    Decorator for internal classes that extend functionality of API classes.

    This decorator:
    1) Adds constructor that accepts new attributes via arguments (the ones defined in the API class).

    Attributes received by constructor will be added to this internal class.

    The constructor is intended to be automatically called by the scripts generated with the @api_class_for decorator.

    If any py2hwsw script tries to call the constructor of the decorated class directly, the call will be redirected to the constructor of corresponding API class. So, calling the constructor of internal class will actually return an object of corresponding API class!

    Attributes:
        api_module (str): module in which the API class is defined. Example: "user_api.api"
        api_class_name (str): name of the API class. Example: "iob_conf"
        allow_unknown_args (bool): if True, allow extra (unknown) arguments in 'args' and 'kwargs'. These will be passed to the internal class constructor. If false, fail with error (same as dataclass behaviour).
    """

    def decorator(cls):
        original_init = cls.__init__

        def replacement_new(cls, *args, **kwargs):
            if len(args) != 6 or args[0] != SPECIAL_ARGUMENT_VALUE:
                # Someone tried to instantiate this class directly, instead of the API class.

                # fail_with_msg(
                #     f"Py2HWSW bug: Internal class '{cls.__name__}' must not be instantiated directly! Please instantiate API class instead."
                # )

                # Lazy import the corresponding API class and automatically instantiate it
                api_class = getattr(importlib.import_module(api_module), api_class_name)
                return api_class(*args, **kwargs)

            # Return the normal __new__ method
            return object.__new__(cls)

        # Update constructor of the internal class
        def replacement_init(
            self,
            special_argument,  # Special internal argument to identify api calls
            api_object_reference,
            new_attributes,
            new_attributes_annotations,
            user_args,
            user_kwargs,
        ):
            # For debug:
            # print("Internal class constructor called: ", cls.__name__)
            # print("Received attributes: ", new_attributes)
            # print("kwargs attributes: ", user_args)

            # Update internal class attributes. Use user values if present, else use default values.
            for attribute_name, default_value in new_attributes.items():
                user_value = user_kwargs.pop(attribute_name, None)
                # If attribute is a dataclass field, get its default value
                if type(default_value) is Field:
                    default_value = get_field_default_value(default_value)
                # TODO: Maybe add some data type validation here before setting value.
                setattr(self, attribute_name, user_value or default_value)
            # Update attributes type hints
            self.__class__.__annotations__ |= new_attributes_annotations

            # If allow_unknown_arguments is False:
            #     Behave similar to dataclass: Throw error if there are unknown arguments (args/kwargs that do not match attributes).
            if not allow_unknown_args:
                # Known user_args/kwargs have been popped out. Any remaining ones are unknown.
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
            original_init(self, *user_args, **user_kwargs)

        cls.__new__ = replacement_new
        cls.__init__ = replacement_init

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

    return decorator
