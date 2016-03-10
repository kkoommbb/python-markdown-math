# -*- coding: utf-8 -*-

'''
Math extension for Python-Markdown
==================================

Adds support for displaying math formulas using [MathJax](http://www.mathjax.org/).

Author: 2015, Dmitry Shachnev <mitya57@gmail.com>.
'''

import markdown
import random

class MathExtension(markdown.extensions.Extension):
    def __init__(self, *args, **kwargs):
        self.config = {
            'enable_dollar_delimiter': [False, 'Enable single-dollar delimiter'],
        }
        super(MathExtension, self).__init__(*args, **kwargs)

    def extendMarkdown(self, md, md_globals):
        def handle_match_inline(m):
            node = markdown.util.etree.Element('span')
            node.set('class', 'equation')
            script_node = markdown.util.etree.SubElement(node, 'script')
            script_id = ''.join([random.choice('0123456789') for i in range(10)])
            script_node.set('id', script_id)
            script_node.text = markdown.util.AtomicString(
                'katex.render("{}", document.getElementById("{}").parentNode);'.format(markdown.util.AtomicString(m.group(3)), script_id))
            return node

        def handle_match(m):
            node = markdown.util.etree.Element('div')
#            node.set('class', 'equation')
#            node.set('displayMode', 'True')
#            node.set('type', 'math/tex; mode=display')
            node.set('class', 'equation')
            script_node = markdown.util.etree.SubElement(node, 'script')
            if '\\begin' in m.group(2):
#                node.set('data-expr', markdown.util.AtomicString(m.group(2) + m.group(4) + m.group(5)))
                script_node.text = markdown.util.AtomicString(
                    'katex.render("{}", document.currentScript.parentNode, \{ displayMode: true \});'.format(markdown.util.AtomicString(m.group(2) + m.group(4) + m.group(5))))
            else:
#                node.set('data-expr', markdown.util.AtomicString(m.group(3)))
                script_node.text = markdown.util.AtomicString(
                    'katex.render("{}", document.currentScript.parentNode, \{ displayMode: true \});'.format(markdown.util.AtomicString(m.group(3))))
            return node

        configs = self.getConfigs()
        inlinemathpatterns = (
            markdown.inlinepatterns.Pattern(r'(?<!\\|\$)(\$)([^\$]+)(\$)'),  #  $...$
            markdown.inlinepatterns.Pattern(r'(?<!\\)(\\\()(.+?)(\\\))')     # \(...\)
        )
        mathpatterns = (
            markdown.inlinepatterns.Pattern(r'(?<!\\)(\$\$)([^\$]+)(\$\$)'), # $$...$$
            markdown.inlinepatterns.Pattern(r'(?<!\\)(\\\[)(.+?)(\\\])'),    # \[...\]
            markdown.inlinepatterns.Pattern(r'(?<!\\)(\\begin{([a-z]+?\*?)})(.+?)(\\end{\3})')
        )
        if not configs['enable_dollar_delimiter']:
            inlinemathpatterns = inlinemathpatterns[1:]
        for i, pattern in enumerate(inlinemathpatterns):
            pattern.handleMatch = handle_match_inline
            md.inlinePatterns.add('math-inline-%d' % i, pattern, '<escape')
        for i, pattern in enumerate(mathpatterns):
            pattern.handleMatch = handle_match
            md.inlinePatterns.add('math-%d' % i, pattern, '<escape')

def makeExtension(*args, **kwargs):
    return MathExtension(*args, **kwargs)
