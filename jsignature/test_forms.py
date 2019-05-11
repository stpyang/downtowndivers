from django.test import SimpleTestCase
from django.core.exceptions import ValidationError

from .widgets import JSignatureWidget
from .forms import JSignatureField


class JSignatureFormFieldTest(SimpleTestCase):

    def test_widget(self):
        field = JSignatureField()
        self.assertIsInstance(field.widget, JSignatureWidget)

    def test_to_python_empty_values(self):
        field = JSignatureField()
        for val in ['', [], '[]']:
            self.assertIsNone(field.to_python(val))

    def test_to_python_correct_values(self):
        field = JSignatureField()
        val = '[{"x":[1,2], "y":[3,4]}]'
        self.assertEqual([{'x': [1, 2], 'y': [3, 4]}], field.to_python(val))

    def test_to_python_incorrect_values(self):
        field = JSignatureField()
        val = 'foo'
        self.assertRaises(ValidationError, field.to_python, val)
