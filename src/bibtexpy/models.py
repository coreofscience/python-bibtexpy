from typing import Dict, List, Union


class Macro:
    """
    Wrapper for a macro name. To be resolved later.
    """

    def __init__(self, name: str):
        self.name = name

    def __repr__(self) -> str:
        return f'Macro("{self.name}")'

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, self.__class__):
            return False
        return self.name == o.name


class Concat:
    """
    Represents an string or macro concatenation.
    """

    def __init__(self, pieces: List[Union[str, Macro]]) -> None:
        self.pieces = pieces

    def __repr__(self) -> str:
        return f"Concat({self.pieces})"

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, self.__class__):
            return False
        return self.pieces == o.pieces


class MacroDefinition:
    """
    A macro definition, associates the name of a macro with it's actual value.
    """

    def __init__(self, name: str, value: Concat) -> None:
        self.name = name
        self.value = value

    def __repr__(self) -> str:
        return f'MacroDefinition(name="{self.name}", value={self.value})'

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, self.__class__):
            return False
        return self.name == o.name and self.value == o.value


class Entry:
    def __init__(self, _type: str, key: str, fields: List[MacroDefinition]) -> None:
        self._type = _type
        self.key = key
        self.fields = fields

    def __repr__(self) -> str:
        return f'Entry(_type="{self._type}", key="{self.key}", fields={self.fields})'

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, self.__class__):
            return False
        return self._type == o._type and self.key == o.key and self.fields == o.fields


class BibContext:
    """
    Context to resolve a bib file.
    """

    def __init__(self, pieces: List[Union[MacroDefinition, Entry]]) -> None:
        self._pieces = pieces
        self.entries: Dict[str, Entry] = {
            e.key: e for e in self._pieces if isinstance(e, Entry)
        }
        self.macros: Dict[str, Concat] = {
            e.name: e.value for e in self._pieces if isinstance(e, MacroDefinition)
        }

    def __repr__(self) -> str:
        return f"BibContext(pieces={self._pieces})"

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, self.__class__):
            return False
        return self._pieces == o._pieces