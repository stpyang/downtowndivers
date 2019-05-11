import json
import six

from django.test import SimpleTestCase
from django.core.exceptions import ValidationError

from .fields import JSignatureField
from .forms import JSignatureField as JSignatureFormField


class JSignatureFieldTest(SimpleTestCase):

    def test_to_python_empty(self):
        field = JSignatureField()
        for val in ['', [], '[]']:
            self.assertIsNone(field.to_python(val))

    def test_to_python_correct_value_python(self):
        field = JSignatureField()
        val = [{"x": [1, 2], "y": [3, 4]}]
        self.assertEqual(val, field.to_python(val))

    def test_to_python_correct_value_json(self):
        field = JSignatureField()
        val = [{"x": [1, 2], "y": [3, 4]}]
        val_str = '[{"x":[1,2], "y":[3,4]}]'
        self.assertEqual(val, field.to_python(val_str))

    def test_to_python_incorrect_value(self):
        field = JSignatureField()
        val = 'foo'
        self.assertRaises(ValidationError, field.to_python, val)

    def test_get_prep_value_empty(self):
        field = JSignatureField()
        for val in ['', [], '[]']:
            self.assertIsNone(field.get_prep_value(val))

    def test_get_prep_value_correct_values_python(self):
        field = JSignatureField()
        val = [{"x": [1, 2], "y": [3, 4]}]
        val_prep = field.get_prep_value(val)
        self.assertIsInstance(val_prep, six.string_types)
        self.assertEqual(val, json.loads(val_prep))

    def test_get_prep_value_correct_values_json(self):
        field = JSignatureField()
        val = [{"x": [1, 2], "y": [3, 4]}]
        val_str = '[{"x":[1,2], "y":[3,4]}]'
        val_prep = field.get_prep_value(val_str)
        self.assertIsInstance(val_prep, six.string_types)
        self.assertEqual(val, json.loads(val_prep))

    def test_get_prep_value_incorrect_values(self):
        field = JSignatureField()
        val = type('Foo')
        self.assertRaises(ValidationError, field.get_prep_value, val)

    def test_formfield(self):
        field = JSignatureField()
        cls = field.formfield().__class__
        self.assertTrue(issubclass(cls, JSignatureFormField))
