# reference:  https://github.com/doconix/pyreact

__pragma__('kwargs')

registered_components = {}


class ComponentMeta(type):
    def __new__(meta, name, bases, attribs):
        cls = type.__new__(meta, name, bases, attribs)
        registered_components[name] = cls
        # override the default name='cls' property to make error messages and debugging more meaningful
        descrip = Object.getOwnPropertyDescriptor(cls, 'name');
        descrip.value = name
        Object.defineProperty(cls, 'name', descrip);
        return cls


class AbstractComponent(object, metaclass=ComponentMeta):
    '''Superclass for React Components.  Use Component below.'''
    def __init__(self, props):
        object.__init__(self)

    def render(self):
        return 'Subclass should override render()'


class Component(AbstractComponent, React.Component.prototype):
    '''Superclass for React Components.  PyReact version of React.Component'''

    def __init__(self, props):
        AbstractComponent.__init__(self)
        React.Component.apply(self, [props])


def console_log(text):
    console.log(text)


def useState(initial_value):
    '''for React hooks'''
    return React.useState(initial_value)


def element(elem, props, *children):
    '''Creates React elements using Component class and properties dictionary'''
    return React.createElement(elem, props, *children)


def render(root_class, props, container):
    '''Load main react component into DOM'''
    def main():
        ReactDOM.render(
            React.createElement(root_class, props),
            document.getElementById(container)
        )

    document.addEventListener("DOMContentLoaded", main)
