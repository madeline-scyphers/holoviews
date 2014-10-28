"""
Test cases for ViewTestCase which implements view comparison.
"""
import numpy as np


from holoviews.core import BoundingBox, Dimension
from holoviews.core.viewmap import ViewMap
from holoviews.testing import ViewTestCase
from holoviews.views import SheetMatrix

class SheetViewTestCase(ViewTestCase):

    def setUp(self):
        self.arr1 = np.array([[1,2], [3,4]])
        self.arr2 = np.array([[10,2], [3,4]])
        self.arr3 = np.array([[10,2], [3,40]])
        # Varying arrays, default bounds
        self.sv1 = SheetMatrix(self.arr1, BoundingBox())
        self.sv2 = SheetMatrix(self.arr2, BoundingBox())
        self.sv3 = SheetMatrix(self.arr3, BoundingBox())
        # Varying arrays, different bounds
        self.sv4 = SheetMatrix(self.arr1, BoundingBox(radius=0.3))
        self.sv5 = SheetMatrix(self.arr2, BoundingBox(radius=0.3))


class SheetOverlayTestCase(SheetViewTestCase):

    def setUp(self):
        super(SheetOverlayTestCase, self).setUp()
        # Two overlays of depth two with different layers
        self.overlay1_depth2 = (self.sv1 * self.sv2)
        self.overlay2_depth2 = (self.sv1 * self.sv3)
        # Overlay of depth 2 with different bounds
        self.overlay3_depth2 = (self.sv4 * self.sv5)
        # # Overlay of depth 3
        self.overlay4_depth3 = (self.sv1 * self.sv2 * self.sv3)


class StackTestCase(SheetOverlayTestCase):

    def setUp(self):
        super(StackTestCase, self).setUp()
        # Example 1D stack
        self.stack1_1D = ViewMap(dimensions=['int'])
        self.stack1_1D[0] = self.sv1
        self.stack1_1D[1] = self.sv2
        # Changed keys...
        self.stack2_1D = ViewMap(dimensions=['int'])
        self.stack2_1D[1] = self.sv1
        self.stack2_1D[2] = self.sv2
        # Changed number of keys...
        self.stack3_1D = ViewMap(dimensions=['int'])
        self.stack3_1D[1] = self.sv1
        self.stack3_1D[2] = self.sv2
        self.stack3_1D[3] = self.sv3
        # Changed values...
        self.stack4_1D = ViewMap(dimensions=['int'])
        self.stack4_1D[0] = self.sv1
        self.stack4_1D[1] = self.sv3
        # Changed bounds...
        self.stack5_1D = ViewMap(dimensions=['int'])
        self.stack5_1D[0] = self.sv4
        self.stack5_1D[1] = self.sv5
        # Example dimension label
        self.stack6_1D = ViewMap(dimensions=['int_v2'])
        self.stack6_1D[0] = self.sv1
        self.stack6_1D[1] = self.sv2
        # A ViewMap of Overlays
        self.stack7_1D = ViewMap(dimensions=['int'])
        self.stack7_1D[0] =  self.overlay1_depth2
        self.stack7_1D[1] =  self.overlay2_depth2
        # A different ViewMap of Overlays
        self.stack8_1D = ViewMap(dimensions=['int'])
        self.stack8_1D[0] =  self.overlay2_depth2
        self.stack8_1D[1] =  self.overlay1_depth2

        # Example 2D stack
        self.stack1_2D = ViewMap(dimensions=['int', Dimension('float')])
        self.stack1_2D[0, 0.5] = self.sv1
        self.stack1_2D[1, 1.0] = self.sv2
        # Changed 2D keys...
        self.stack2_2D = ViewMap(dimensions=['int', Dimension('float')])
        self.stack2_2D[0, 1.0] = self.sv1
        self.stack2_2D[1, 1.5] = self.sv2



class SheetComparisonTest(SheetViewTestCase):
    """
    This tests the ViewTestCase class which is an important component
    of other tests.
    """

    def test_equal(self):
        self.assertEqual(self.sv1, self.sv1)

    def test_unequal_arrays(self):
        try:
            self.assertEqual(self.sv1, self.sv2)
            raise AssertionError("Array mismatch not detected")
        except AssertionError as e:
            assert str(e).startswith('SheetMatrix: \nArrays are not almost equal to 6 decimals')

    def test_bounds_mismatch(self):
        try:
            self.assertEqual(self.sv1, self.sv4)
        except AssertionError as e:
            assert str(e).startswith('BoundingBoxes are mismatched.')



class SheetOverlayComparisonTest(SheetOverlayTestCase):

    def test_depth_mismatch(self):
        try:
            self.assertEqual(self.overlay1_depth2, self.overlay4_depth3)
        except AssertionError as e:
            assert str(e).startswith("Overlays have different lengths.")

    def test_element_mismatch(self):
        try:
            self.assertEqual(self.overlay1_depth2, self.overlay2_depth2)
        except AssertionError as e:
            assert str(e).startswith('SheetMatrix: \nArrays are not almost equal to 6 decimals')



class StackComparisonTest(StackTestCase):

    def test_dimension_mismatch(self):
         try:
             self.assertEqual(self.stack1_1D, self.stack1_2D)
             raise AssertionError("Mismatch in dimension number not detected.")
         except AssertionError as e:
             assert str(e).startswith("HoloMaps have different numbers of dimensions.")

    def test_dimension_label_mismatch(self):
         try:
             self.assertEqual(self.stack1_1D, self.stack6_1D)
             raise AssertionError("Mismatch in dimension labels not detected.")
         except AssertionError as e:
             assert str(e).startswith("HoloMaps have different dimension labels.")


    def test_key_len_mismatch(self):
        try:
            self.assertEqual(self.stack1_1D, self.stack3_1D)
            raise AssertionError("Mismatch in stack key number not detected.")
        except AssertionError as e:
            assert str(e).startswith("HoloMaps have different numbers of keys.")

    def test_key_mismatch(self):
        try:
            self.assertEqual(self.stack1_1D, self.stack2_1D)
            raise AssertionError("Mismatch in stack keys not detected.")
        except AssertionError as e:
            assert str(e).startswith("HoloMaps have different sets of keys.")

    def test_element_mismatch(self):
        try:
            self.assertEqual(self.stack1_1D, self.stack4_1D)
            raise AssertionError("Pane mismatch in array data not detected.")
        except AssertionError as e:
            assert str(e).startswith('SheetMatrix: \nArrays are not almost equal to 6 decimals')


if __name__ == "__main__":
    import sys
    import nose
    nose.runmodule(argv=[sys.argv[0], "--logging-level", "ERROR"])
