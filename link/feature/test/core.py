# -*- coding: utf-8 -*-

from unittest import TestCase, main

from link.feature.core import Feature
from link.feature.core import addfeatures, getfeatures
from link.feature.core import hasfeature, getfeature


class DummyFeature(Feature):
    name = 'dummy'


class DummyFeature2(Feature):
    name = 'dummy2'


class TestFeature(TestCase):
    def setUp(self):
        # create circular reference for getfeatures tests
        def inner_init(this, dummy):
            self.dummy = dummy

        self.inner_cls = type('InnerDummy', (object,), {
            '__init__': inner_init
        })

        def dummy_init(this):
            this.inner = self.inner_cls(this)

        self.cls = type('Dummy', (object,), {
            '__init__': dummy_init
        })

    def test_addfeatures(self):
        decorator = addfeatures([DummyFeature])
        self.cls = decorator(self.cls)

        self.assertTrue(hasattr(self.cls, '__features__'))
        self.assertIsInstance(self.cls.__features__, list)
        self.assertIn(DummyFeature, self.cls.__features__)

    def test_addfeatures_fail(self):
        with self.assertRaises(TypeError):
            addfeatures([self.cls])

        with self.assertRaises(TypeError):
            addfeatures([self.cls()])

    def test_getfeatures(self):
        obj = self.cls()

        result = getfeatures(obj)

        self.assertEqual(result, [])

        self.cls = addfeatures([DummyFeature])(self.cls)
        obj = self.cls()
        result = getfeatures(obj)

        self.assertEqual(result, [(obj, DummyFeature)])

        self.inner_cls = addfeatures([DummyFeature2])(self.inner_cls)
        obj = self.cls()
        result = getfeatures(obj)

        self.assertEqual(result, [
            (obj, DummyFeature),
            (obj.inner, DummyFeature2)
        ])

    def test_hasfeature(self):
        self.cls = addfeatures([DummyFeature])(self.cls)
        obj = self.cls()
        result = hasfeature(obj, 'dummy')

        self.assertTrue(result)

    def test_not_hasfeature(self):
        obj = self.cls()
        result = hasfeature(obj, 'dummy')

        self.assertFalse(result)

    def test_getfeature(self):
        self.cls = addfeatures([DummyFeature])(self.cls)
        obj = self.cls()
        f = getfeature(obj, 'dummy')

        self.assertIsInstance(f, DummyFeature)
        self.assertIs(f.obj, obj)

    def test_getfeature_fail(self):
        obj = self.cls()

        with self.assertRaises(AttributeError):
            getfeature(obj, 'dummy')


if __name__ == '__main__':
    main()
