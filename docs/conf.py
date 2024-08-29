from __future__ import annotations


extensions = [
    'sphinx.ext.autodoc',
    'jaraco.packaging.sphinx',
]

master_doc = "index"
html_theme = "furo"

# Link dates and other references in the changelog
extensions += ['rst.linker']
link_files = {
    '../NEWS.rst': dict(
        using=dict(GH='https://github.com'),
        replace=[
            dict(
                pattern=r'(Issue #|\B#)(?P<issue>\d+)',
                url='{package_url}/issues/{issue}',
            ),
            dict(
                pattern=r'(?m:^((?P<scm_version>v?\d+(\.\d+){1,2}))\n[-=]+\n)',
                with_scm='{text}\n{rev[timestamp]:%d %b %Y}\n',
            ),
            dict(
                pattern=r'PEP[- ](?P<pep_number>\d+)',
                url='https://peps.python.org/pep-{pep_number:0>4}/',
            ),
        ],
    )
}

# Be strict about any broken references
nitpicky = True
nitpick_ignore: list[tuple[str, str]] = []

# Include Python intersphinx mapping to prevent failures
# jaraco/skeleton#51
extensions += ['sphinx.ext.intersphinx']
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
}

# Preserve authored syntax for defaults
autodoc_preserve_defaults = True

# Add support for linking usernames, PyPI projects, Wikipedia pages
github_url = 'https://github.com/'
extlinks = {
    'user': (f'{github_url}%s', '@%s'),
    'pypi': ('https://pypi.org/project/%s', '%s'),
    'wiki': ('https://wikipedia.org/wiki/%s', '%s'),
}
extensions += ['sphinx.ext.extlinks']

# local

extensions += ['jaraco.tidelift']

# jaraco/jaraco.collections#11
nitpick_ignore += [
    ('py:class', 'v, remove specified key and return the corresponding value.'),
    ('py:class', 'None.  Update D from dict/iterable E and F.'),
    ('py:class', 'D[k] if k in D, else d.  d defaults to None.'),
]

nitpick_ignore += [
    ('py:class', 're.Pattern'),
]

# jaraco/jaraco.collections#16
nitpick_ignore += [
    ('py:class', 'SupportsKeysAndGetItem'),
    ('py:class', '_RangeMapKT'),
    ('py:class', '_VT'),
    ('py:class', '_T'),
    ('py:class', 'jaraco.collections._RangeMapKT'),
    ('py:class', 'jaraco.collections._VT'),
    ('py:class', 'jaraco.collections._T'),
    ('py:obj', 'jaraco.collections._RangeMapKT'),
    ('py:obj', 'jaraco.collections._VT'),
]
