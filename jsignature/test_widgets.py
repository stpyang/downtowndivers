import json
from pyquery import PyQuery as pq
import six

from django.test import SimpleTestCase
from django.core.exceptions import ValidationError

from .widgets import JSignatureWidget
from .settings import JSIGNATURE_HEIGHT


class JSignatureWidgetTest(SimpleTestCase):

    def test_default_media(self):
        widget = JSignatureWidget()
        media = widget.media
        media_js = list(media.render_js())
        self.assertEqual(2, len(media_js))
        media_js_str = "".join(media_js)
        self.assertIn('jSignature.min.js', media_js_str)
        self.assertIn('django_jsignature.js', media_js_str)
        media_css = list(media.render_css())
        self.assertEqual([], media_css)

    def test_init(self):
        widget = JSignatureWidget()
        self.assertEqual({}, widget.jsignature_attrs)
        given_attrs = {'width': 300, 'height': 100}
        widget = JSignatureWidget(jsignature_attrs=given_attrs)
        self.assertEqual(given_attrs, widget.jsignature_attrs)

    def test_build_jsignature_id(self):
        widget = JSignatureWidget()
        id = widget.build_jsignature_id('foo')
        self.assertEqual('jsign_foo', id)

    def test_build_jsignature_config(self):
        widget = JSignatureWidget(jsignature_attrs={'width': 400})
        config = widget.build_jsignature_config()
        self.assertEqual(400, config.get('width'))
        self.assertEqual(JSIGNATURE_HEIGHT, config.get('height'))

    def test_prep_value_empty_values(self):
        widget = JSignatureWidget()
        for val in ['', [], '[]']:
            self.assertEqual('[]', widget.prep_value(val))

    def test_prep_value_correct_values_python(self):
        widget = JSignatureWidget()
        val = [{"x": [1, 2], "y": [3, 4]}]
        val_prep = widget.prep_value(val)
        self.assertIsInstance(val_prep, six.string_types)
        self.assertEqual(val, json.loads(val_prep))

    def test_prep_value_correct_values_json(self):
        widget = JSignatureWidget()
        val = [{"x": [1, 2], "y": [3, 4]}]
        val_str = '[{"x":[1,2], "y":[3,4]}]'
        val_prep = widget.prep_value(val_str)
        self.assertIsInstance(val_prep, six.string_types)
        self.assertEqual(val, json.loads(val_prep))

    def test_prep_value_incorrect_values(self):
        widget = JSignatureWidget()
        val = type('Foo')
        self.assertRaises(ValidationError, widget.prep_value, val)

    def test_render(self):
        widget = JSignatureWidget()
        output = widget.render(name='foo', value=None)
        # Almost useless :/
        self.assertEqual(1, len(pq('.jsign-wrapper', output)))
        self.assertEqual(1, len(pq('[type=hidden]', output)))

    def test_render_reset_button_true(self):
        widget = JSignatureWidget(jsignature_attrs={'ResetButton': True})
        output = widget.render(name='foo', value=None)
        self.assertEqual(1, len(pq('[type=button]', output)))

    def test_render_reset_button_false(self):
        widget = JSignatureWidget(jsignature_attrs={'ResetButton': False})
        output = widget.render(name='foo', value=None)
        self.assertEqual(0, len(pq('[type=button]', output)))
