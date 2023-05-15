from __future__ import absolute_import

import base64
import re
import sys
import traceback

from applitools.selenium.command_context import CommandContext

from .optional_deps import PlaywrightLocator

camel_to_snake = re.compile(r"([A-Z]+)")


class PlaywrightSpecDriverCommandContext(CommandContext):
    def execute_callback(self, command):
        name, key = command["name"], command["key"]
        assert name.startswith("Driver.")
        py_name = camel_to_snake.sub(r"_\1", name[7:]).lower()
        method = getattr(self, py_name)
        try:
            result = method(**command["payload"])
            self._connection.response(key, name, result)
        except Exception as exc:
            stack = "".join(traceback.format_tb(sys.exc_info()[2]))
            error = {"message": repr(exc), "stack": stack}
            self._connection.response(key, name, error=error)

    def get_driver_info(self, driver):
        return {"features": {"allCookies": True, "canExecuteOnlyFunctionScripts": True}}

    def execute_script(self, context, script, arg=None):
        page = self.object_registry.demarshal_driver(context)
        arg = self._demarshal_script_args(arg or [])
        res = page.evaluate_handle(script, arg)
        ho = self._handle_to_object(res)
        return ho

    def main_context(self, context):
        if context.get("type") == "element":
            page = self.object_registry.demarshal_element(context).page
        else:
            page = self.object_registry.demarshal_driver(context)
        return self.object_registry.marshal_driver(page.main_frame)

    def child_context(self, context, element):
        element = self.object_registry.demarshal_driver(element)
        return self.object_registry.marshal_element(element.content_frame())

    def find_element(self, context, selector, parent=None):
        if isinstance(selector, dict) and selector["type"] == "selector":
            locator = self.object_registry.demarshal_element(selector)
            element = locator.element_handle()
        else:
            selector = _convert_selector(selector)
            if parent:
                parent = self.object_registry.demarshal_driver(parent)
                element = parent.query_selector(selector)
            else:
                parent = self.object_registry.demarshal_driver(context)
                element = parent.locator(selector).element_handle()
        return self.object_registry.marshal_element(element)

    def find_elements(self, context, selector, parent=None):
        if isinstance(selector, dict) and selector["type"] == "selector":
            locator = self.object_registry.demarshal_element(selector)
            all_handles = (elem.element_handle() for elem in locator.all())
        else:
            selector = _convert_selector(selector)
            if parent:
                parent = self.object_registry.demarshal_driver(parent)
                all_handles = parent.query_selector_all(selector)
            else:
                parent = self.object_registry.demarshal_driver(context)
                locator = parent.locator(selector)
                all_handles = (elem.element_handle() for elem in locator.all())
        return [self.object_registry.marshal_element(h) for h in all_handles]

    def set_viewport_size(self, driver, size):
        page = self.object_registry.demarshal_driver(driver)
        return page.set_viewport_size(size)

    def get_viewport_size(self, driver):
        page = self.object_registry.demarshal_driver(driver)
        return page.viewport_size

    def take_screenshot(self, driver):
        page = self.object_registry.demarshal_driver(driver)
        screenshot = page.screenshot()
        return base64.b64encode(screenshot).decode()

    def get_title(self, driver):
        page = self.object_registry.demarshal_driver(driver)
        return page.title()

    def get_url(self, driver):
        page = self.object_registry.demarshal_driver(driver)
        return page.url

    def get_cookies(self, driver):
        page = self.object_registry.demarshal_driver(driver)
        cookies = page.context.cookies()
        return [
            {"expiry" if k == "expires" else k: v for k, v in cookie.items()}
            for cookie in cookies
        ]

    def _handle_to_object(self, handle):
        m = re.match(r"(?:.+@)?(\w*)(?:\(\d+\))?", str(handle), re.IGNORECASE)
        if m:
            type = m.groups()[-1].lower()
        else:
            type = None
        if type == "array":
            props = handle.get_properties()
            return [self._handle_to_object(o) for o in props.values()]
        if type == "object":
            props = handle.get_properties()
            return {k: self._handle_to_object(v) for k, v in props.items()}
        elif str(handle).startswith("JSHandle@"):
            element = handle.as_element()
            return self.object_registry.marshal_element(element)
        return handle.json_value()

    def _demarshal_script_args(self, arg):
        if isinstance(arg, dict):
            if "applitools-ref-id" in arg:
                node = self.object_registry.demarshal_element(arg)
                if isinstance(node, PlaywrightLocator):
                    return node.element_handle()
                else:
                    return node
            else:
                return {k: self._demarshal_script_args(v) for k, v in arg.items()}
        elif isinstance(arg, list):
            return [self._demarshal_script_args(i) for i in arg]
        else:
            return arg


def _convert_selector(selector):
    prefix = {"css": "css", "css selector": "css", "xpath": "xpath"}
    if isinstance(selector, dict):
        return prefix[selector["type"]] + "=" + selector["selector"]
    else:
        return selector
