# this is a namespace package
# it allows multiple packages to share the 'math_utils.geometry' namespace
try:
    __import__('pkg_resources').declare_namespace(__name__)
except ImportError:
    __path__ = __import__('pkgutil').extend_path(__path__, __name__) 