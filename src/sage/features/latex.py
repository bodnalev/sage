# -*- coding: utf-8 -*-
r"""
Features for testing the presence of ``latex`` and equivalent programs
"""
# ****************************************************************************
#       Copyright (C) 2021 Sebastien Labbe <slabqc@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#                  https://www.gnu.org/licenses/
# ****************************************************************************

from . import StaticFile, Executable, FeatureTestResult, FeatureNotPresentError
from sage.features.join_feature import JoinFeature

latex_url = 'https://www.latex-project.org/'
latex_spkg = 'texlive'


class LaTeX(Executable):
    r"""
    A :class:`~sage.features.Feature` describing the presence of ``latex``

    EXAMPLES::

        sage: from sage.features.latex import latex
        sage: latex().is_present()             # optional - latex
        FeatureTestResult('latex', True)
    """
    def __init__(self, name):
        r"""
        TESTS::

            sage: from sage.features.latex import latex
            sage: isinstance(latex(), latex)
            True
        """
        Executable.__init__(self, name, executable=name, spkg=latex_spkg, url=latex_url)

    def is_functional(self):
        r"""
        Return whether ``latex`` in the path is functional.

        EXAMPLES::

            sage: from sage.features.latex import latex
            sage: latex().is_functional()             # optional - latex
            FeatureTestResult('latex', True)
        """
        lines = []
        lines.append(r"\documentclass{article}")
        lines.append(r"\begin{document}")
        lines.append(r"$\alpha+2$")
        lines.append(r"\end{document}")
        content = '\n'.join(lines)

        # create a simple tex file with the content
        from sage.misc.temporary_file import tmp_filename
        base_filename_tex = tmp_filename(ext='.tex')
        with open(base_filename_tex, 'w') as f:
            f.write(content)
        import os
        base, filename_tex = os.path.split(base_filename_tex)

        # running latex
        from subprocess import run
        cmd = [self.name, '-interaction=nonstopmode', filename_tex]
        cmd = ' '.join(cmd)
        result = run(cmd, shell=True, cwd=base, capture_output=True, text=True)

        # return
        if result.returncode == 0:
            return FeatureTestResult(self, True)
        else:
            return FeatureTestResult(self, False, reason="Running latex on "
                                     "a sample file returned non-zero "
                                     "exit status {}".format(result.returncode))


class latex(LaTeX):
    r"""
    A :class:`~sage.features.Feature` describing the presence of ``latex``

    EXAMPLES::

        sage: from sage.features.latex import latex
        sage: latex().is_present()             # optional - latex
        FeatureTestResult('latex', True)
    """
    def __init__(self):
        r"""
        TESTS::

            sage: from sage.features.latex import latex
            sage: isinstance(latex(), latex)
            True
        """
        LaTeX.__init__(self, "latex")


class pdflatex(LaTeX):
    r"""
    A :class:`~sage.features.Feature` describing the presence of ``pdflatex``

    EXAMPLES::

        sage: from sage.features.latex import pdflatex
        sage: pdflatex().is_present()             # optional - pdflatex
        FeatureTestResult('pdflatex', True)
    """
    def __init__(self):
        r"""
        TESTS::

            sage: from sage.features.latex import pdflatex
            sage: isinstance(pdflatex(), pdflatex)
            True
        """
        LaTeX.__init__(self, "pdflatex")


class xelatex(LaTeX):
    r"""
    A :class:`~sage.features.Feature` describing the presence of ``xelatex``

    EXAMPLES::

        sage: from sage.features.latex import xelatex
        sage: xelatex().is_present()             # optional - xelatex
        FeatureTestResult('xelatex', True)
    """
    def __init__(self):
        r"""
        TESTS::

            sage: from sage.features.latex import xelatex
            sage: isinstance(xelatex(), xelatex)
            True
        """
        LaTeX.__init__(self, "xelatex")


class lualatex(LaTeX):
    r"""
    A :class:`~sage.features.Feature` describing the presence of ``lualatex``

    EXAMPLES::

        sage: from sage.features.latex import lualatex
        sage: lualatex().is_present()             # optional - lualatex
        FeatureTestResult('lualatex', True)
    """
    def __init__(self):
        r"""
        TESTS::

            sage: from sage.features.latex import lualatex
            sage: isinstance(lualatex(), lualatex)
            True
        """
        LaTeX.__init__(self, "lualatex")


class TeXFile(StaticFile, JoinFeature):
    r"""
    A :class:`sage.features.Feature` describing the presence of a TeX file

    EXAMPLES::

        sage: from sage.features.latex import TeXFile
        sage: TeXFile('x', 'x.tex').is_present()  # optional: pdflatex
        FeatureTestResult('x', True)
        sage: TeXFile('nonexisting', 'xxxxxx-nonexisting-file.tex').is_present()  # optional - pdflatex
        FeatureTestResult('nonexisting', False)
    """
    def __init__(self, name, filename, **kwds):
        r"""
        EXAMPLES::

            sage: from sage.features.latex import LaTeXPackage, pdflatex
            sage: LaTeXPackage("tkz-graph")._features
            [Feature('pdflatex')]
        """
        JoinFeature.__init__(self, name, [pdflatex()],
                             spkg=latex_spkg, url=latex_url)  # see :trac:`34282`
        StaticFile.__init__(self, name, filename, search_path=[], **kwds)

    def absolute_filename(self) -> str:
        r"""
        The absolute path of the file.

        EXAMPLES::

            sage: from sage.features.latex import TeXFile
            sage: feature = TeXFile('latex_class_article', 'article.cls')
            sage: feature.absolute_filename()  # optional - pdflatex
            '.../latex/base/article.cls'
        """
        from subprocess import run, CalledProcessError, PIPE
        try:
            proc = run(['kpsewhich', self.filename],
                       stdout=PIPE, stderr=PIPE,
                       universal_newlines=True, check=True)
            return proc.stdout.strip()
        except CalledProcessError:
            raise FeatureNotPresentError(self,
                                         reason="{filename!r} not found by kpsewhich".format(filename=self.filename))

    def _is_present(self):
        r"""
        Test for the presence of the TeX-file.

        EXAMPLES::

            sage: from sage.features.latex import LaTeXPackage, pdflatex
            sage: f = LaTeXPackage("tkz-graph")
            sage: g = pdflatex()
            sage: bool(f.is_present()) == bool(g.is_present())  # indirect doctest
            True
        """
        test = JoinFeature._is_present(self)
        if not test:
            return test
        return super(TeXFile, self)._is_present()


class LaTeXPackage(TeXFile):
    r"""
    A :class:`sage.features.Feature` describing the presence of a LaTeX package
    (``.sty`` file).

    EXAMPLES::

        sage: from sage.features.latex import LaTeXPackage
        sage: LaTeXPackage('graphics').is_present()  # optional - pdflatex
        FeatureTestResult('latex_package_graphics', True)
    """
    @staticmethod
    def __classcall__(cls, package_name, **kwds):
        """
        TESTS::

            sage: from sage.features.latex import LaTeXPackage
            sage: LaTeXPackage('graphics') is LaTeXPackage('graphics')
            True
        """
        return TeXFile.__classcall__(cls,
                                     f'latex_package_{package_name}'.replace('-', '_'),
                                     f'{package_name}.sty',
                                     **kwds)


def all_features():
    return [latex(),
            pdflatex(),
            xelatex(),
            lualatex(),
            LaTeXPackage("tkz-graph")]
