from __future__ import absolute_import

from typing import TYPE_CHECKING

from ..common.object_registry import ObjectRegistry, RefId
from .optional_deps import PlaywrightLocator

if TYPE_CHECKING:
    from typing import Text


class PlaywrightSpecDriverObjectRegistry(ObjectRegistry):
    def __init__(self):
        # type: () -> None
        super(PlaywrightSpecDriverObjectRegistry, self).__init__()
        self._objects = []

    def marshal_driver(self, driver):
        return {"applitools-ref-id": self._obj2id(driver)}

    def demarshal_driver(self, obj):
        return self._id2obj(obj["applitools-ref-id"])

    def marshal_element(self, element):
        # USDK needs to differentiate Locators, to call findElements to resolve them
        obj_type = "selector" if isinstance(element, PlaywrightLocator) else "element"
        return {"applitools-ref-id": self._obj2id(element), "type": obj_type}

    def demarshal_element(self, obj):
        return self._id2obj(obj["applitools-ref-id"])

    def _obj2id(self, object):
        # type: (object) -> Text
        try:
            idx = self._objects.index(object)
        except ValueError:
            self._objects.append(object)
            idx = len(self._objects) - 1
        return str(RefId(self.id, str(idx)))

    def _id2obj(self, objid):
        # type: (Text) -> object
        ref_id = RefId.from_str(objid)
        assert ref_id.object_registry_id == self.id, "Object belongs to this registry"
        return self._objects[int(ref_id.obj_id)]
