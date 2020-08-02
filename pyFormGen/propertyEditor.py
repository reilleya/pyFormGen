import math

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLineEdit
from PyQt5.QtWidgets import QDoubleSpinBox, QSpinBox, QComboBox
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QDoubleValidator

from . import properties
from . import units

class PropertyEditor(QWidget):

    valueChanged = pyqtSignal()

    def __init__(self, parent, prop, preferences):
        super(PropertyEditor, self).__init__(QWidget(parent))
        self.preferences = preferences
        self.setLayout(QHBoxLayout())
        self.prop = prop

        if self.preferences is not None:
            self.dispUnit = self.preferences.getUnit(self.prop.unit)
        else:
            self.dispUnit = self.prop.unit

        if isinstance(prop, properties.FloatProperty):
            self.currentValue = self.prop.getValue()
            self.editor = QLineEdit()
            self.editor.setMaximumWidth(200)
            self.editor.setAlignment(Qt.AlignRight)
            self.editor.editingFinished.connect(self.textEntered)
            self.editor.inputRejected.connect(self.invalidEntry)

            self.unitSelector = QComboBox()
            self.unitSelector.setMinimumWidth(150)
            self.unitSelector.setMaximumWidth(150)
            self.unitSelector.addItems(units.getAllConversions(self.prop.unit))
            if len(units.getAllConversions(self.prop.unit)) == 1:
                self.unitSelector.setEnabled(False)
            self.unitSelector.setCurrentText(self.dispUnit)
            self.updateUnits()
            self.unitSelector.currentTextChanged.connect(self.updateUnits)

            self.layout().addWidget(self.editor)
            self.layout().addWidget(self.unitSelector)

        elif isinstance(prop, properties.IntProperty):
            self.editor = QSpinBox()

            convMin = units.convert(self.prop.min, self.prop.unit, self.dispUnit)
            convMax = units.convert(self.prop.max, self.prop.unit, self.dispUnit)
            self.editor.setRange(convMin, convMax)

            self.editor.setValue(self.prop.getValue())
            self.editor.valueChanged.connect(self.valueChanged.emit)
            self.layout().addWidget(self.editor)

        elif isinstance(prop, properties.StringProperty):
            self.editor = QLineEdit()
            self.editor.setText(self.prop.getValue())
            self.layout().addWidget(self.editor)

        elif isinstance(prop, properties.EnumProperty):
            self.editor = QComboBox()

            self.editor.addItems(self.prop.values)
            self.editor.setCurrentText(self.prop.value)
            self.editor.currentTextChanged.connect(self.valueChanged.emit)

            self.layout().addWidget(self.editor)

    def getValue(self):
        if isinstance(self.prop, properties.FloatProperty):
            self.textEntered() # OSX needs this as focus doesn't leave line edits when they click a button
            return self.currentValue

        if isinstance(self.prop, properties.IntProperty):
            return units.convert(self.editor.value(), self.dispUnit, self.prop.unit)

        if isinstance(self.prop, properties.StringProperty):
            return self.editor.text()

        if isinstance(self.prop, properties.EnumProperty):
            return self.editor.currentText()

        return None

    def updateUnits(self):
        if isinstance(self.prop, properties.FloatProperty):
            self.dispUnit = self.unitSelector.currentText()
            self.unitSelector.setCurrentText(self.dispUnit)
            convMin = units.convert(self.prop.min, self.prop.unit, self.dispUnit)
            convMax = units.convert(self.prop.max, self.prop.unit, self.dispUnit)
            self.editor.setValidator(QDoubleValidator(convMin, convMax, 8))
            self.editor.setText('{:.8f}'.format(units.convert(self.currentValue, self.prop.unit, self.dispUnit)))

    def textEntered(self):
        self.currentValue = units.convert(float(self.editor.text()), self.dispUnit, self.prop.unit)
        self.valueChanged.emit()

    def invalidEntry(self):
        self.editor.setText('{:.8f}'.format(units.convert(self.currentValue, self.prop.unit, self.dispUnit)))
