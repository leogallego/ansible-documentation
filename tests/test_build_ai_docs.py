"""Tests for docs/bin/build_ai_docs.py."""

from __future__ import annotations

import subprocess
import sys
import textwrap
from pathlib import Path
from unittest.mock import patch

import pytest

# Add docs/bin to import path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "docs" / "bin"))

import build_ai_docs


class TestStripDirectives:
    """Tests for strip_directives()."""

    def test_strips_toctree(self) -> None:
        text = (
            "Some text before.\n"
            "\n"
            ".. toctree::\n"
            "   :maxdepth: 2\n"
            "\n"
            "   playbooks\n"
            "   roles\n"
            "\n"
            "Some text after.\n"
        )
        result = build_ai_docs.strip_directives(text)
        assert "toctree" not in result
        assert "playbooks" not in result
        assert "Some text before." in result
        assert "Some text after." in result

    def test_strips_versionadded(self) -> None:
        text = (
            "Feature description.\n"
            "\n"
            ".. versionadded:: 2.9\n"
            "   This feature was added in 2.9.\n"
            "\n"
            "More text.\n"
        )
        result = build_ai_docs.strip_directives(text)
        assert "versionadded" not in result
        assert "Feature description." in result
        assert "More text." in result

    def test_strips_versionchanged(self) -> None:
        text = (
            "Behavior description.\n"
            "\n"
            ".. versionchanged:: 2.10\n"
            "   The behavior changed.\n"
            "\n"
            "Continuation.\n"
        )
        result = build_ai_docs.strip_directives(text)
        assert "versionchanged" not in result
        assert "Behavior description." in result
        assert "Continuation." in result

    def test_strips_deprecated(self) -> None:
        text = (
            "Old feature.\n"
            "\n"
            ".. deprecated:: 2.8\n"
            "   Use new_feature instead.\n"
            "\n"
            "Next section.\n"
        )
        result = build_ai_docs.strip_directives(text)
        assert "deprecated" not in result
        assert "Old feature." in result
        assert "Next section." in result

    def test_strips_seealso(self) -> None:
        text = (
            "Main content.\n"
            "\n"
            ".. seealso::\n"
            "\n"
            "   :ref:`some_ref`\n"
            "      Description of the reference.\n"
            "\n"
            "Following content.\n"
        )
        result = build_ai_docs.strip_directives(text)
        assert "seealso" not in result
        assert "Main content." in result
        assert "Following content." in result

    def test_strips_contents(self) -> None:
        text = (
            "Page title\n"
            "==========\n"
            "\n"
            ".. contents::\n"
            "   :local:\n"
            "   :depth: 2\n"
            "\n"
            "Section 1\n"
            "---------\n"
        )
        result = build_ai_docs.strip_directives(text)
        assert "contents" not in result
        assert "Page title" in result
        assert "Section 1" in result

    def test_strips_meta(self) -> None:
        text = (
            ".. meta::\n"
            "   :description: A page about something\n"
            "   :keywords: ansible, automation\n"
            "\n"
            "Page content.\n"
        )
        result = build_ai_docs.strip_directives(text)
        assert "meta" not in result
        assert "Page content." in result

    def test_strips_raw(self) -> None:
        text = (
            "Some text.\n"
            "\n"
            ".. raw:: html\n"
            "\n"
            "   <div>HTML content</div>\n"
            "\n"
            "More text.\n"
        )
        result = build_ai_docs.strip_directives(text)
        assert "raw" not in result
        assert "<div>" not in result
        assert "Some text." in result
        assert "More text." in result

    def test_strips_only(self) -> None:
        text = (
            "Universal content.\n"
            "\n"
            ".. only:: builder_html\n"
            "\n"
            "   HTML-specific content.\n"
            "\n"
            "Common content.\n"
        )
        result = build_ai_docs.strip_directives(text)
        assert "only" not in result
        assert "HTML-specific" not in result
        assert "Universal content." in result
        assert "Common content." in result

    def test_strips_target_labels(self) -> None:
        text = (
            ".. _my-reference-label:\n"
            "\n"
            "Section Title\n"
            "=============\n"
            "\n"
            "Content here.\n"
        )
        result = build_ai_docs.strip_directives(text)
        assert ".. _my-reference-label:" not in result
        assert "Section Title" in result
        assert "Content here." in result

    def test_strips_substitution_definitions(self) -> None:
        text = (
            ".. |project| replace:: Ansible\n"
            "\n"
            "Welcome to |project| documentation.\n"
        )
        result = build_ai_docs.strip_directives(text)
        assert ".. |project|" not in result
        assert "Welcome to |project| documentation." in result

    def test_strips_comments(self) -> None:
        text = (
            "Visible text.\n"
            "\n"
            ".. This is a comment\n"
            "   that spans multiple lines.\n"
            "\n"
            "More visible text.\n"
        )
        result = build_ai_docs.strip_directives(text)
        assert "This is a comment" not in result
        assert "Visible text." in result
        assert "More visible text." in result

    def test_strips_single_line_comment(self) -> None:
        text = (
            "Before.\n"
            "\n"
            ".. A single-line comment\n"
            "\n"
            "After.\n"
        )
        result = build_ai_docs.strip_directives(text)
        assert "single-line comment" not in result
        assert "Before." in result
        assert "After." in result

    def test_preserves_note_directive(self) -> None:
        text = (
            ".. note::\n"
            "\n"
            "   This is important.\n"
            "\n"
            "Other text.\n"
        )
        result = build_ai_docs.strip_directives(text)
        assert "note" in result
        assert "This is important." in result

    def test_preserves_warning_directive(self) -> None:
        text = (
            ".. warning::\n"
            "\n"
            "   Be careful!\n"
            "\n"
        )
        result = build_ai_docs.strip_directives(text)
        assert "warning" in result
        assert "Be careful!" in result

    def test_preserves_code_block_directive(self) -> None:
        text = (
            ".. code-block:: yaml\n"
            "\n"
            "   - hosts: all\n"
            "     tasks: []\n"
            "\n"
        )
        result = build_ai_docs.strip_directives(text)
        assert "code-block" in result
        assert "hosts: all" in result

    def test_preserves_important_directive(self) -> None:
        text = (
            ".. important::\n"
            "\n"
            "   Do not skip this.\n"
            "\n"
        )
        result = build_ai_docs.strip_directives(text)
        assert "important" in result
        assert "Do not skip this." in result

    def test_preserves_tip_directive(self) -> None:
        text = (
            ".. tip::\n"
            "\n"
            "   A useful tip.\n"
            "\n"
        )
        result = build_ai_docs.strip_directives(text)
        assert "tip" in result
        assert "A useful tip." in result

    def test_preserves_hint_directive(self) -> None:
        text = (
            ".. hint::\n"
            "\n"
            "   A helpful hint.\n"
            "\n"
        )
        result = build_ai_docs.strip_directives(text)
        assert "hint" in result
        assert "A helpful hint." in result

    def test_preserves_danger_directive(self) -> None:
        text = (
            ".. danger::\n"
            "\n"
            "   This is dangerous.\n"
            "\n"
        )
        result = build_ai_docs.strip_directives(text)
        assert "danger" in result
        assert "This is dangerous." in result

    def test_preserves_caution_directive(self) -> None:
        text = (
            ".. caution::\n"
            "\n"
            "   Exercise caution.\n"
            "\n"
        )
        result = build_ai_docs.strip_directives(text)
        assert "caution" in result
        assert "Exercise caution." in result

    def test_preserves_literalinclude_directive(self) -> None:
        text = (
            ".. literalinclude:: example.yml\n"
            "   :language: yaml\n"
            "\n"
        )
        result = build_ai_docs.strip_directives(text)
        assert "literalinclude" in result

    def test_preserves_highlight_directive(self) -> None:
        text = (
            ".. highlight:: yaml\n"
            "\n"
            "Some text.\n"
        )
        result = build_ai_docs.strip_directives(text)
        assert "highlight" in result

    def test_preserves_code_directive(self) -> None:
        text = (
            ".. code:: python\n"
            "\n"
            "   print('hello')\n"
            "\n"
        )
        result = build_ai_docs.strip_directives(text)
        assert "code::" in result
        assert "print('hello')" in result

    def test_preserves_surrounding_content(self) -> None:
        text = (
            "First paragraph.\n"
            "\n"
            ".. toctree::\n"
            "   :maxdepth: 1\n"
            "\n"
            "   item1\n"
            "   item2\n"
            "\n"
            "Second paragraph.\n"
            "\n"
            ".. note::\n"
            "\n"
            "   Keep this note.\n"
            "\n"
            "Third paragraph.\n"
        )
        result = build_ai_docs.strip_directives(text)
        assert "First paragraph." in result
        assert "Second paragraph." in result
        assert "Third paragraph." in result
        assert "Keep this note." in result
        assert "toctree" not in result

    def test_collapses_excessive_newlines(self) -> None:
        text = (
            "Before.\n"
            "\n"
            ".. toctree::\n"
            "   :maxdepth: 1\n"
            "\n"
            "   item\n"
            "\n"
            "\n"
            "\n"
            "After.\n"
        )
        result = build_ai_docs.strip_directives(text)
        assert "\n\n\n" not in result
        assert "Before." in result
        assert "After." in result

    def test_strips_multiple_directives(self) -> None:
        text = (
            ".. versionadded:: 2.9\n"
            "   Added.\n"
            "\n"
            "Content.\n"
            "\n"
            ".. deprecated:: 2.10\n"
            "   Removed.\n"
            "\n"
            "More content.\n"
        )
        result = build_ai_docs.strip_directives(text)
        assert "versionadded" not in result
        assert "deprecated" not in result
        assert "Content." in result
        assert "More content." in result

    def test_strips_multiline_substitution(self) -> None:
        text = (
            ".. |long_sub| replace::\n"
            "   A very long\n"
            "   substitution text.\n"
            "\n"
            "Visible.\n"
        )
        result = build_ai_docs.strip_directives(text)
        assert "long_sub" not in result
        assert "Visible." in result


class TestConvertRoles:
    """Tests for convert_roles()."""

    def test_ref_with_display_text(self) -> None:
        text = "See :ref:`User Guide <user_guide>` for details."
        result = build_ai_docs.convert_roles(text)
        assert result == "See User Guide for details."

    def test_ref_without_display_text(self) -> None:
        text = "See :ref:`user_guide` for details."
        result = build_ai_docs.convert_roles(text)
        assert result == "See user_guide for details."

    def test_doc_with_display_text(self) -> None:
        text = "Read the :doc:`Installation Guide <installation>`."
        result = build_ai_docs.convert_roles(text)
        assert result == "Read the Installation Guide."

    def test_doc_without_display_text(self) -> None:
        text = "Read the :doc:`installation`."
        result = build_ai_docs.convert_roles(text)
        assert result == "Read the installation."

    def test_term_role(self) -> None:
        text = "A :term:`playbook` is a YAML file."
        result = build_ai_docs.convert_roles(text)
        assert result == "A playbook is a YAML file."

    def test_guilabel_role(self) -> None:
        text = "Click the :guilabel:`Save` button."
        result = build_ai_docs.convert_roles(text)
        assert result == "Click the Save button."

    def test_mod_role(self) -> None:
        text = "Use the :mod:`os.path` module."
        result = build_ai_docs.convert_roles(text)
        assert result == "Use the ``os.path`` module."

    def test_func_role(self) -> None:
        text = "Call :func:`my_function` to start."
        result = build_ai_docs.convert_roles(text)
        assert result == "Call ``my_function`` to start."

    def test_class_role(self) -> None:
        text = "The :class:`MyClass` provides this."
        result = build_ai_docs.convert_roles(text)
        assert result == "The ``MyClass`` provides this."

    def test_meth_role(self) -> None:
        text = "Use :meth:`obj.run` to execute."
        result = build_ai_docs.convert_roles(text)
        assert result == "Use ``obj.run`` to execute."

    def test_attr_role(self) -> None:
        text = "Access :attr:`obj.name` for the name."
        result = build_ai_docs.convert_roles(text)
        assert result == "Access ``obj.name`` for the name."

    def test_command_role(self) -> None:
        text = "Run :command:`ansible-playbook site.yml`."
        result = build_ai_docs.convert_roles(text)
        assert result == "Run ``ansible-playbook site.yml``."

    def test_file_role(self) -> None:
        text = "Edit :file:`/etc/ansible/hosts`."
        result = build_ai_docs.convert_roles(text)
        assert result == "Edit ``/etc/ansible/hosts``."

    def test_envvar_role(self) -> None:
        text = "Set :envvar:`ANSIBLE_CONFIG` to override."
        result = build_ai_docs.convert_roles(text)
        assert result == "Set ``ANSIBLE_CONFIG`` to override."

    def test_option_role(self) -> None:
        text = "Use :option:`--verbose` for details."
        result = build_ai_docs.convert_roles(text)
        assert result == "Use ``--verbose`` for details."

    def test_program_role(self) -> None:
        text = "The :program:`ansible` command."
        result = build_ai_docs.convert_roles(text)
        assert result == "The ``ansible`` command."

    def test_literal_role(self) -> None:
        text = "Use :literal:`some_value` here."
        result = build_ai_docs.convert_roles(text)
        assert result == "Use ``some_value`` here."

    def test_code_role(self) -> None:
        text = "The :code:`return_code` variable."
        result = build_ai_docs.convert_roles(text)
        assert result == "The ``return_code`` variable."

    def test_ansplugin_with_type(self) -> None:
        text = "Use :ansplugin:`ansible.builtin.copy#module`."
        result = build_ai_docs.convert_roles(text)
        assert result == "Use ``ansible.builtin.copy``."

    def test_ansplugin_without_type(self) -> None:
        text = "Use :ansplugin:`ansible.builtin.copy`."
        result = build_ai_docs.convert_roles(text)
        assert result == "Use ``ansible.builtin.copy``."

    def test_ansopt_with_fqcn_and_type(self) -> None:
        text = "Set :ansopt:`ansible.builtin.copy#module:dest`."
        result = build_ai_docs.convert_roles(text)
        assert result == "Set ``dest``."

    def test_ansopt_simple(self) -> None:
        text = "Set :ansopt:`dest`."
        result = build_ai_docs.convert_roles(text)
        assert result == "Set ``dest``."

    def test_ansretval(self) -> None:
        text = "Check :ansretval:`ansible.builtin.command#module:stdout`."
        result = build_ai_docs.convert_roles(text)
        assert result == "Check ``stdout``."

    def test_ansoptref(self) -> None:
        text = "See :ansoptref:`ansible.builtin.copy#module:src`."
        result = build_ai_docs.convert_roles(text)
        assert result == "See ``src``."

    def test_abbr_with_expansion(self) -> None:
        text = "Use :abbr:`YAML (YAML Ain't Markup Language)` format."
        result = build_ai_docs.convert_roles(text)
        assert result == "Use YAML format."

    def test_abbr_without_expansion(self) -> None:
        text = "Use :abbr:`YAML` format."
        result = build_ai_docs.convert_roles(text)
        assert result == "Use YAML format."

    def test_multiple_roles_in_one_line(self) -> None:
        text = (
            "Use :command:`ansible-playbook` with :option:`--check` "
            "and :ref:`see the guide <guide>`."
        )
        result = build_ai_docs.convert_roles(text)
        assert result == (
            "Use ``ansible-playbook`` with ``--check`` "
            "and see the guide."
        )

    def test_preserves_non_role_backticks(self) -> None:
        text = "Use ``literal text`` and :command:`ansible`."
        result = build_ai_docs.convert_roles(text)
        assert "``literal text``" in result
        assert "``ansible``" in result

    def test_no_roles_unchanged(self) -> None:
        text = "Plain text with no roles at all."
        result = build_ai_docs.convert_roles(text)
        assert result == text

    def test_ref_display_text_lowercase(self) -> None:
        """Verify :ref: with display text uses display, not target."""
        text = ":ref:`Click here <some_target>`"
        result = build_ai_docs.convert_roles(text)
        assert result == "Click here"
        assert "some_target" not in result


class TestResolveIncludes:
    """Tests for resolve_includes()."""

    def test_resolves_relative_include(self, tmp_path: Path) -> None:
        snippet = tmp_path / "shared_snippets" / "snippet.txt"
        snippet.parent.mkdir()
        snippet.write_text("Included content here.\n")
        rst_file = tmp_path / "guide.rst"
        text = "Before.\n\n.. include:: shared_snippets/snippet.txt\n\nAfter.\n"
        result = build_ai_docs.resolve_includes(text, rst_file)
        assert "Included content here." in result
        assert ".. include::" not in result
        assert "Before." in result
        assert "After." in result

    def test_missing_include_removed_silently(self, tmp_path: Path) -> None:
        rst_file = tmp_path / "guide.rst"
        text = "Before.\n\n.. include:: nonexistent/file.txt\n\nAfter.\n"
        result = build_ai_docs.resolve_includes(text, rst_file)
        assert ".. include::" not in result
        assert "Before." in result
        assert "After." in result

    def test_no_includes_unchanged(self, tmp_path: Path) -> None:
        rst_file = tmp_path / "guide.rst"
        text = "Just plain text.\n\nNo includes here.\n"
        result = build_ai_docs.resolve_includes(text, rst_file)
        assert result == text


class TestDiscoverRstFiles:
    """Tests for discover_rst_files()."""

    def _create_rst_tree(self, tmp_path: Path) -> Path:
        """Create a realistic RST directory tree for testing."""
        rst_dir = tmp_path / "rst"
        rst_dir.mkdir()
        # Top-level files (should be excluded)
        (rst_dir / "404.rst").write_text("Not found.\n")
        (rst_dir / "ansible_index.rst").write_text("Index.\n")
        (rst_dir / "core_index.rst").write_text("Core index.\n")
        # Subdirectory with content files
        guide = rst_dir / "playbook_guide"
        guide.mkdir()
        (guide / "playbooks.rst").write_text("Playbooks.\n")
        (guide / "roles.rst").write_text("Roles.\n")
        (guide / "index.rst").write_text("Guide index.\n")
        # Another subdirectory
        dev = rst_dir / "dev_guide"
        dev.mkdir()
        (dev / "developing_modules.rst").write_text("Modules.\n")
        # Excluded directories
        images = rst_dir / "images"
        images.mkdir()
        (images / "logo.rst").write_text("Logo.\n")
        snippets = rst_dir / "shared_snippets"
        snippets.mkdir()
        (snippets / "with2loop.rst").write_text("Snippet.\n")
        return rst_dir

    def test_finds_rst_files(self, tmp_path: Path) -> None:
        rst_dir = self._create_rst_tree(tmp_path)
        result = build_ai_docs.discover_rst_files(rst_dir)
        names = [f.name for f in result]
        assert "playbooks.rst" in names
        assert "roles.rst" in names
        assert "developing_modules.rst" in names

    def test_excludes_index_rst(self, tmp_path: Path) -> None:
        rst_dir = self._create_rst_tree(tmp_path)
        result = build_ai_docs.discover_rst_files(rst_dir)
        names = [f.name for f in result]
        assert "index.rst" not in names

    def test_excludes_top_level_files(self, tmp_path: Path) -> None:
        rst_dir = self._create_rst_tree(tmp_path)
        result = build_ai_docs.discover_rst_files(rst_dir)
        names = [f.name for f in result]
        assert "404.rst" not in names
        assert "ansible_index.rst" not in names
        assert "core_index.rst" not in names

    def test_excludes_images_dir(self, tmp_path: Path) -> None:
        rst_dir = self._create_rst_tree(tmp_path)
        result = build_ai_docs.discover_rst_files(rst_dir)
        parents = [f.parent.name for f in result]
        assert "images" not in parents

    def test_excludes_shared_snippets_dir(self, tmp_path: Path) -> None:
        rst_dir = self._create_rst_tree(tmp_path)
        result = build_ai_docs.discover_rst_files(rst_dir)
        parents = [f.parent.name for f in result]
        assert "shared_snippets" not in parents

    def test_returns_sorted_paths(self, tmp_path: Path) -> None:
        rst_dir = self._create_rst_tree(tmp_path)
        result = build_ai_docs.discover_rst_files(rst_dir)
        assert result == sorted(result)


class TestConvertRstToMd:
    """Tests for convert_rst_to_md()."""

    def test_converts_heading(self) -> None:
        rst = "My Heading\n==========\n\nSome body text.\n"
        result = build_ai_docs.convert_rst_to_md(rst)
        assert "# My Heading" in result
        assert "Some body text." in result

    def test_converts_code_block(self) -> None:
        rst = (
            "Example:\n"
            "\n"
            ".. code-block:: yaml\n"
            "\n"
            "   - hosts: all\n"
            "     tasks: []\n"
            "\n"
        )
        result = build_ai_docs.convert_rst_to_md(rst)
        assert "```" in result
        assert "- hosts: all" in result

    def test_converts_bullet_list(self) -> None:
        rst = (
            "Items:\n"
            "\n"
            "- First item\n"
            "- Second item\n"
            "- Third item\n"
        )
        result = build_ai_docs.convert_rst_to_md(rst)
        assert "First item" in result
        assert "Second item" in result
        assert "Third item" in result

    def test_converts_note_to_callout(self) -> None:
        rst = (
            ".. note::\n"
            "\n"
            "   This is an important note.\n"
            "\n"
        )
        result = build_ai_docs.convert_rst_to_md(rst)
        assert "important note" in result

    def test_raises_on_missing_pandoc(self, monkeypatch: pytest.MonkeyPatch) -> None:
        def fake_run(*args: object, **kwargs: object) -> None:
            raise FileNotFoundError("No such file or directory: 'pandoc'")

        monkeypatch.setattr(subprocess, "run", fake_run)
        with pytest.raises(SystemExit):
            build_ai_docs.convert_rst_to_md("Some RST text.")


class TestPostprocessMd:
    """Tests for postprocess_md()."""

    def test_strips_span_id_tags(self) -> None:
        text = '<span id="my-anchor"></span>\n\n# Heading\n'
        result = build_ai_docs.postprocess_md(text)
        assert "<span" not in result
        assert "# Heading" in result

    def test_strips_div_blocks(self) -> None:
        text = (
            'Some text.\n\n<div class="contents" local="">\n\n'
            "- item1\n- item2\n\n</div>\n\nMore text.\n"
        )
        result = build_ai_docs.postprocess_md(text)
        assert "<div" not in result
        assert "</div>" not in result
        assert "Some text." in result
        assert "More text." in result

    def test_strips_toctree_div(self) -> None:
        text = (
            "Before.\n\n"
            '<div class="toctree-wrapper compound">\n\n'
            "- entry1\n- entry2\n\n"
            "</div>\n\n"
            "After.\n"
        )
        result = build_ai_docs.postprocess_md(text)
        assert "<div" not in result
        assert "</div>" not in result
        assert "Before." in result
        assert "After." in result

    def test_strips_versionadded_div(self) -> None:
        text = (
            "Feature text.\n\n"
            '<div class="versionadded">\n\n'
            "New in version 2.9.\n\n"
            "</div>\n\n"
            "More text.\n"
        )
        result = build_ai_docs.postprocess_md(text)
        assert "<div" not in result
        assert "</div>" not in result
        assert "Feature text." in result
        assert "More text." in result

    def test_preserves_code_blocks(self) -> None:
        text = "```yaml\n- hosts: all\n  tasks: []\n```\n"
        result = build_ai_docs.postprocess_md(text)
        assert "```yaml" in result
        assert "- hosts: all" in result

    def test_collapses_excessive_blank_lines(self) -> None:
        text = "First.\n\n\n\n\nSecond.\n"
        result = build_ai_docs.postprocess_md(text)
        assert "\n\n\n" not in result
        assert "First." in result
        assert "Second." in result


class TestExtractTitle:
    """Tests for extract_title()."""

    def test_extracts_h1_title(self) -> None:
        md = "# Ansible playbooks\n\nText.\n"
        result = build_ai_docs.extract_title(md)
        assert result == "Ansible playbooks"

    def test_extracts_h1_with_trailing_whitespace(self) -> None:
        md = "# Loops  \n\nText.\n"
        result = build_ai_docs.extract_title(md)
        assert result == "Loops"

    def test_returns_untitled_when_no_heading(self) -> None:
        md = "Just plain text.\n"
        result = build_ai_docs.extract_title(md)
        assert result == "Untitled"

    def test_ignores_h2_for_title(self) -> None:
        md = "## Section heading\n\nSome text.\n\n# Actual title\n\nMore text.\n"
        result = build_ai_docs.extract_title(md)
        assert result == "Actual title"


class TestGetAudience:
    """Tests for get_audience()."""

    def test_dev_guide_is_developer(self) -> None:
        assert build_ai_docs.get_audience("dev_guide") == "developer"

    def test_playbook_guide_is_author(self) -> None:
        assert build_ai_docs.get_audience("playbook_guide") == "author"

    def test_inventory_guide_is_author(self) -> None:
        assert build_ai_docs.get_audience("inventory_guide") == "author"

    def test_unknown_topic_is_both(self) -> None:
        assert build_ai_docs.get_audience("network") == "both"

    def test_reference_appendices_is_both(self) -> None:
        assert build_ai_docs.get_audience("reference_appendices") == "both"


class TestExtractSummary:
    """Tests for extract_summary()."""

    def test_extracts_first_paragraph(self) -> None:
        md = "# Title\n\nThis is the intro paragraph about playbooks.\n\nMore details.\n"
        result = build_ai_docs.extract_summary(md)
        assert result == "This is the intro paragraph about playbooks."

    def test_truncates_long_summary(self) -> None:
        long_text = "A" * 200
        md = f"# Title\n\n{long_text}\n\nMore.\n"
        result = build_ai_docs.extract_summary(md)
        assert len(result) <= 120
        assert result.endswith("...")

    def test_takes_first_sentence_from_long_paragraph(self) -> None:
        md = (
            "# Title\n\n"
            "First sentence here. Second sentence continues with more detail. "
            "Third sentence wraps up.\n\n"
            "Another paragraph.\n"
        )
        result = build_ai_docs.extract_summary(md)
        assert result == "First sentence here."

    def test_returns_empty_when_no_content(self) -> None:
        md = "# Title\n"
        result = build_ai_docs.extract_summary(md)
        assert result == ""
