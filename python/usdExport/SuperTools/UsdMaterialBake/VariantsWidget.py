from Katana import QtWidgets, QtCore, QtGui
from Katana import NodegraphAPI, Utils
import UI4

class VariantsWidget(QtWidgets.QFrame):
    """ Main Variants widget, contains a toolbar and the VariantsListWidget.
    """

    def __init__(self, node, newVariantName=None, parent=None):
        """
        @param node: The UsdMaterialBake node which should have the following
            methods. addVariantInput, deleteVariantInput, reorderInput,
            renameVariantInput, require3DInput, and the MIN_PORTS attribute.
        @param newVariantName: The name to use when adding new variants with
            the plus button.  If not set, it will default to "variant"
        @param parent: The Qt parent widget for this QFrame.
        @type node: C{GroupNode} (Supertool)
        @type newVariantName: C{str}
        @type parent: C{QtWidgets.Widget}
        """
        super(VariantsWidget, self).__init__(parent=parent)
        self.node = node
        self.newVariantName = newVariantName or "variant"
        self.minPorts = self.node.MIN_PORTS
        self.setAutoFillBackground(True)
        self.setBackgroundRole(QtGui.QPalette.Base)

        Utils.EventModule.RegisterEventHandler(
            self.__onAddOrRemoveInputPort, 'node_addInputPort', None)
        Utils.EventModule.RegisterEventHandler(
            self.__onAddOrRemoveInputPort, 'node_removeInputPort', None)

        # Toolbar to work as heading for Variants widget.
        self.toolbar = QtWidgets.QToolBar(self)
        variantsLabel = QtWidgets.QLabel("Variants")
        self.toolbar.addWidget(variantsLabel)

        # Spacer widget to allow us to align some widgets to the right of the
        # toolbar.
        spacerWidget = QtWidgets.QWidget(self)
        spacerWidget.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Preferred)
        spacerWidget.setVisible(True)
        self.toolbar.addWidget(spacerWidget)

        # Toolbar Actions
        addIcon = UI4.Util.IconManager.GetIcon('Icons/plus16.png')
        self.addAction = self.toolbar.addAction(addIcon, "Add")
        self.addAction.triggered.connect(self.addNewVariant)

        # List Widget
        self.listWidget = VariantsListWidget(self)
        self.listWidget.itemChanged.connect(self.__onCurrentTextChanged)
        self.listWidget.customContextMenuRequested.connect(
            self.customContextMenu)
        self.listWidget.model().rowsMoved.connect(self.__onRowMoved)

        deleteIcon = UI4.Util.IconManager.GetIcon('Icons/trashCan.png')
        self.deleteSelectedAction = QtWidgets.QAction(
            deleteIcon, "Delete", self.listWidget)
        self.listWidget.addAction(self.deleteSelectedAction)
        self.deleteSelectedAction.triggered.connect(self.deleteSelectedVariant)
        self.deleteSelectedAction.setShortcut(QtCore.Qt.Key_Delete)

        # Layout
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.listWidget)
        self.updateWidgets()

    def updateWidgets(self):
        """ Perform a clean reset of the widget and its items.
        """
        self.listWidget.clear()
        # Ensure self.minPorts default ports always available.
        for port in self.node.getInputPorts()[self.minPorts:]:
            item = QtWidgets.QListWidgetItem(port.getName())
            item.setFlags(
                QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsDropEnabled |
                QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemNeverHasChildren |
                QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable)
            self.listWidget.addItem(item)

    def addNewVariant(self):
        """ Add a new input port to this widgets attached node. """
        self.node.addVariantInput(self.newVariantName)

    def deleteSelectedVariant(self):
        """ Delete the input port on this widgets attached node matching the
            currently selected items name.
        """
        index = self.listWidget.currentRow() + self.node.MIN_PORTS
        self.node.deleteVariantInput(index)

    def __onCurrentTextChanged(self, item):
        """ Update the input ports name on the node attached to this widget.
        """
        itemIndex = self.listWidget.row(item) + self.minPorts
        self.node.renameVariantInput(itemIndex, item.text())

    def customContextMenu(self, pos):
        """ Open up a custom context menu. """
        globalPos = self.mapToGlobal(pos)
        menu = QtWidgets.QMenu()
        menu.addAction(self.deleteSelectedAction)
        menu.exec_(globalPos)

    # pylint: disable=undefined-variable
    def __onRowMoved(self, parent, start, end, dest, row):
        """ Update the order of the inputs on the attached node when a row has
            been moved in the listWidget.
        """
        # Because we are moving an item, the resultant row is one earlier than
        # Qt thinks at this point, because it counts our item as existing
        # still.
        if row > start:
            row = row-1
        self.node.reorderInput(start + self.minPorts, row + self.minPorts)

    def __onAddOrRemoveInputPort(self, eventType, eventID,
                               nodeName, portName, port, **kwargs):
        """ When we add or remove input ports, ensure we trigger a new update.
        """
        self.updateWidgets()


class VariantsListWidget(QtWidgets.QListWidget):
    """ A List widget setup to allow for custom context menu's, drag and drop
        as well as some custom styling to match Katana's UI.
    """

    def __init__(self, parent=None):
        super(VariantsListWidget, self).__init__(parent=parent)
        self.setAlternatingRowColors(True)
        self.setAutoFillBackground(True)
        self.setBackgroundRole(QtGui.QPalette.AlternateBase)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.setDragEnabled(True)
        self.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.setStyleSheet(
            "QListWidget {padding: 10px;} QListWidget::item { margin: 5px; }")