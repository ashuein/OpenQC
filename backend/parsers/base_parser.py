"""
Abstract base parser for instrument file ingestion.

Every concrete parser (e.g. QuantStudio, BioRad, Roche) must subclass
`BaseParser` and implement the three abstract methods below.

Contract
--------
* ``can_handle`` inspects lightweight file metadata (name, extension,
  magic bytes, etc.) and returns True if *this* parser knows how to
  read the file.
* ``parse`` accepts raw file bytes and an optional column-mapping
  configuration, returning a **canonical** parsed dataset dict.
  The dict must never contain UI-formatted objects -- downstream
  consumers rely on a stable, schema-documented structure.
* ``normalize_instrument_name`` returns a consistent, lower-case
  instrument identifier string used for audit trails and database
  lookups (e.g. ``"quantstudio-5"``).
"""

from abc import ABC, abstractmethod


class BaseParser(ABC):
    """Abstract base class that every instrument-file parser must implement."""

    @abstractmethod
    def can_handle(self, file_metadata: dict) -> bool:
        """Determine whether this parser supports the given file.

        Parameters
        ----------
        file_metadata : dict
            Lightweight metadata about the uploaded file.  Expected keys
            include ``"filename"`` (str) and ``"content_type"`` (str);
            implementations may inspect additional keys.

        Returns
        -------
        bool
            ``True`` if this parser can parse the described file.
        """
        ...

    @abstractmethod
    def parse(
        self,
        file_bytes: bytes,
        mapping_config: dict | None = None,
    ) -> dict:
        """Parse raw file bytes into a canonical dataset dictionary.

        Parameters
        ----------
        file_bytes : bytes
            The complete file content.
        mapping_config : dict | None, optional
            An optional column-mapping configuration that tells the parser
            how to map instrument-specific column names to canonical field
            names.  When ``None``, the parser should use its built-in
            defaults.

        Returns
        -------
        dict
            A canonical parsed dataset.  Must conform to the project's
            shared schema -- never return UI-formatted objects.
        """
        ...

    @abstractmethod
    def normalize_instrument_name(self) -> str:
        """Return a normalised, lower-case instrument identifier.

        The string is used in audit trails and database lookups, so it
        must be deterministic and consistent across calls (e.g.
        ``"quantstudio-5"``, ``"biorad-cfx96"``).

        Returns
        -------
        str
            A stable, lower-case instrument name.
        """
        ...
